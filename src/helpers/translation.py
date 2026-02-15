"""Helpers for localized Product/Category content."""

from fastapi import Header


SUPPORTED = frozenset({"ru", "kk"})
DEFAULT_LOCALE = "ru"


def localized(obj, field: str, locale: str, default_locale: str = "ru"):
    locale = locale if locale in SUPPORTED else default_locale

    localized_value = getattr(obj, f"{field}_{locale}", None)
    if localized_value:
        return localized_value

    fallback_value = getattr(obj, f"{field}_{default_locale}", None)
    if fallback_value:
        return fallback_value

    return getattr(obj, field)


def get_locale(
    accept_language: str | None = Header(None, alias="Accept-Language"),
) -> str:
    if not accept_language:
        return DEFAULT_LOCALE
    for part in accept_language.replace(" ", "").split(","):
        lang = part.split(";")[0].split("-")[0].lower()
        if lang in SUPPORTED:
            return lang
    return DEFAULT_LOCALE