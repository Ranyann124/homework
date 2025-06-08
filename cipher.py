# cipher.py

def encrypt(plaintext: str, key_map: dict) -> str:
    """
    单表代换加密
    :param plaintext: 明文字符串
    :param key_map: 字母映射字典，如 {'A':'Q', 'B':'W', ...}
    :return: 密文字符串
    """
    ciphertext = []
    for ch in plaintext:
        if ch.isalpha():
            is_upper = ch.isupper()
            mapped = key_map.get(ch.upper(), ch.upper())
            ciphertext.append(mapped if is_upper else mapped.lower())
        else:
            ciphertext.append(ch)
    return ''.join(ciphertext)


def decrypt(ciphertext: str, key_map: dict) -> str:
    """
    单表代换解密
    :param ciphertext: 密文字符串
    :param key_map: 字母映射字典，如 {'A':'Q', 'B':'W', ...}
    :return: 明文字符串
    """
    # 反转映射
    reverse_map = {v: k for k, v in key_map.items()}
    plaintext = []
    for ch in ciphertext:
        if ch.isalpha():
            is_upper = ch.isupper()
            mapped = reverse_map.get(ch.upper(), ch.upper())
            plaintext.append(mapped if is_upper else mapped.lower())
        else:
            plaintext.append(ch)
    return ''.join(plaintext)
