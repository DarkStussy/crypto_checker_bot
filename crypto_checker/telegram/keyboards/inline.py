from typing import Final

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

INLINE_TRACK_PRICES_BTN: Final[InlineKeyboardButton] = InlineKeyboardButton(
    text="📈 Track prices", callback_data="track_prices"
)
INLINE_GET_PRICE_BTN: Final[InlineKeyboardButton] = InlineKeyboardButton(text="✨ Get price", callback_data="get_price")

INLINE_HIDE_BTN: Final[InlineKeyboardButton] = InlineKeyboardButton(text="🗙 Hide", callback_data="hide")
INLINE_HIDE_KB: Final[InlineKeyboardMarkup] = InlineKeyboardMarkup(inline_keyboard=[[INLINE_HIDE_BTN]])

INLINE_MENU_KB: Final[InlineKeyboardMarkup] = InlineKeyboardMarkup(
    inline_keyboard=[[INLINE_TRACK_PRICES_BTN], [INLINE_GET_PRICE_BTN], [INLINE_HIDE_BTN]]
)

INLINE_BACK_TO_MENU_BTN: Final[InlineKeyboardButton] = InlineKeyboardButton(
    text="🔙 Back", callback_data="back_to_menu"
)
INLINE_BACK_TO_MENU_KB: Final[InlineKeyboardMarkup] = InlineKeyboardMarkup(inline_keyboard=[[INLINE_BACK_TO_MENU_BTN]])

INLINE_TRACK_PRICES_KB: Final[InlineKeyboardMarkup] = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Add pair", callback_data="add_pair"),
            InlineKeyboardButton(text="➖ Remove pair", callback_data="remove_pair"),
        ],
        [InlineKeyboardButton(text="% Change percentage", callback_data="change_percent")],
        [INLINE_BACK_TO_MENU_BTN],
    ]
)
INLINE_BACK_TO_TRACK_PRICES_KB: Final[InlineKeyboardMarkup] = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="🔙 Back", callback_data="back_to_track_prices")]]
)
