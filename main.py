# main.py
import os
import sys

plugin_path = r"C:\Users\肖焦菲\AppData\Local\Programs\Python\Python311-32\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
from PyQt5.QtWidgets import QApplication
from gui import SubstitutionCipherGUI
from PyQt5.QtCore import Qt

def main():
    app = QApplication(sys.argv)
    window = SubstitutionCipherGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
