import sys
from window import *
from PyQt5 import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioPlayerApp()
    window.show()
    sys.exit(app.exec_())