import os
import sys
import json
import requests

from dotenv import load_dotenv

load_dotenv()

roblox_token = os.environ.get('ROBLOSECURITY')
user_id = os.environ.get('USERID')
exempt_games = os.environ.get('GAMES_EXEMPT').split(',')

if not roblox_token or not user_id:
    print('All environment variables must be entered.')

    sys.exit(1)

def main() -> None:
    s = requests.Session()

    cursor = ''
    page = 0
    badge_ids = []

    while True:
        r = s.get(f'https://badges.roblox.com/v1/users/{user_id}/badges?sortOrder=Desc&limit=100&cursor={cursor}')
        content = json.loads(r.text)
        data = content['data']
        cursor = content['nextPageCursor'] or None

        for badge in data:
            badge_data = {
                'id': badge['id'],
                'name': badge['name'],
                'gameID': badge['awarder']['id']
            }

            # Checks if the game the badge was awarded from is exempt from badge removal
            if not str(badge_data['gameID']) in exempt_games:
                badge_ids.append(badge_data)

        page += 1

        print(f'Scraped badges page #{page}. Approximate badges found: {(page * 100):,}.')

        if not cursor:
            break

    print(f'Total badges found: {len(badge_ids)}')

if __name__ == '__main__':
    main()