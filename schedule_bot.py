import requests
import os
from datetime import datetime
import pytz

def send_to_discord(embeds):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if embeds:
        requests.post(webhook_url, json={"embeds": embeds})

def main():
    api_key = os.getenv('FOOTBALL_API_KEY')
    tz = pytz.timezone('Asia/Bangkok')
    today_dt = datetime.now(tz)
    date_str = today_dt.strftime('%Y-%m-%d')

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    # ถอดตัวแปร season ออก ค้นหาจากรหัสพรีเมียร์ลีก (39) และวันที่โดยตรง
    params = {"league": "39", "date": date_str}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        fixtures = data.get('response', [])
        
        match_list = []
        for match in fixtures:
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            # แปลงเวลาเริ่มแข่ง UTC เป็นเวลาไทย
            utc_time = datetime.strptime(match['fixture']['date'], "%Y-%m-%dT%H:%M:%S%z")
            local_time = utc_time.astimezone(tz).strftime('%H:%M')
            match_list.append(f"⏰ **{local_time}**: {home} vs {away}")

        if match_list:
            description = "\n".join(match_list)
        else:
            description = "วันนี้ไม่มีการแข่งขันพรีเมียร์ลีกครับ 🏴󠁧󠁢󠁥󠁮󠁧󠁿"

        embed = [{
            "title": f"📅 ตารางแข่งพรีเมียร์ลีกวันนี้ ({today_dt.strftime('%d/%m')})",
            "description": description,
            "color": 15844367,
            "footer": {"text": f"อัปเดตข้อมูลเมื่อ: {today_dt.strftime('%H:%M:%S')}"}
        }]
        
        send_to_discord(embed)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
