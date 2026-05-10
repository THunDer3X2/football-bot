import requests
import os

def send_discord(msg):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    requests.post(webhook_url, json={"content": msg})

def main():
    api_key = os.getenv('FOOTBALL_API_KEY')
    # ส่งข้อความทดสอบเข้า Discord
    send_discord("⚽ บอทฟุตบอลเชื่อมต่อสำเร็จ! พร้อมรันอัตโนมัติแล้วครับ")

if __name__ == "__main__":
    main()
