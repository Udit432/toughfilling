import requests
import time

# ====== CONFIG ======
WALLET = "0xa8fac068d32639c40188563c83c206b320e57dda"

BOT_TOKEN = "8675973300:AAE-_m3brqtqhFD27JmawD2QM_CCd3U_tns"
CHAT_ID = "5081251584"

POLL_INTERVAL = 5  # seconds

last_tx_hash = None

# ====== TELEGRAM SEND ======
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

# ====== FETCH TRANSACTIONS ======
def get_latest_tx():
    url = f"https://api.polygonscan.com/api?module=account&action=txlist&address={WALLET}&sort=desc"
    res = requests.get(url).json()

    if res["status"] != "1":
        return None

    return res["result"][0]

# ====== MAIN LOOP ======
print("Bot started...")

while True:
    try:
        tx = get_latest_tx()

        if tx:
            global last_tx_hash

            if last_tx_hash != tx["hash"]:
                last_tx_hash = tx["hash"]

                msg = f"""
🚨 New Activity Detected

Hash: {tx['hash']}
From: {tx['from']}
To: {tx['to']}
Value: {int(tx['value'])/10**18} MATIC
Time: {tx['timeStamp']}
"""

                print(msg)
                send_telegram(msg)

        time.sleep(POLL_INTERVAL)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
