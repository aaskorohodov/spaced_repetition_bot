class LexiconController:
    _lexicons: dict = {}
    _error_text = {
        'RU': 'Произошла ошибка!',
        'EN': 'Some error happened!'
    }
    _supported_languages = ['EN', 'RU']
    _possible_typos = {
        tuple(['Ru', 'ru', 'ру', 'Ру', 'РУ', 'RUS', 'Rus', 'rus', 'Russian']): 'RU',
        tuple(['En', 'en', 'ENG', 'Eng', 'english', 'English']): 'EN'
    }
    _default_language = 'EN'

    @staticmethod
    def set_lexicon(lexicon: dict) -> None:
        LexiconController._lexicons = lexicon

    @staticmethod
    def get_supported_languages() -> list[str]:
        return LexiconController._supported_languages

    @staticmethod
    def get_text(text_key: str, language: str | None = None) -> str:
        language = LexiconController._check_language(language)
        if text_key in LexiconController._lexicons:
            return LexiconController._get_text_for_language(language, text_key)
        return LexiconController._error_text[language]

    @staticmethod
    def get_text_for_keyboard_buttons(text_key: str, language: str | None) -> str | None:
        language = LexiconController._check_language(language)
        if text_key in LexiconController._lexicons:
            return LexiconController._get_text_for_language(language, text_key)
        return None

    @staticmethod
    def _check_language(language: str) -> str:
        if language in LexiconController._supported_languages:
            return language
        for typos, correct_language in LexiconController._possible_typos.items():
            if language in typos:
                return correct_language

        return LexiconController._default_language

    @staticmethod
    def _get_text_for_language(language: str, text_ket: str) -> str:
        texts: dict = LexiconController._lexicons.get(text_ket)
        text_for_requested_language = texts.get(language)
        return text_for_requested_language
