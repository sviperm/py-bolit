# py-bolit

## Pre Requirements

1. Install [Ngrok](https://ngrok.com/) and run it
2. Create Telegram bot via [@BotFather](https://t.me/botfather) and get API-key (or use existing bot)

## Intallation

1. Copy `.env.example` to `.env`
2. Change `TG_API_URL` with your bot API-key
3. Change `BOT_WEBHOOK` with ngrok tunnel-url
4. Change `SECRET_KEY` for Django.
5. Install all dependencies:
    ```shell
    pip install -r requirements.txt
    ```

## Run
```shell
python manage.py runserver
```
