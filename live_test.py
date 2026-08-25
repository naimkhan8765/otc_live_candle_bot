import time

from live_feed import LiveFeed


def main():
    feed = LiveFeed()

    print("=== OTC LIVE FEED TEST ===")

    feed.start()

    print("Feed adapter started.")
    print("Waiting for real market data...")
    print("No fake price will be generated.")

    time.sleep(10)

    feed.stop()

    print("=== TEST FINISHED ===")


if __name__ == "__main__":
    main()
