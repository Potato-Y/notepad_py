import sys
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction

from service.io_service import IOService


class ViewMain(QMainWindow):
    file_path = ''

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

        self.statusBar().showMessage('0 / 0:0')  # statusbar 기본 텍스트 설정
        self.show()

    # 저장 버튼 클릭 시 실행
    def save_onclick(self):
        print('save click')

    # 열기 버튼 누를 시 실행
    def open_onclick(self):
        print('open click')

        # QFileDialog로 열을 파일 불러오기
        fileSelect = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'text file(*.txt);; All File(*)')

        try:
            load_text = IOService.open(fileSelect[0])
            self.text_editor.setText(load_text)

            # 불러오기가 정상적으로 완료되면 file path 정보 저장
            self.file_path = fileSelect[0]

        except FileNotFoundError:
            QMessageBox.about(self, 'Error', 'The file cannot be loaded.')

    def position_changed(self):
        count = len(self.text_editor.toPlainText())  # 입력한 텍스트 수
        cursor = self.text_editor.textCursor()

        self.statusBar().showMessage(
            '{0} / {1}:{2}'.format(count, cursor.blockNumber(), cursor.columnNumber()))
