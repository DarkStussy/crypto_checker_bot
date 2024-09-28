from decimal import Decimal

from crypto_checker.core.models import dto


def get_tracking_bar_message(percent: Decimal, pairs: list[dto.CryptoPair]):
    return (
        f"<b>Tracking bar</b>:\n<b>Percentage Change:</b> {percent.normalize():g}%\n"
        f"<b>Current tracking pairs:</b>\n<i>{', '.join([pair.name for pair in pairs]) or '-'}</i>"
    )


def get_prices_changes_message(user_pairs: list[dto.CryptoPair], binance_pairs: dict[str, Decimal]) -> str:
    pairs_info = []
    for pair in user_pairs:
        if (current_price := binance_pairs.get(pair.name)) is not None:
            pairs_info.append(
                f"<b>{pair.name}:</b>\nLast request: <i>{pair.price.normalize():f}</i>\n"
                f"Now: <i>{current_price:f}</i>\nDifference: <i>{(current_price - pair.price).normalize():f} "
                f"({round(100.0 - float(pair.price * 100 / current_price), 2)}%)</i>"
            )

    return "\n\n".join(pairs_info)
