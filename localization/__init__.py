import locale
from .strings import STRINGS

def detect_language():
    try:
        lang, _ = locale.getdefaultlocale()
        if lang and lang.startswith("zh"):
            return "zh"
    except:
        pass
    return "en"

_LANGUAGE = detect_language()

def set_language(lang):
    global _LANGUAGE
    if lang in ("zh", "en"):
        _LANGUAGE = lang

def tr(key, *args):
    s = STRINGS.get(_LANGUAGE, {}).get(key, key)
    if args:
        s = s.format(*args)
    return s
