import sys
from PyQt6.QtWidgets import QMainWindow, QTextEdit
from PyQt6.QtGui import QAction

class ViewMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 기본 설정
        self.setWindowTitle('Simple Notepad')
        self.move(300, 300)
        self.resize(400, 500)

        # save menu
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('File save.')
        save_action.triggered.connect(self.save_onclick)

        # open menu
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('File open.')
        open_action.triggered.connect(self.open_onclick)

        # menu bar 생성
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # file 메뉴 버튼
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(save_action)
        file_menu.addAction(open_action)

        # text editor
        self.text_editor = QTextEdit()
        self.text_editor.setAcceptRichText(False)
        self.text_editor.cursorPositionChanged.connect(self.position_changed)

        # widget에 text edit 추가
        self.setCentralWidget(self.text_editor)

        self.statusBar().showMessage('0 / 0:0')
        self.show()

    # 저장 버튼 클릭 시 실행
    def save_onclick(self):
        print('save click')

    # 열기 버튼 누를 시 실행
    def open_onclick(self):
        print('open click')

    def position_changed(self):
        count = len(self.text_editor.toPlainText()) # 입력한 텍스트 수
        cursor=self.text_editor.textCursor()

        self.statusBar().showMessage('{0} / {1}:{2}'.format(count,cursor.blockNumber(),cursor.columnNumber()))
