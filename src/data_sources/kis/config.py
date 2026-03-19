from __future__ import annotations

import os
from dataclasses import dataclass

from src.common.env import load_env_file


@dataclass
class KISConfig:
    app_key: str
    app_secret: str
    base_url: str
    account_no: str | None = None
    account_no_sub: str | None = None
    polling_interval_sec: int = 2
    tr_stock_minute: str | None = None
    tr_deriv_minute: str | None = None
    tr_option_chain: str | None = None
    tr_deriv_order: str | None = None
    tr_deriv_order_rvsecncl: str | None = None
    tr_deriv_balance: str | None = None
    tr_deriv_order_list: str | None = None
    tr_bid_ask_list: str | None = None

    @classmethod
    def from_env(cls) -> "KISConfig":
        load_env_file('.env')
        return cls(
            app_key=os.environ["KIS_APP_KEY"],
            app_secret=os.environ["KIS_APP_SECRET"],
            base_url=os.environ["KIS_BASE_URL"],
            account_no=os.environ.get("KIS_ACCOUNT_NO"),
            account_no_sub=os.environ.get("KIS_ACCOUNT_NO_SUB"),
            polling_interval_sec=int(os.environ.get("KIS_POLLING_INTERVAL_SEC", "2")),
            tr_stock_minute=os.environ.get("KIS_TR_STOCK_MINUTE"),
            tr_deriv_minute=os.environ.get("KIS_TR_DERIV_MINUTE"),
            tr_option_chain=os.environ.get("KIS_TR_OPTION_CHAIN"),
            tr_deriv_order=os.environ.get("KIS_TR_DERIV_ORDER"),
            tr_deriv_order_rvsecncl=os.environ.get("KIS_TR_DERIV_ORDER_RVSECNCL"),
            tr_deriv_balance=os.environ.get("KIS_TR_DERIV_BALANCE"),
            tr_deriv_order_list=os.environ.get("KIS_TR_DERIV_ORDER_LIST"),
            tr_bid_ask_list=os.environ.get("KIS_TR_BID_ASK_LIST"),
        )
