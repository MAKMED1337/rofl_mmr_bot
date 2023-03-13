# rofl_mmr_bot
Bot uses mysql, telethon
Mysql account username is `root_db` and database named `mmr_bot` (check `db_config.py`)

Firstly run:
```
pip install -r requirements.txt
```

Secondly setup enviorment variables:
1. `API_ID` - from https://my.telegram.org
2. `API_HASH` - from https://my.telegram.org
3. `TOKEN` - your telegram bot token from https://t.me/BotFather
4. `BOT_NAME` - your bot name(for example `rofl_mmr_bot`)
5. `db_pass` - password for your db account