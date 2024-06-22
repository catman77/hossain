import asyncio
import inspect
import logging
import signal
from copy import deepcopy
from datetime import datetime, timedelta, timezone
from math import floor, isnan
from threading import Lock
from typing import Any, Coroutine, Dict, List, Literal, Optional, Tuple, Union

import ccxt
import ccxt.async_support as ccxt_async
from math import floor
from freqtrade.constants import (BuySell, MakerTaker)
from freqtrade.enums import MarginMode, TradingMode
from freqtrade.exceptions import (DDosProtection,InsufficientFundsError,InvalidOrderException,OperationalException,RetryableOrderError,TemporaryError)
from freqtrade.exchange.common import (API_FETCH_ORDER_RETRY_COUNT,retrier)


from freqtrade.exchange import Exchange


logger = logging.getLogger(__name__)



class Coinex(Exchange):

    _ft_has_futures: Dict = {
        "stoploss_on_exchange": False,
        "order_time_in_force": ["GTC"],
        "ohlcv_candle_limit": 1000,
        "tickers_have_bid_ask": True,
        "l2_limit_range": [5,10,20,50],
        "mark_ohlcv_price": "mark_price",
    }


    _supported_trading_mode_margin_pairs: List[Tuple[TradingMode, MarginMode]] = [
        # TradingMode.SPOT always supported and not required in this list
        # (TradingMode.FUTURES, MarginMode.CROSS),
        (TradingMode.FUTURES, MarginMode.ISOLATED)
    ]


    @property
    def _ccxt_config(self) -> Dict:
        return {"options": {"defaultType": self._ft_has["ccxt_futures_name"]}}


    def _lev_prep(self, pair: str, leverage: float, side: BuySell, accept_fail: bool = False):
        if self.trading_mode != TradingMode.SPOT:
            self._set_leverage(leverage, pair, accept_fail)

    @retrier
    def _set_leverage(self,leverage: float,pair: Optional[str] = None,accept_fail: bool = False):

        if self._config["dry_run"] or not self.exchange_has("setLeverage"):
            return
        try:
            lev = int(floor(leverage))
            res = self._api.set_leverage(leverage= lev , symbol= pair)
            self._log_exchange_response("set_leverage", res)

        except ccxt.DDoSProtection as e:
            raise DDosProtection(e) from e
        except (ccxt.BadRequest, ccxt.OperationRejected, ccxt.InsufficientFunds) as e:
            if not accept_fail:
                raise TemporaryError(f"Could not set leverage due to {e.__class__.__name__}. Message: {e}"
                ) from e
        except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
            raise TemporaryError(f"Could not set leverage due to {e.__class__.__name__}. Message: {e}"
            ) from e
        except ccxt.BaseError as e:
            raise OperationalException(e) from e



    def create_order(self,*,pair: str,ordertype: str,side: BuySell,amount: float,rate: float,leverage: float,reduceOnly: bool = False,time_in_force: str = "GTC") -> Dict:

        if self._config["dry_run"]:
            dry_order = self.create_dry_run_order(pair, ordertype, side, amount, self.price_to_precision(pair, rate), leverage)
            return dry_order

        try:
            amount = self.amount_to_precision(pair, self._amount_to_contracts(pair, amount))
            needs_price = self._order_needs_price(ordertype)
            rate_for_order = self.price_to_precision(pair, rate) if needs_price else None

            if not reduceOnly:
                params = {}
                self._lev_prep(pair, leverage, side)
                order = self._api.create_order( symbol= pair,type= ordertype, side=side, amount= amount, price= rate_for_order)

            if reduceOnly:
                params = {}
                order = self._api.close_coinex_position(symbol= pair ,type= ordertype , side= side , amount= amount , price= rate_for_order)

            if order.get("status") is None:
                order["status"] = "open"

            if order.get("type") is None:
                order["type"] = ordertype

            self._log_exchange_response("create_order", order)
            order = self._order_contracts_to_amount(order)

            return order

        except ccxt.InsufficientFunds as e:
            raise InsufficientFundsError(f"Insufficient funds to create {ordertype} {side} order on market {pair}. "
                f"Tried to {side} amount {amount} at rate {rate}."
                f"Message: {e}") from e
        except ccxt.InvalidOrder as e:
            raise InvalidOrderException(f"Could not create {ordertype} {side} order on market {pair}. "
                f"Tried to {side} amount {amount} at rate {rate}. "
                f"Message: {e}") from e
        except ccxt.DDoSProtection as e:
            raise DDosProtection(e) from e
        except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
            raise TemporaryError(f"Could not place {side} order due to {e.__class__.__name__}. Message: {e}"
            ) from e
        except ccxt.BaseError as e:
            raise OperationalException(e) from e




    @retrier(retries=API_FETCH_ORDER_RETRY_COUNT)
    def fetch_order(self, order_id: str, pair: str, params: Optional[Dict] = None) -> Dict:
        if self._config["dry_run"]:
            return self.fetch_dry_run_order(order_id)
        try:
            params = {}
            order = self._api.fetch_order(id= order_id,symbol= pair, params=params)
            self._log_exchange_response("fetch_order", order)
            order = self._order_contracts_to_amount(order)
            return order

        except ccxt.OrderNotFound as e:
            raise RetryableOrderError(f"Order not found (pair: {pair} id: {order_id}). Message: {e}"
            ) from e
        except ccxt.InvalidOrder as e:
            raise InvalidOrderException(f"Tried to get an invalid order (pair: {pair} id: {order_id}). Message: {e}"
            ) from e
        except ccxt.DDoSProtection as e:
            raise DDosProtection(e) from e
        except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
            raise TemporaryError(f"Could not get order due to {e.__class__.__name__}. Message: {e}"
            ) from e
        except ccxt.BaseError as e:
            raise OperationalException(e) from e


        

    @retrier
    def cancel_order(self, order_id: str, pair: str, params: Optional[Dict] = None) -> Dict:
        if self._config["dry_run"]:
            try:
                order = self.fetch_dry_run_order(order_id)
                order.update({"status": "canceled", "filled": 0.0, "remaining": order["amount"]})
                return order
            except InvalidOrderException:
                return {}

        try:
            params = {}

            order = self._api.cancel_order(id= order_id, symbol= pair)
            self._log_exchange_response("cancel_order", order)
            order = self._order_contracts_to_amount(order)
            return order

        except ccxt.InvalidOrder as e:
            raise InvalidOrderException(f"Could not cancel order. Message: {e}") from e
        except ccxt.DDoSProtection as e:
            raise DDosProtection(e) from e
        except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
            raise TemporaryError(f"Could not cancel order due to {e.__class__.__name__}. Message: {e}"
            ) from e
        except ccxt.BaseError as e:
            raise OperationalException(e) from e


    @retrier
    def fetch_positions(self, pair: Optional[str] = None) -> List[Dict]:

        if self._config["dry_run"] or self.trading_mode != TradingMode.FUTURES:
            return []
        try:
            symbols = []
            positions: List[Dict] = None

            if pair is None:
                positions: List[Dict] = self._api.fetch_positions()
            
            if pair:
                symbols.append(pair)
                positions: List[Dict] = self._api.fetch_positions(symbols= symbols)

            self._log_exchange_response("fetch_positions", positions)
            return positions

        except ccxt.DDoSProtection as e:
            raise DDosProtection(e) from e
        except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
            raise TemporaryError(f"Could not get positions due to {e.__class__.__name__}. Message: {e}"
            ) from e
        except ccxt.BaseError as e:
            raise OperationalException(e) from e


    @retrier(retries=0)
    def fetch_orders(self, pair: str, since: datetime, params: Optional[Dict] = None) -> List[Dict]:
        if self._config["dry_run"]:
            return []
        try:
            since_ms = int((since.timestamp() - 10) * 1000)

            if not params:
                params = {}

            try:
                orders: List[Dict] = self._api.fetch_orders(pair, since=since_ms, params=params)
            except ccxt.NotSupported:
                orders = self._fetch_orders_emulate(pair, since_ms)

            self._log_exchange_response("fetch_orders", orders)
            orders = [self._order_contracts_to_amount(o) for o in orders]
            return orders

        except ccxt.DDoSProtection as e:
            raise DDosProtection(e) from e
        except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
            raise TemporaryError(f"Could not fetch positions due to {e.__class__.__name__}. Message: {e}"
            ) from e
        except ccxt.BaseError as e:
            raise OperationalException(e) from e

    @retrier
    def get_fee(self,symbol: str,type: str = "",side: str = "",amount: float = 1,price: float = 1,taker_or_maker: MakerTaker = "maker") -> float:

        if type and type == "market":
            taker_or_maker = "taker"
        try:
            if self._config.get("fee", None) is not None:
                return self._config["fee"]

        except ccxt.DDoSProtection as e:
            raise DDosProtection(e) from e
        except (ccxt.OperationFailed, ccxt.ExchangeError) as e:
            raise TemporaryError(f"Could not get fee info due to {e.__class__.__name__}. Message: {e}"
            ) from e
        except ccxt.BaseError as e:
            raise OperationalException(e) from e


