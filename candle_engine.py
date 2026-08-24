from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:
    start: int
    open: float
    high: float
    low: float
    close: float


class CandleEngine:
    def __init__(self):
        self.candles = {}

    def update(self, symbol, price, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().timestamp()

        price = float(price)
        timestamp = int(timestamp)

        periods = {
            "5s": 5,
            "10s": 10,
            "1m": 60
        }

        result = {}

        for name, seconds in periods.items():
            start = timestamp - (timestamp % seconds)
            key = (symbol, name)

            candle = self.candles.get(key)

            if candle is None or candle.start != start:
                candle = Candle(
                    start=start,
                    open=price,
                    high=price,
                    low=price,
                    close=price
                )
                self.candles[key] = candle
            else:
                candle.high = max(candle.high, price)
                candle.low = min(candle.low, price)
                candle.close = price

            result[name] = {
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,
                "start": candle.start
            }

        return result
