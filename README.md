# Roblox badge removal

### This script serves as an easy way to delete badges on your ROBLOX profile.

## Features:
- [x] Game exemption
- [x] Keyword exemption

## Installation
1. Clone the repo `git clone https://github.com/dieperdev/roblox-badge-removal.git`
2. Install requirements `pip install -r requirements.txt` or `pip3` on MacOS/Linux
3. Customize `.env.example` and rename it to `.env` (See [get your token](#get-your-token) and [.env customization](#env-customization))
4. Run the script `python main.py` or `python3` on MacOS/Linux

## Get your token

### See [this link](https://devforum.roblox.com/t/about-the-roblosecurity-cookie/2305393) on the devforum. This script is completely safe and **does not** send your cookie anywhere besides ROBLOX.

## .env Customization

1. Set `ROBLOSECURITY` to your ROBLOX cookie.
2. Set `USERID` to your ROBLOX User ID.
3. (Optional) Set `GAMES_EXEMPT` to the Game ID's of games exempt from badge removal (separated by commas). This can be left blank and no games will be exempt.
4. (Optional) Set `KEYWORDS_EXEMPT` to the keywords you want to be exempt from badge removal. If the name or description of a badge includes any of the words in the `KEYWORDS_EXEMPT` environment variable (separated by commas), it will be exempt from badge removal. This can be left blank and no keywords will be exempt.