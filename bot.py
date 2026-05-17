import requests
import os
from datetime import datetime, timedelta
import pytz

def send_to_discord(embeds):
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    if embeds:
        requests.post(webhook_url, json={"embeds": embeds})

def get_league_matches(api_key, date_str):
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
        return data.get('response', [])
    except:
        return []

def main():
    api_key = os.getenv('FOOTBALL_API_KEY')
    tz = pytz.timezone('Asia/Bangkok')
    today_dt = datetime.now(tz)
    yesterday_dt = today_dt - timedelta(days=1)

    yesterday_str = yesterday_dt.strftime('%Y-%m-%d')
    today_str = today_dt.strftime('%Y-%m-%d')

    matches_yesterday = get_league_matches(api_key, yesterday_str)
    matches_today = get_league_matches(api_key, today_str)
    
    all_matches = []
    
    # สรุปผลเมื่อวาน
    for match in matches_yesterday:
        teams = match['teams']
        goals = match['goals']
        status = match['fixture']['status']['short']
        home_g = goals['home'] if goals['home'] is not None else 0
        away_g = goals['away'] if goals['away'] is not None else 0
        all_matches.append(f"⏪ **{yesterday_dt.strftime('%d/%m')}:** {teams['home']['name']} {home_g}-{away_g} {teams['away']['name']} ({status})")

    # สรุปผล/สถานะวันนี้
    for match in matches_today:
        teams = match['teams']
        goals = match['goals']
        status = match['fixture']['status']['short']
        home_g = goals['home'] if goals['home'] is not None else 0
        away_g = goals['away'] if goals['away'] is not None else 0
        all_matches.append(f"📅 **{today_dt.strftime('%d/%m')}:** {teams['home']['name']} {home_g}-{away_g} {teams['away']['name']} ({status})")

    if all_matches:
        description = "\n".join(all_matches)
    else:
        description = "วันนี้และเมื่อวานไม่มีการแข่งขันพรีเมียร์ลีกครับ 🏴󠁧󠁢󠁥󠁮󠁧󠁿"

    embed = [{
        "title": "🏆 รายงานผลบอลพรีเมียร์ลีกอังกฤษ",
        "description": description,
        "color": 38143,
        "footer": {"text": f"อัปเดตล่าสุด: {today_dt.strftime('%H:%M:%S')}"}
    }]
    
    send_to_discord(embed)

if __name__ == "__main__":
    main()
