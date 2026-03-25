from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn

from tft_us_quantdb.config.core import ModelConfig
from tft_us_quantdb.data.contracts import WindowedBatch


class GatedResidualNetwork(nn.Module):
    def __init__(self, input_dim: int, hidden_size: int, output_dim: int) -> None:
        super().__init__()
        self.ff = nn.Sequential(
            nn.Linear(input_dim, hidden_size),
            nn.ELU(),
            nn.Linear(hidden_size, output_dim),
        )
        self.gate = nn.Sequential(nn.Linear(output_dim, output_dim), nn.Sigmoid())
        self.skip = nn.Linear(input_dim, output_dim) if input_dim != output_dim else nn.Identity()
        self.norm = nn.LayerNorm(output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        transformed = self.ff(x)
        gated = transformed * self.gate(transformed)
        return self.norm(gated + self.skip(x))


class VariableSelectionNetwork(nn.Module):
    def __init__(self, input_dim: int, hidden_size: int) -> None:
        super().__init__()
        self.selector = GatedResidualNetwork(input_dim, hidden_size, input_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        weights = torch.softmax(self.selector(x), dim=-1)
        return x * weights


@dataclass(frozen=True)
class TftOutput:
    logits: torch.Tensor
    attention: torch.Tensor
    encoded_sequence: torch.Tensor


class TemporalFusionClassifier(nn.Module):
    def __init__(self, config: ModelConfig, static_dim: int, known_future_dim: int, observed_dim: int) -> None:
        super().__init__()
        self.config = config
        self.static_embedding = GatedResidualNetwork(static_dim, config.hidden_size, config.hidden_size)
        self.temporal_projection = nn.Linear(known_future_dim + observed_dim, config.hidden_size)
        self.variable_selection = VariableSelectionNetwork(config.hidden_size, config.hidden_size)
        self.encoder = nn.LSTM(
            input_size=config.hidden_size,
            hidden_size=config.hidden_size,
            num_layers=config.lstm_layers,
            batch_first=True,
        )
        self.decoder = nn.LSTM(
            input_size=config.hidden_size,
            hidden_size=config.hidden_size,
            num_layers=config.lstm_layers,
            batch_first=True,
        )
        self.attention = nn.MultiheadAttention(
            embed_dim=config.hidden_size,
            num_heads=config.attention_heads,
            dropout=config.dropout,
            batch_first=True,
        )
        self.classifier = nn.Sequential(
            nn.LayerNorm(config.hidden_size),
            nn.Dropout(config.dropout),
            nn.Linear(config.hidden_size, config.output_dim),
        )

    def forward(self, batch: WindowedBatch) -> TftOutput:
        static_context = self.static_embedding(batch.static_real).unsqueeze(1)
        temporal = torch.cat((batch.known_future, batch.observed_past), dim=-1)
        temporal = self.temporal_projection(temporal)
        temporal = temporal + static_context
        temporal = self.variable_selection(temporal)

        context_length = self.config.context_length
        encoded, state = self.encoder(temporal[:, :context_length, :])
        decoded, _ = self.decoder(temporal[:, context_length:, :], state)
        attended, attention = self.attention(decoded, encoded, encoded)
        logits = self.classifier(attended)
        return TftOutput(logits=logits, attention=attention, encoded_sequence=encoded)
