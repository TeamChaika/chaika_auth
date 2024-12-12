from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse, HTMLResponse
import telegram

app = FastAPI()

TELEGRAM_BOT_TOKEN = '7529471166:AAG3R4Av0TAEVhMql4qIjo8wPCcibR_-XQ4'
TELEGRAM_BOT_USERNAME = 'chaika_auth_bot'
TELEGRAM_AUTH_URL = f'https://telegram.me/{TELEGRAM_BOT_USERNAME}?start=auth'
TELEGRAM_WEBHOOK_URL = f'https://127.0.0.1:8000/webhook'

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(url=TELEGRAM_WEBHOOK_URL)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Telegram Auth Web App"}

@app.get("/login")
def login():
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Form</title>
    </head>
    <body>
        <h1>Login with Telegram</h1>
        <form action="/auth" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <br>
            <button type="submit">Login</button>
        </form>
        <br>
        <a href="https://telegram.me/YOUR_TELEGRAM_BOT_USERNAME?start=auth">
            <button type="button">Login with Telegram</button>
        </a>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/auth")
async def auth(username: str = Form(...), password: str = Form(...)):
    # Здесь можно добавить логику для обработки авторизации
    return RedirectResponse(url="/redirect")

@app.get("/redirect")
def redirect_page():
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Redirect Page</title>
    </head>
    <body>
        <h1>Welcome, you are successfully authenticated!</h1>
        <p>Thank you for logging in via Telegram.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = telegram.Update.de_json(data, bot)
    if update.message:
        chat_id = update.message.chat.id
        text = update.message.text
        # Обработка сообщения от пользователя
        if text == "/start auth":
            await bot.send_message(chat_id=chat_id, text="Вы успешно авторизованы!")
    return {"status": "ok"}
