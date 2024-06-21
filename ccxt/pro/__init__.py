# -*- coding: utf-8 -*-

"""CCXT: CryptoCurrency eXchange Trading Library (Async)"""

# ----------------------------------------------------------------------------

__version__ = '4.3.45'

# ----------------------------------------------------------------------------

from ccxt.async_support.base.exchange import Exchange  # noqa: F401

# CCXT Pro exchanges (now this is mainly used for importing exchanges in WS tests)

from ccxt.pro.bybit import bybit                                          # noqa: F401
from ccxt.pro.coinex import coinex                                        # noqa: F401



exchanges = [
    'bybit',
    'coinex',
]
