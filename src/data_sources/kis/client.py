from __future__ import annotations

from datetime import datetime, UTC
import requests
from typing import Any

from src.data_sources.kis.config import KISConfig


class KISClient:
    def __init__(self, config: KISConfig):
        self.config = config
        self._access_token: str | None = None

    def authenticate(self) -> str:
        url = f"{self.config.base_url}/oauth2/tokenP"
        payload = {
            "grant_type": "client_credentials",
            "appkey": self.config.app_key,
            "appsecret": self.config.app_secret,
        }
        headers = {
            "content-type": "application/json",
        }
        res = requests.post(url, json=payload, headers=headers, timeout=20)
        res.raise_for_status()
        body = res.json()
        token = body["access_token"]
        self._access_token = token
        return token

    def _headers(self, tr_id: str) -> dict[str, str]:
        if not self._access_token:
            self.authenticate()
        return {
            "content-type": "application/json; charset=utf-8",
            "authorization": f"Bearer {self._access_token}",
            "appkey": self.config.app_key,
            "appsecret": self.config.app_secret,
            "tr_id": tr_id,
            "custtype": "P",
        }

    def get(self, api_path: str, tr_id: str, params: dict[str, Any]) -> dict[str, Any]:
        url = f"{self.config.base_url}{api_path}"
        res = requests.get(url, headers=self._headers(tr_id), params=params, timeout=20)
        res.raise_for_status()
        return res.json()

    def inquire_domestic_future_asking_price(self, market_code: str, symbol: str) -> dict[str, Any]:
        return self.get(
            "/uapi/domestic-futureoption/v1/quotations/inquire-asking-price",
            tr_id="FHMIF10010000",
            params={
                "FID_COND_MRKT_DIV_CODE": market_code,
                "FID_INPUT_ISCD": symbol,
            },
        )

    def inquire_domestic_future_minute_bars(
        self,
        market_code: str,
        symbol: str,
        hour_cls_code: str = "60",
        include_past: str = "Y",
        include_fake_tick: str = "N",
        input_date: str | None = None,
        input_hour: str | None = None,
    ) -> dict[str, Any]:
        now = datetime.now(UTC)
        if input_date is None:
            input_date = now.strftime("%Y%m%d")
        if input_hour is None:
            input_hour = now.strftime("%H%M%S")
        return self.get(
            "/uapi/domestic-futureoption/v1/quotations/inquire-time-fuopchartprice",
            tr_id="FHKIF03020200",
            params={
                "FID_COND_MRKT_DIV_CODE": market_code,
                "FID_INPUT_ISCD": symbol,
                "FID_HOUR_CLS_CODE": hour_cls_code,
                "FID_PW_DATA_INCU_YN": include_past,
                "FID_FAKE_TICK_INCU_YN": include_fake_tick,
                "FID_INPUT_DATE_1": input_date,
                "FID_INPUT_HOUR_1": input_hour,
            },
        )
