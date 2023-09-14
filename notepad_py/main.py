import sys
from PyQt6.QtWidgets import QApplication

from view.view_main import ViewMain

if __name__ == '__main__':
    app = QApplication(sys.argv)  # PyQt 애플리케이션은 객체를 생성해야 함.
    view = ViewMain()
    sys.exit(app.exec())
