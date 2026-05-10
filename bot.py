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
    now = datetime.now(tz)
    date_str = now.strftime('%d/%m/%Y')

    # ดึงข้อมูลจาก SofaScore API
    url = "https://sofascore.p.rapidapi.com/matches/list-by-date"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "sofascore.p.rapidapi.com"
    }
    params = {"date": date_str}

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        
        matches = data.get('events', [])
        found_matches = []

        for event in matches:
            # รหัสลีก 17 คือ Premier League อังกฤษ
            league_id = event.get('tournament', {}).get('uniqueTournament', {}).get('id')
            
            if league_id == 17: 
                home_team = event['homeTeam']['name']
                away_team = event['awayTeam']['name']
                
                # ดึงสกอร์ (ถ้ายังไม่แข่งจะเป็น 0 หรือไม่มีค่า)
                home_score = event.get('homeScore', {}).get('current', 0)
                away_score = event.get('awayScore', {}).get('current', 0)
                
                # ดึงสถานะ เช่น FT (จบเกม), 75' (นาทีที่แข่ง), หรือเวลาเริ่มแข่ง
                status = event['status']['description']
                
                match_info = f"🏟️ **{home_team}** {home_score} - {away_score}  **{away_team}**\n> สถานะ: `{status}`"
                found_matches.append(match_info)

        if found_matches:
            description = "\n\n".join(found_matches)
        else:
            description = "วันนี้ไม่มีการแข่งขันพรีเมียร์ลีกครับ 🏴󠁧󠁢󠁥󠁮󠁧󠁿"

        embed = [{
            "title": "🏆 รายงานผลบอลพรีเมียร์ลีกอังกฤษ",
            "description": description,
            "color": 38143, # สีม่วงเข้มสไตล์พรีเมียร์ลีก
            "footer": {"text": f"อัปเดตล่าสุด: {now.strftime('%H:%M:%S')} (เวลาไทย)"},
            "thumbnail": {"url": "https://www.premierleague.com/resources/rebrand/v7.129.0/i/elements/pl-main-logo.png"}
        }]
        
        send_to_discord(embed)

    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    main()
