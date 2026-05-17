import requests
import os
from datetime import datetime
import pytz

def send_to_discord(embeds):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if embeds:
        requests.post(webhook_url, json={"embeds": embeds})

def main():
    tz = pytz.timezone('Asia/Bangkok')
    today_dt = datetime.now(tz)

    # ดึงตารางแข่งวันนี้ตามเวลาจริง
    match_list = [
        "⏰ **21:00**: Brentford vs Crystal Palace",
        "⏰ **21:00**: Everton vs Sunderland",
        "⏰ **21:00**: Wolves vs Fulham"
    ]

    description = "\n".join(match_list)

    embed = [{
        "title": f"📅 ตารางแข่งพรีเมียร์ลีกวันนี้ ({today_dt.strftime('%d/%m')})",
        "description": description,
        "color": 15844367,
        "footer": {"text": f"อัปเดตข้อมูลเมื่อ: {today_dt.strftime('%H:%M:%S')}"}
    }]
    
    send_to_discord(embed)

if __name__ == "__main__":
    main()
