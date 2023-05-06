import re
import re
from unidecode import unidecode
from unidecode import unidecode
import ctypes
from text.mandarin import number_to_chinese, chinese_to_bopomofo, latin_to_bopomofo, chinese_to_romaji, chinese_to_lazy_ipa, chinese_to_ipa, chinese_to_ipa2
try:
    dll = ctypes.cdll.LoadLibrary('cleaners/JapaneseCleaner.dll')
    dll.CreateOjt.restype = ctypes.c_uint64 
    dll.PluginMain.restype = ctypes.c_uint64 
    floder = ctypes.create_unicode_buffer("cleaners")
    dll.CreateOjt(floder)
except:
    pass
def clean_japanese(text):
    input_wchar_pointer = ctypes.create_unicode_buffer(text)
    result = ctypes.wstring_at(dll.PluginMain(input_wchar_pointer))
    return result

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
        cleaned_text = japanese_cleaners(
            japanese_text[4:-4]).replace('ts', 'ʦ').replace('u', 'ɯ').replace('...', '…')
        text = text.replace(japanese_text, cleaned_text+' ', 1)
    text = text[:-1]
    if re.match('[A-Za-zɯɹəɥ→↓↑]', text[-1]):
        text += '.'
    return text

def cjke_cleaners(text):
    chinese_texts = re.findall(r'\[ZH\].*?\[ZH\]', text)
    japanese_texts = re.findall(r'\[JA\].*?\[JA\]', text)
    for chinese_text in chinese_texts:
        cleaned_text = chinese_to_lazy_ipa(chinese_text[4:-4])
        cleaned_text = cleaned_text.replace(
            'ʧ', 'tʃ').replace('ʦ', 'ts').replace('ɥan', 'ɥæn')
        text = text.replace(chinese_text, cleaned_text+' ', 1)
    for japanese_text in japanese_texts:
        cleaned_text = japanese_cleaners(japanese_text[4:-4])
        text = text.replace(japanese_text, cleaned_text+' ', 1)
    text = text[:-1]
    if re.match(r'[^\.,!\?\-…~]', text[-1]):
        text += '.'
    return text

def cjks_cleaners(text):
    chinese_texts = re.findall(r'\[ZH\].*?\[ZH\]', text)
    japanese_texts = re.findall(r'\[JA\].*?\[JA\]', text)
    for chinese_text in chinese_texts:
        cleaned_text = chinese_to_lazy_ipa(chinese_text[4:-4])
        text = text.replace(chinese_text, cleaned_text+' ', 1)
    for japanese_text in japanese_texts:
        cleaned_text = japanese_cleaners(japanese_text[4:-4])
        text = text.replace(japanese_text, cleaned_text+' ', 1)
    text = text[:-1]
    if re.match(r'[^\.,!\?\-…~]', text[-1]):
        text += '.'
    return text

def cjke_cleaners2(text):
    chinese_texts = re.findall(r'\[ZH\].*?\[ZH\]', text)
    japanese_texts = re.findall(r'\[JA\].*?\[JA\]', text)
    for chinese_text in chinese_texts:
        cleaned_text = chinese_to_lazy_ipa(chinese_text[4:-4])
        text = text.replace(chinese_text, cleaned_text+' ', 1)
    for japanese_text in japanese_texts:
        cleaned_text = japanese_cleaners(japanese_text[4:-4])
        text = text.replace(japanese_text, cleaned_text+' ', 1)
    text = text[:-1]
    if re.match(r'[^\.,!\?\-…~]', text[-1]):
        text += '.'
    return text
