import requests
import os
from datetime import datetime
import pytz

def send_discord_embed(embeds):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    data = {"embeds": embeds}
    requests.post(webhook_url, json=data)

def get_football_data():
    api_key = os.getenv('FOOTBALL_API_KEY')
    # ใช้ URL ดึงตารางแข่งตามวันที่
    url = "https://sofascore.p.rapidapi.com/matches/list-by-date"
    
    # ตั้งเวลาเป็นประเทศไทย (Asia/Bangkok)
    tz = pytz.timezone('Asia/Bangkok')
    now = datetime.now(tz)
    date_str = now.strftime('%d/%m/%Y')
    
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    
    # ดึงข้อมูลของวันนี้
    # หมายเหตุ: สำหรับ SofaScore API บางครั้งต้องระบุวันที่ในรูปแบบ d/m/Y หรือ Y-m-d 
    params = {"date": date_str}
    
    try:
        # ส่งข้อความสรุปเบื้องต้น
        embed = [{
            "title": f"⚽ รายงานฟุตบอลประจำวันที่ {date_str}",
            "description": "บอทกำลังเริ่มติดตามผลบอลให้คุณแล้ว! ระบบจะรายงานผลอัตโนมัติทุก 30 นาที",
            "color": 5814783,
            "footer": {"text": f"อัปเดตล่าสุดเมื่อ: {now.strftime('%H:%M:%S')}"}
        }]
        send_discord_embed(embed)
        print("Successfully sent update to Discord")
        
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    get_football_data()
