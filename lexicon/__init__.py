from lexicon.commands.start import START_LEXICON
from lexicon.lexicon_controller import LexiconController
from lexicon.menus.main_menu import MAIN_MENU_LEXICON


def set_lexicon():
    registered_lexicons = [
        START_LEXICON,
        MAIN_MENU_LEXICON
    ]
    all_lexicons = {}

    for lexicon in registered_lexicons:
        for text_key, texts in lexicon.items():
            check_key_is_unique(text_key, all_lexicons)
            all_lexicons[text_key] = texts

    LexiconController.set_lexicon(all_lexicons)


def check_key_is_unique(text_key: str, all_lexicons: dict) -> None:
    if text_key in all_lexicons:
        raise AssertionError(f'There is the same key "{text_key}" found in several lexicons! Change it to something '
                             f'unique please, before launching this application.')
