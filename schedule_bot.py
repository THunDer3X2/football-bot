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
    # ใช้รูปแบบ YYYY-MM-DD เพื่อความแม่นยำของ API
    date_str = today_dt.strftime('%Y-%m-%d')

    url = "https://sofascore.p.rapidapi.com/matches/list-by-date"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    params = {"date": date_str}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        events = data.get('events', [])
        
        # กรองเฉพาะ Premier League อังกฤษ (ID: 17)
        pl_matches = [e for e in events if e.get('tournament', {}).get('uniqueTournament', {}).get('id') == 17]
        
        match_list = []
        for m in pl_matches:
            home = m['homeTeam']['name']
            away = m['awayTeam']['name']
            # แปลงเวลาเริ่มแข่งเป็นเวลาไทย
            start_time = datetime.fromtimestamp(m['startTimestamp'], tz).strftime('%H:%M')
            match_list.append(f"⏰ **{start_time}**: {home} vs {away}")

        if match_list:
            description = "\n".join(match_list)
        else:
            description = "วันนี้ไม่มีการแข่งขันพรีเมียร์ลีกครับ 🏴󠁧󠁢󠁥󠁮󠁧󠁿"

        embed = [{
            "title": f"📅 ตารางแข่งพรีเมียร์ลีกวันนี้ ({today_dt.strftime('%d/%m')})",
            "description": description,
            "color": 15844367, # สีทอง
            "footer": {"text": f"อัปเดตข้อมูลเมื่อ: {today_dt.strftime('%H:%M:%S')}"}
        }]
        
        send_to_discord(embed)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
