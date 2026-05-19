from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_price_alert(email: str, coin_id: str, old_price: float, new_price:float):
    change = ((new_price-old_price)/old_price) * 100
    direction = "выросла" if change > 0 else "упала"
    
    message = MessageSchema(
        subject=f"Price Alert: {coin_id}",
        recipients=[email],
        body=f"{coin_id} {direction} на {abs(change):.2f}%! Старая цена ${old_price}, новая ${new_price}",
        subtype="plain"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)