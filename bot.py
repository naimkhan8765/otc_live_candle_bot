import os
import time
import json
import urllib.request
import urllib.parse

from candle_engine import CandleEngine

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

engine = CandleEngine()


def telegram(method, data=None):
    url = f"{API}/{method}"
    encoded = urllib.parse.urlencode(data or {}).encode()

    request = urllib.request.Request(
        url,
        data=encoded
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def send_message(chat_id, text):
    telegram(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": text
        }
    )


def candle_menu():
    return (
        "🕯 CANDLE TIMEFRAMES\n\n"
        "⚡ 5 SEC\n"
        "⚡ 10 SEC\n"
        "⚡ 1 MIN\n\n"
        "Live price source এখনো যুক্ত করা হয়নি।"
    )


def market_menu():
    return (
        "📊 MARKET LIST\n\n"
        "🟢 REAL MARKET\n"
        "EUR/USD\n"
        "GBP/USD\n"
        "USD/JPY\n"
        "USD/CHF\n\n"
        "🟣 OTC MARKET\n"
        "EUR/USD OTC\n"
        "GBP/USD OTC\n"
        "USD/JPY OTC\n\n"
        "⚠️ এগুলো এখন শুধু menu। "
        "Actual live feed পরের ধাপে যুক্ত হবে।"
    )


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if text == "/start":
        send_message(
            chat_id,
            "🟢 OTC LIVE CANDLE BOT\n\n"
            "Bot connection working.\n\n"
            "📊 /markets - Real + OTC market\n"
            "🕯 /candle - 5s / 10s / 1m\n"
            "ℹ️ /help - Help"
        )

    elif text == "/markets":
        send_message(
            chat_id,
            market_menu()
        )

    elif text == "/candle":
        send_message(
            chat_id,
            candle_menu()
        )

    elif text == "/help":
        send_message(
            chat_id,
            "📖 COMMANDS\n\n"
            "/start - Bot start\n"
            "/markets - Market list\n"
            "/candle - Candle timeframes\n"
            "/help - Help"
        )

    else:
        send_message(
            chat_id,
            "কমান্ড বুঝতে পারিনি।\n\n"
            "/start লিখো।"
        )
print("Testing Telegram connection...")

test = telegram("getMe")

print("Telegram API response:", test)

if not test.get("ok"):
    raise RuntimeError(f"Telegram API failed: {test}")

print("Telegram connection OK")
print("Bot:", test["result"]["username"])

def main():
    offset = 0

    print("OTC Live Candle Bot is running...")

    while True:
        try:
            result = telegram(
                "getUpdates",
                {
                    "timeout": 25,
                    "offset": offset
                }
            )

            for update in result.get("result", []):
                offset = update["update_id"] + 1

                if "message" in update:
                    handle_message(update["message"])

        except Exception as error:
            print("Error:", error)
            time.sleep(5)


if __name__ == "__main__":
    main()
