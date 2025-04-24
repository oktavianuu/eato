import os
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Order, MenuItem

# Load environment variables from .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
    raise ValueError("Missing TELEGRAM_TOKEN or TELEGRAM_CHAT_ID in .env")

# Initialize the Telegram Bot
bot = Bot(token=TELEGRAM_TOKEN)


def send_order_alert(order_id: int):
    """
    Fetch order details and send a Telegram alert to staff.

    1. Open a DB session
    2. Query the Order and its items
    3. Build a user-friendly message
    4. Send via Telegram
    5. Close the session
    """
    db: Session = SessionLocal()
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            return

        # Construct message lines
        lines = [
            f"📣 *New Order Alert!* Order #{order.id}",
            f"👤 Customer: {order.customer_name or 'Guest'}",
            f"🍽️ Table: {order.table_number or 'N/A'}",
            "🧾 Items:"
        ]
        # Append each ordered item
        for item in order.items:
            menu_item = db.query(MenuItem).filter(MenuItem.id == item.menu_item_id).first()
            lines.append(f"- {menu_item.name} x {item.quantity}")

        # Join into a single message
        message = "\n".join(lines)

        # Send the message (Markdown for formatting)
        bot.send_message(
            chat_id=int(TELEGRAM_CHAT_ID),
            text=message,
            parse_mode="Markdown"
        )
    except TelegramError as e:
        print(f"Error sending Telegram message: {e}")
    finally:
        db.close()

# Dependencies:
# pip install python-telegram-bot python-dotenv
# Add TELEGRAM_TOKEN and TELEGRAM_CHAT_ID to .env
# Hook send_order_alert into order creation endpoint using BackgroundTasks
