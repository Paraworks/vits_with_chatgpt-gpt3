import re
from text.english import english_to_lazy_ipa, english_to_ipa2, english_to_lazy_ipa2
from text.japanese import clean_japanese, japanese_to_romaji_with_accent, japanese_to_ipa, japanese_to_ipa2, japanese_to_ipa3
from text.mandarin import number_to_chinese, chinese_to_bopomofo, latin_to_bopomofo, chinese_to_romaji, chinese_to_lazy_ipa, chinese_to_ipa, chinese_to_ipa2

def none_cleaner(text):
    return text

def japanese_cleaners(text):
    text = clean_japanese(text)
    text = re.sub(r'([A-Za-z])$', r'\1.', text)
    return text

def japanese_cleaners2(text):
    return japanese_cleaners(text).replace('ts', 'ʦ').replace('...', '…')

def chinese_cleaners(text):
    '''Pipeline for Chinese text'''
    text = number_to_chinese(text)
    text = chinese_to_bopomofo(text)
    text = latin_to_bopomofo(text)
    if re.match('[ˉˊˇˋ˙]', text[-1]):
        text += '。'
    return text

def zh_ja_mixture_cleaners(text):
    chinese_texts = re.findall(r'\[ZH\].*?\[ZH\]', text)
    japanese_texts = re.findall(r'\[JA\].*?\[JA\]', text)
    for chinese_text in chinese_texts:
        cleaned_text = chinese_to_romaji(chinese_text[4:-4])
        text = text.replace(chinese_text, cleaned_text+' ', 1)
    for japanese_text in japanese_texts:
        cleaned_text = japanese_to_romaji_with_accent(
            japanese_text[4:-4]).replace('ts', 'ʦ').replace('u', 'ɯ').replace('...', '…')
        text = text.replace(japanese_text, cleaned_text+' ', 1)
    text = text[:-1]
    if re.match('[A-Za-zɯɹəɥ→↓↑]', text[-1]):
        text += '.'
    return text

def cjke_cleaners(text):
    chinese_texts = re.findall(r'\[ZH\].*?\[ZH\]', text)
    japanese_texts = re.findall(r'\[JA\].*?\[JA\]', text)
    english_texts = re.findall(r'\[EN\].*?\[EN\]', text)
    for chinese_text in chinese_texts:
        cleaned_text = chinese_to_lazy_ipa(chinese_text[4:-4])
        cleaned_text = cleaned_text.replace(
            'ʧ', 'tʃ').replace('ʦ', 'ts').replace('ɥan', 'ɥæn')
        text = text.replace(chinese_text, cleaned_text+' ', 1)
    for japanese_text in japanese_texts:
        cleaned_text = clean_japanese(japanese_text[4:-4])
        cleaned_text = cleaned_text.replace('ʧ', 'tʃ').replace(
            'ʦ', 'ts').replace('ɥan', 'ɥæn').replace('ʥ', 'dz')
        text = text.replace(japanese_text, cleaned_text+' ', 1)
    for english_text in english_texts:
        cleaned_text = english_to_ipa2(english_text[4:-4])
        cleaned_text = cleaned_text.replace('ɑ', 'a').replace(
            'ɔ', 'o').replace('ɛ', 'e').replace('ɪ', 'i').replace('ʊ', 'u')
        text = text.replace(english_text, cleaned_text+' ', 1)
    text = text[:-1]
    if re.match(r'[^\.,!\?\-…~]', text[-1]):
        text += '.'
    return text