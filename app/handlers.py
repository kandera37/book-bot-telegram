import logging
import html

from pathlib import Path

from aiogram import types
from aiogram.filters import Command
from aiogram import Router
from aiogram.types import FSInputFile

from app.keyboards import get_buy_keyboard
from app.config import (
    BOOK_FILE_PATH,
    IMAGES_DIR,
    ADMIN_IDS
)
from app.services.payments import (
    mark_user_paid,
    is_paid_user,
    create_payment_link,
    get_all_paid_users
)
from app.services.crm import upset_user, get_all_users

logger = logging.getLogger(__name__)

router = Router()

def get_intro_image_paths() -> list[Path]:
    """
    Return a sorted list of intro image paths from IMAGES_DIR.
    Only jpg / jpeg / png files are included.
    """
    if not IMAGES_DIR.exists():
        return []
    # Sort files and filter buy suffix
    image_paths = [
        p for p in IMAGES_DIR.iterdir()
        if p.is_file() and p.suffix.lower() in (".jpg", ".jpeg", ".png")
    ]

    # Sort by name of file
    image_paths.sort(key=lambda p: p.name)
    return image_paths

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    """
    Handle /start command:
    - send intro image (if exists)
    - send book description with a Buy button
    """
    user_id = message.from_user.id
    user = message.from_user
    upset_user(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    logger.info("User %s called /start", message.from_user.id)

    # 1. Trying sent first image, if it exists
    image_paths = get_intro_image_paths()
    if image_paths:
        first_image_path = image_paths[0]
        photo = FSInputFile(path=str(first_image_path))
        await message.answer_photo(
            photo,
            caption="Спасибо, что зашли в бот 🙌",
        )

    text = (
        "Здесь можно купить книгу в PDF.\n"
        "Нажми на кнопку ниже, чтобы перейти к оплате."
    )

    pay_link = create_payment_link(user.id)


    await message.answer(
        text,
        reply_markup=get_buy_keyboard(pay_link),
    )

@router.message(Command("get_book"))
async def cmd_get_book(message: types.Message):
    """
    Send the book file to the user as a document.
    """
    user_id = message.from_user.id
    logger.info("User %s called /get_book", user_id)

    if not is_paid_user(user_id):
        logger.info("User %s called /get_book without payment", user_id)
        await message.answer(
            "Похоже, вы ещё не оплатили книгу. "
            "Сначала оплатите по кнопке / через /start, потом отправьте команду /i_paid"
        )
        return
    book = FSInputFile(path=str(BOOK_FILE_PATH), filename="Книга про добро.pdf")
    logger.info("Book set to user %s", user_id)

    await message.answer_document(
        document=book,
        caption="Вот ваша книга 📕"
    )

@router.message(Command("i_paid"))
async def cmd_i_paid(message: types.Message):
    """
    Mark the user as paid after they complete payment.
    """
    user = message.from_user
    mark_user_paid(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,)
    logger.info("User %s marked as paid", user.id)

    await message.answer(
        "Спасибо, оплата отмечена. Теперь вы можете получить книгу по команде /get_book"
    )

@router.message(Command("buyers"))
async def cmd_buyers(message: types.Message):
    """
    Show list of buyers (for admins only).
    Each buyer is shown as a clickable link with their name.
    """
    user_id = message.from_user.id

    # Only for admins
    if user_id not in ADMIN_IDS:
        return

    users = get_all_paid_users()

    if not users:
        await message.answer("Покупателей пока нет.")
        return

    lines: list[str] = []

    for u in users:
        uid = u["user_id"]
        username = u["username"]
        first_name = u["first_name"]
        last_name = u["last_name"]

        # Build a shown name
        if first_name or last_name:
            display_name = " ".join(
                part for part in [first_name, last_name] if part
            )
        elif username:
            display_name = f"@{username}"
        else:
            display_name = f"User {uid}"

        display_name = html.escape(display_name)

        if username:
            href = f"https://t.me/{username}"
        else:
            href = f"tg://user?id={uid}"

        line = f' - <a href="{href}">{display_name}</a>'
        lines.append(line)

    text = "Покупатели \n" + "\n".join(lines)

    await message.answer(
        text,
        parse_mode="html",
        disable_web_page_preview=True,
    )

@router.message(Command("broadcast"))
async def cmd_broadcast(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return

    text = "Пока текст-затычка"

    users = get_all_users()
    for uid in users:
        try:
            await message.bot.send_message(chat_id=uid, text=text)
        except Exception as e:
            logger.warning("Failed to send message to %s: %s", uid, e)