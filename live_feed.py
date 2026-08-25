import time


class LiveFeed:
    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        print("Live feed adapter started")

    def stop(self):
        self.running = False
        print("Live feed adapter stopped")

    def process_tick(self, symbol, price, timestamp=None):
        if timestamp is None:
            timestamp = int(time.time())

        return {
            "symbol": symbol,
            "price": float(price),
            "timestamp": timestamp
        }
