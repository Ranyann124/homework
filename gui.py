# gui.py
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QTextEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox)
from cipher import encrypt, decrypt
from analysis import letter_frequency, initial_key_guess, apply_partial_key

class SubstitutionCipherGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("单表代换密码辅助工具")
        self.resize(800, 600)
        self.key_map = {chr(i): chr(i) for i in range(65, 91)}  # 初始为身份映射

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 明文输入
        self.plaintext_edit = QTextEdit()
        self.plaintext_edit.setPlaceholderText("请输入明文")
        layout.addWidget(QLabel("明文输入"))
        layout.addWidget(self.plaintext_edit)

        # 密钥输入（26个字母映射，按A-Z顺序）
        self.key_input = QLineEdit("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        layout.addWidget(QLabel("密钥映射（26个字母，A对应的替换字母依次输入）"))
        layout.addWidget(self.key_input)

        # 加密按钮
        btn_encrypt = QPushButton("加密")
        btn_encrypt.clicked.connect(self.do_encrypt)
        # 解密按钮
        btn_decrypt = QPushButton("解密")
        btn_decrypt.clicked.connect(self.do_decrypt)

        h_layout = QHBoxLayout()
        h_layout.addWidget(btn_encrypt)
        h_layout.addWidget(btn_decrypt)
        layout.addLayout(h_layout)

        # 密文输出
        self.ciphertext_edit = QTextEdit()
        self.ciphertext_edit.setPlaceholderText("密文显示区")
        layout.addWidget(QLabel("密文输出"))
        layout.addWidget(self.ciphertext_edit)

        # 破译辅助部分
        layout.addWidget(QLabel("破译辅助（输入密文，点击分析）"))
        self.ciphertext_input = QTextEdit()
        self.ciphertext_input.setPlaceholderText("请输入密文进行破译分析")
        layout.addWidget(self.ciphertext_input)

        btn_analyze = QPushButton("分析频率并给出初步密钥")
        btn_analyze.clicked.connect(self.analyze_ciphertext)
        layout.addWidget(btn_analyze)

        self.analysis_result = QTextEdit()
        self.analysis_result.setReadOnly(True)
        layout.addWidget(QLabel("破译建议和部分解密结果"))
        layout.addWidget(self.analysis_result)

        # 用户输入部分密钥映射（格式：密文字母=明文字母，逗号分隔）
        layout.addWidget(QLabel("手动指定部分密钥映射（格式：C=E,T=A,...）"))
        self.partial_key_input = QLineEdit()
        layout.addWidget(self.partial_key_input)

        btn_update_key = QPushButton("更新密钥并显示解密结果")
        btn_update_key.clicked.connect(self.update_partial_key)
        layout.addWidget(btn_update_key)

        self.setLayout(layout)

    def do_encrypt(self):
        plaintext = self.plaintext_edit.toPlainText()
        key_str = self.key_input.text().upper()
        if len(key_str) != 26 or not key_str.isalpha():
            QMessageBox.warning(self, "错误", "密钥必须是26个字母")
            return
        key_map = {chr(65 + i): key_str[i] for i in range(26)}
        ciphertext = encrypt(plaintext, key_map)
        self.ciphertext_edit.setPlainText(ciphertext)

    def do_decrypt(self):
        ciphertext = self.ciphertext_edit.toPlainText()
        key_str = self.key_input.text().upper()
        if len(key_str) != 26 or not key_str.isalpha():
            QMessageBox.warning(self, "错误", "密钥必须是26个字母")
            return
        key_map = {chr(65 + i): key_str[i] for i in range(26)}
        plaintext = decrypt(ciphertext, key_map)
        self.plaintext_edit.setPlainText(plaintext)

    def analyze_ciphertext(self):
        ciphertext = self.ciphertext_input.toPlainText()
        freq = letter_frequency(ciphertext)
        guess = initial_key_guess(freq)
        # 显示频率
        freq_str = "字母频率统计:\n"
        for ch in sorted(freq.keys()):
            freq_str += f"{ch}: {freq[ch]:.2f}%  "
        freq_str += "\n\n初步密钥猜测（密文字母->明文字母）:\n"
        freq_str += ', '.join([f"{k}->{v}" for k, v in guess.items()])
        # 部分解密结果
        partial_decrypt = apply_partial_key(ciphertext, guess)
        freq_str += "\n\n部分解密结果:\n" + partial_decrypt
        self.analysis_result.setPlainText(freq_str)
        self.current_guess = guess  # 保存当前猜测

    def update_partial_key(self):
        user_input = self.partial_key_input.text().upper()
        if not hasattr(self, 'current_guess'):
            QMessageBox.warning(self, "错误", "请先点击分析按钮获得初步密钥")
            return
        # 解析用户输入
        try:
            pairs = user_input.split(',')
            for pair in pairs:
                if '=' in pair:
                    c_letter, p_letter = pair.split('=')
                    c_letter = c_letter.strip()
                    p_letter = p_letter.strip()
                    if len(c_letter) == 1 and len(p_letter) == 1 and c_letter.isalpha() and p_letter.isalpha():
                        self.current_guess[c_letter] = p_letter
            # 更新显示部分解密结果
            ciphertext = self.ciphertext_input.toPlainText()
            partial_decrypt = apply_partial_key(ciphertext, self.current_guess)
            self.analysis_result.setPlainText("更新后的部分解密结果:\n" + partial_decrypt)
        except Exception as e:
            QMessageBox.warning(self, "错误", f"输入格式错误: {e}")
