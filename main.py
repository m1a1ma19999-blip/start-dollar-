
import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text(
        f"مرحبًا بك في Start Dollar!\n\n"
        f"Telegram ID الخاص بك هو:\n`{user.id}`\n\n"
        "يمكنك إرسال Binance ID الخاص بك هنا للمراجعة.\n"
        "أرسل /start للعودة إلى هذه القائمة.",
        parse_mode="Markdown",
    )


async def receive_binance_id(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user
    binance_id = update.message.text.strip()

    if len(binance_id) > 100:
        await update.message.reply_text("الـ ID طويل جدًا. أعد المحاولة.")
        return

    if not ADMIN_ID:
        await update.message.reply_text(
            "تم استلام رسالتك، لكن الإدارة لم تُضبط بعد."
        )
        return

    try:
        await context.bot.send_message(
            chat_id=int(ADMIN_ID),
            text=(
                "طلب مراجعة Binance ID\n"
                f"اسم المستخدم: @{user.username or 'لا يوجد'}\n"
                f"Telegram ID: {user.id}\n"
                f"Binance ID المرسل: {binance_id}"
            ),
        )
        await update.message.reply_text(
            "تم إرسال الـ ID إلى الإدارة للمراجعة."
        )
    except Exception:
        logging.exception("Could not notify admin")
        await update.message.reply_text(
            "تعذر إرسال الطلب. حاول لاحقًا."
        )


def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, receive_binance_id)
    )
    app.run_polling()


if __name__ == "__main__":
    main()
