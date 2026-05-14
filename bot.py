import requests
import os
from datetime import datetime, timedelta
import pytz

def send_to_discord(embeds):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if embeds:
        requests.post(webhook_url, json={"embeds": embeds})

def get_matches(api_key, date_obj):
    # ปรับเป็นรูปแบบ YYYY-MM-DD เพื่อความแม่นยำของ API
    date_str = date_obj.strftime('%Y-%m-%d')
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
        return [e for e in events if e.get('tournament', {}).get('uniqueTournament', {}).get('id') == 17]
    except Exception as e:
        print(f"Error fetching for {date_str}: {e}")
        return []

def main():
    api_key = os.getenv('FOOTBALL_API_KEY')
    tz = pytz.timezone('Asia/Bangkok')
    today_dt = datetime.now(tz)
    yesterday_dt = today_dt - timedelta(days=1)

    # ดึงข้อมูล 2 วันกันพลาด
    matches_yesterday = get_matches(api_key, yesterday_dt)
    matches_today = get_matches(api_key, today_dt)
    
    all_matches = []
    
    # รวมผลเมื่อวาน
    for m in matches_yesterday:
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        h_score = m.get('homeScore', {}).get('current', 0)
        a_score = m.get('awayScore', {}).get('current', 0)
        status = m['status']['description']
        all_matches.append(f"⏪ **{yesterday_dt.strftime('%d/%m')}:** {home} {h_score}-{a_score} {away} ({status})")

    # รวมตารางวันนี้
    for m in matches_today:
        home = m['homeTeam']['name']
        away = m['awayTeam']['name']
        h_score = m.get('homeScore', {}).get('current', 0)
        a_score = m.get('awayScore', {}).get('current', 0)
        status = m['status']['description']
        all_matches.append(f"📅 **{today_dt.strftime('%d/%m')}:** {home} {h_score}-{a_score} {away} ({status})")

    if all_matches:
        description = "\n".join(all_matches)
    else:
        description = "ไม่พบรายการแข่งขันพรีเมียร์ลีกในช่วงวันนี้และเมื่อวานครับ 🏴󠁧󠁢󠁥󠁮󠁧󠁿"

    embed = [{
        "title": "🏆 รายงานผลบอลพรีเมียร์ลีก",
        "description": description,
        "color": 38143,
        "footer": {"text": f"อัปเดตล่าสุด: {today_dt.strftime('%H:%M:%S')}"}
    }]
    
    send_to_discord(embed)

if __name__ == "__main__":
    main()
