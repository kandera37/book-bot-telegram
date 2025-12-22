from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_buy_keyboard(pay_url: str) -> InlineKeyboardMarkup:
    """
    Create inline keyboard with a single 'Buy book' button.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить книгу 💳",
                    url=pay_url,
                )
            ]
        ]
    )
    return keyboard