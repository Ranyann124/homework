import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QTextEdit, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt

# 导入你写的cipher模块
from cipher import encrypt, decrypt

class CipherTool(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        # 这里定义一个简单的示例替换表，可以根据需要修改
        self.key_map = {
            'a': 'm', 'b': 'n', 'c': 'b', 'd': 'v', 'e': 'c',
            'f': 'x', 'g': 'z', 'h': 'l', 'i': 'k', 'j': 'j',
            'k': 'h', 'l': 'g', 'm': 'f', 'n': 'd', 'o': 's',
            'p': 'a', 'q': 'p', 'r': 'o', 's': 'i', 't': 'u',
            'u': 'y', 'v': 't', 'w': 'r', 'x': 'e', 'y': 'w',
            'z': 'q',
            # 大写字母映射（可选）
            'A': 'M', 'B': 'N', 'C': 'B', 'D': 'V', 'E': 'C',
            'F': 'X', 'G': 'Z', 'H': 'L', 'I': 'K', 'J': 'J',
            'K': 'H', 'L': 'G', 'M': 'F', 'N': 'D', 'O': 'S',
            'P': 'A', 'Q': 'P', 'R': 'O', 'S': 'I', 'T': 'U',
            'U': 'Y', 'V': 'T', 'W': 'R', 'X': 'E', 'Y': 'W',
            'Z': 'Q',
        }

    def init_ui(self):
        self.setWindowTitle("单表代换辅助工具")

        self.input_label = QLabel("输入文本：")
        self.input_text = QTextEdit()

        self.result_label = QLabel("结果：")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)

        self.encrypt_btn = QPushButton("加密")
        self.decrypt_btn = QPushButton("解密")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.encrypt_btn)
        btn_layout.addWidget(self.decrypt_btn)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_label)
        main_layout.addWidget(self.input_text)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.result_text)

        self.setLayout(main_layout)

        self.encrypt_btn.clicked.connect(self.encrypt_text)
        self.decrypt_btn.clicked.connect(self.decrypt_text)

    def encrypt_text(self):
        plaintext = self.input_text.toPlainText()
        if not plaintext:
            QMessageBox.warning(self, "提示", "请输入要加密的文本")
            return
        ciphertext = encrypt(plaintext, self.key_map)
        self.result_text.setPlainText(ciphertext)

    def decrypt_text(self):
        ciphertext = self.input_text.toPlainText()
        if not ciphertext:
            QMessageBox.warning(self, "提示", "请输入要解密的文本")
            return
        plaintext = decrypt(ciphertext, self.key_map)
        self.result_text.setPlainText(plaintext)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CipherTool()
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec_())
