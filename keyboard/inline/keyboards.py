from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_tracking_button = InlineKeyboardButton('Track prices', callback_data='track_prices')
inline_btn_check_price = InlineKeyboardButton('Get price', callback_data='get_price')
inline_btn_close = InlineKeyboardButton('Close', callback_data='close')
inline_kb_menu = InlineKeyboardMarkup().add(inline_tracking_button).add(inline_btn_check_price).add(inline_btn_close)

inline_kb_close = InlineKeyboardMarkup().add(inline_btn_close)

inline_add_pair = InlineKeyboardButton('Add pair', callback_data='add_pair')
inline_remove_pair = InlineKeyboardButton('Remove pair', callback_data='remove_pair')
inline_change_percent = InlineKeyboardButton('Change percentage for alert', callback_data='change_percent')
inline_kb_track_prices = InlineKeyboardMarkup().add(inline_add_pair, inline_remove_pair) \
    .add(inline_change_percent).add(inline_btn_close)
