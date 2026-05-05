import requests
import time
import threading
from flask import Flask
import os

# ====== CONFIG (Render ENV VARIABLES use करो) ======
WALLET = "0xa8fac068d32639c40188563c83c206b320e57dda"
BOT_TOKEN = "8675973300:AAE-_m3brqtqhFD27JmawD2QM_CCd3U_tns"
CHAT_ID = "5081251584"

POLL_INTERVAL = 5  # seconds

last_tx_hash = None

# ====== TELEGRAM SEND ======
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print("Telegram Error:", e)

# ====== FETCH TRANSACTIONS ======
def get_latest_tx():
    try:
        url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={WALLET}&sort=desc"
        res = requests.get(url).json()

        if res["status"] != "1":
            return None

        return res["result"][0]
    except Exception as e:
        print("Fetch Error:", e)
        return None

# ====== BOT LOOP ======
def run_bot():
    global last_tx_hash

    print("Bot started...")
    send_telegram("🚀 Bot successfully started!")

    while True:
        try:
            tx = get_latest_tx()

            if tx and tx["hash"] != last_tx_hash:
                last_tx_hash = tx["hash"]

                msg = f"""🚨 New Activity Detected

Hash: {tx['hash']}
From: {tx['from']}
To: {tx['to']}
Value: {int(tx['value'])/10**18} MATIC
"""

                print(msg)
                send_telegram(msg)

            time.sleep(POLL_INTERVAL)

        except Exception as e:
            print("Main Loop Error:", e)
            time.sleep(10)

# ====== FLASK SERVER (Render ke liye) ======
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# ====== MAIN ======
if __name__ == "__main__":
    t1 = threading.Thread(target=run_server)
    t2 = threading.Thread(target=run_bot)

    t1.start()
    t2.start()
