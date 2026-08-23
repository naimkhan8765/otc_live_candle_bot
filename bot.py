import os
import time
import json
import urllib.request
import urllib.parse

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def telegram(method, data=None):
    url = f"{API}/{method}"
    encoded = urllib.parse.urlencode(data or {}).encode()
    request = urllib.request.Request(url, data=encoded)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode())


def send_message(chat_id, text):
    telegram("sendMessage", {
        "chat_id": chat_id,
        "text": text
    })


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

    if text == "/start":
        send_message(
            chat_id,
            "🟢 OTC Live Candle Bot\n\n"
            "স্বাগতম!\n\n"
            "📊 /markets - মার্কেট তালিকা\n"
            "🕐 /candle - Candle তথ্য\n"
            "ℹ️ /help - সাহায্য"
        )

    elif text == "/markets":
        send_message(
            chat_id,
            "📊 Markets\n\n"
            "OTC\n"
            "EUR/USD\n"
            "GBP/USD\n"
            "USD/JPY\n\n"
            "⚠️ Live data source এখনো সংযুক্ত করা হয়নি।"
        )

    elif text == "/candle":
        send_message(
            chat_id,
            "🕯 Candle\n\n"
            "5 SEC\n"
            "10 SEC\n"
            "1 MIN\n\n"
            "⚠️ Real-time candle feed এখনো সংযুক্ত করা হয়নি।"
        )

    elif text == "/help":
        send_message(
            chat_id,
            "/start - বট শুরু\n"
            "/markets - মার্কেট\n"
            "/candle - Candle menu"
        )

    else:
        send_message(
            chat_id,
            "কমান্ড বুঝতে পারিনি। /start লিখো।"
        )


def main():
    offset = 0

    print("Bot is running...")

    while True:
        try:
            result = telegram("getUpdates", {
                "timeout": 25,
                "offset": offset
            })

            for update in result.get("result", []):
                offset = update["update_id"] + 1

                if "message" in update:
                    handle_message(update["message"])

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
