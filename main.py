import os
import sys
import json
import requests

from dotenv import load_dotenv

load_dotenv()

roblox_token = os.environ.get('ROBLOSECURITY')
user_id = os.environ.get('USERID')
exempt_games = os.environ.get('GAMES_EXEMPT').split(',')
exempt_keywords = os.environ.get('KEYWORDS_EXEMPT').split(',')

if not roblox_token or not user_id:
    print('All environment variables must be entered.')

    sys.exit(1)

def main() -> None:
    s = requests.Session()
    # Set roblosecurity token
    s.cookies['.ROBLOSECURITY'] = roblox_token

    # Add CSRF token to actually make the request work. The old method is outdated: https://stackoverflow.com/a/69855008 .
    header = s.post('https://catalog.roblox.com/v1/topic/get-topics')
    s.headers['X-CSRF-TOKEN'] = header.headers['X-CSRF-TOKEN']

    cursor = ''
    page = 0
    badge_ids = []

    while True:
        r = s.get(f'https://badges.roblox.com/v1/users/{user_id}/badges?sortOrder=Desc&limit=100&cursor={cursor}')
        content = json.loads(r.text)
        data = content['data']
        cursor = content['nextPageCursor'] or None

        for badge in data:
            found_match = False

            badge_data = {
                'id': badge['id'],
                'name': badge['name'],
                'description': badge['description'],
                'gameID': badge['awarder']['id']
            }

            # Checks if the game the badge was awarded from is exempt from badge removal
            if str(badge_data['gameID']) in exempt_games:
                print(f'Badge ID #{badge_data['id']} was exempt from badge removal.')

                continue

            # Checks if the name or description of the badge is exempt from badge removal based on keywords
            for word in exempt_keywords:
                if word.lower() in badge_data['name'].lower() or word.lower() in badge_data['description'].lower():
                    # Exit loop early because checking other words isn't needed
                    found_match = True

                    break

            if found_match:
                print(f'Badge ID #{badge_data['id']} was exempt from badge removal.')

                continue

            badge_ids.append(badge_data)

        page += 1

        print(f'Scraped badges page #{page}. Approximate badges found: {(page * 100):,}.')

        if not cursor:
            break

    total_badges = len(badge_ids)
    deleted_badges_count = 0

    print(f'Total badges found: {total_badges}')
    print('Deleting badges...')

    for badge in badge_ids:
        badge_id = badge['id']

        r = s.delete(f'https://badges.roblox.com/v1/user/badges/{badge_id}')

        if r.status_code == 200:
            deleted_badges_count += 1

            print(f'Deleted Badge ID #{badge_id}. Total badges deleted: {deleted_badges_count}. {(total_badges - deleted_badges_count):,} badges remain.')
        else:
            print(f'Something went wrong deleting Badge ID #{badge_id}. Open a github issue and include json content of the request above.')

    print(f'Deleted badges. {total_badges - deleted_badges_count} badges remain.')

if __name__ == '__main__':
    main()