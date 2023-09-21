import sys
import os
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction

from service.io_service import IOService

window_name = 'Simple Notepad'


class ViewMain(QMainWindow):
    file_path = ''
    file_name = 'New'
    close_lock = False

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 기본 설정
        self.setWindowTitle(window_name+' :: '+self.file_name)
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
        self.text_editor.textChanged.connect(self.text_changed)

        # widget에 text edit 추가
        self.setCentralWidget(self.text_editor)

        self.statusBar().showMessage('0 / 0:0')  # statusbar 기본 텍스트 설정
        self.show()

    # 저장 버튼 클릭 시 실행
    def save_onclick(self):
        # 파일을 선택한 적 없다면 선택창을 띄운다.
        if self.file_path == '':
            file_save_select = QFileDialog.getSaveFileName(
                self, 'Save file', '', 'text file(*.txt);; All File(*)')

            if file_save_select[0]:
                # 선택한 위치를 저장한다.
                self.file_path = file_save_select[0]
                self.file_name = os.path.basename(file_save_select[0])
            else:
                # 선택하지 않으면 리턴한다.
                return False

        try:
            # 파일을 저장한다.
            IOService.save(
                self.file_path, self.text_editor.toPlainText())
            self.setWindowTitle(window_name+' :: '+self.file_name)
            self.close_lock = False
            return True
        except:
            # 저장 중 오류가 발생할 경우 안내창을 띄운다.
            QMessageBox.about(self, 'Error', 'Failed to save file.')

    # 열기 버튼 누를 시 실행
    def open_onclick(self):
        # 파일 내용이 삭제될 수 있음을 고지
        if len(self.text_editor.toPlainText()) > 0 or self.file_path != '':
            QMessageBox.about(
                self, 'Warning', 'Your written content will be deleted.')

        # QFileDialog로 열을 파일 불러오기
        file_select = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'text file(*.txt);; All File(*)')

        if not file_select[0]:
            return

        try:
            load_text = IOService.open(file_select[0])
            self.text_editor.setText(load_text)

            # 불러오기가 정상적으로 완료되면 file path 정보 저장
            self.file_path = file_select[0]
            self.file_name = os.path.basename(file_select[0])
            self.setWindowTitle(window_name+' :: '+self.file_name)
            self.close_lock = False

        except FileNotFoundError:
            QMessageBox.about(self, 'Error', 'The file cannot be loaded.')

    # 텍스트 내용이 바뀔 때 별표 추가
    def text_changed(self):
        self.setWindowTitle(window_name+' :: '+self.file_name+' *')
        self.close_lock = True

    def position_changed(self):
        count = len(self.text_editor.toPlainText())  # 입력한 텍스트 수
        cursor = self.text_editor.textCursor()

        self.statusBar().showMessage(
            '{0} / {1}:{2}'.format(count, cursor.blockNumber(), cursor.columnNumber()))

    def closeEvent(self, event):
        # 내용이 저장된 경우에 바로 종료한다.
        if not self.close_lock:
            return event.accept()

        # 내용이 저장되지 않은 상태에서 종료 시도 시 선택을 요구한다.
        quit_msg = "Want to exit?"
        reply = QMessageBox.question(self, 'Message', quit_msg, (QMessageBox.StandardButton.Save |
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel))

        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        elif reply == QMessageBox.StandardButton.Save:
            if self.save_onclick() == False:  # 만약 저장 취소 시 창 유지
                event.ignore()
        else:
            event.ignore()
