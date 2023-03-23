# rofl_mmr_bot
Source code of https://t.me/rofl_mmr_bot:
This bot has next commands:
1. `/mmr` - gives you random amount of points
2. `/top` - prints top by points in current group
3. `/top10` - same as `/top` but prints only top 10 participants

Bot uses Mysql and telethon

Firstly run:
```
pip install -r requirements.txt
```

Secondly setup enviorment variables:
1. `API_ID` - from https://my.telegram.org
2. `API_HASH` - from https://my.telegram.org
3. `TOKEN` - your telegram bot token from https://t.me/BotFather
4. `BOT_NAME` - your bot name(for example `rofl_mmr_bot`)
5. `db_username` - username for mysql
6. `db_password` - password for mysql
7. `host` - mysql host(by default `localhost`)
8. `port` - mysql port(by default `3306`)
9. `db_name` - mysql database name

Thirdly run:
```
python3 main.py
```