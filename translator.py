import translators


def translate_en2ru(text: str) -> str:
    my_translators_pool = ['deepl', 'yandex', 'bing', 'google'] + translators.translators_pool
    result = ''
    for translator in my_translators_pool:
        if result: return result
        try:
            result = translators.translate_text(text, translator, 'en', 'ru')
        except Exception as e:
            # TODO logging
            continue
    return result


def translate_list(array: list) -> list:
    for index in range(len(array)):
        array[index] = translate_en2ru(array[index])

    return array
