import requests
import os
from datetime import datetime
import pytz

def send_to_discord(embeds):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    requests.post(webhook_url, json={"embeds": embeds})

def main():
    api_key = os.getenv('FOOTBALL_API_KEY')
    # กำหนดเวลาไทย
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(tz)
    date_str = now.strftime('%d/%m/%Y')

    embed = [{
        "title": f"⚽ อัปเดตบอทบอลประจำวันที่ {date_str}",
        "description": "เชื่อมต่อระบบรายงานผลสำเร็จ! บอทจะเริ่มแจ้งเตือนเมื่อมีการแข่ง",
        "color": 3447003,
        "footer": {"text": f"เวลาอัปเดต: {now.strftime('%H:%M:%S')}"}
    }]
    
    send_to_discord(embed)

if __name__ == "__main__":
    main()
