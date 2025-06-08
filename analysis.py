# analysis.py
import json
import string
from collections import Counter

# 载入英文字母频率（示例数据）
ENGLISH_FREQ = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3,
    'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
    'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15, 'Q': 0.1,
    'Z': 0.07
}

def letter_frequency(text: str) -> dict:
    """
    统计文本中字母频率
    :param text: 输入文本
    :return: 字母频率字典
    """
    text = text.upper()
    letters_only = [ch for ch in text if ch in string.ascii_uppercase]
    total = len(letters_only)
    counts = Counter(letters_only)
    freq = {ch: counts.get(ch, 0) / total * 100 if total > 0 else 0 for ch in string.ascii_uppercase}
    return freq


def initial_key_guess(cipher_freq: dict) -> dict:
    """
    根据密文字母频率匹配英文频率，给出初步密钥猜测
    :param cipher_freq: 密文字母频率字典
    :return: 初步密钥映射，密文字母->明文字母
    """
    # 按频率排序
    cipher_sorted = sorted(cipher_freq.items(), key=lambda x: x[1], reverse=True)
    english_sorted = sorted(ENGLISH_FREQ.items(), key=lambda x: x[1], reverse=True)

    key_guess = {}
    for (c_letter, _), (e_letter, _) in zip(cipher_sorted, english_sorted):
        key_guess[c_letter] = e_letter
    return key_guess


def apply_partial_key(ciphertext: str, partial_key: dict) -> str:
    """
    根据部分密钥映射解密密文，未映射字母用下划线代替
    :param ciphertext: 密文
    :param partial_key: 密文字母->明文字母映射
    :return: 部分解密文本
    """
    result = []
    for ch in ciphertext:
        if ch.upper() in partial_key:
            mapped = partial_key[ch.upper()]
            result.append(mapped if ch.isupper() else mapped.lower())
        elif ch.isalpha():
            result.append('_')
        else:
            result.append(ch)
    return ''.join(result)
