# pip install pyqt5
from PyQt5.QtCore import QDir, Qt, QUrl, QPoint, pyqtSlot, QRegExp
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtTest
from PyQt5 import *
from functools import partial

from cryptography.fernet import Fernet
import base64

title = '  JPM'
version = 'v0.1'
width = 300
height = 400
btn_size = 25
# pwd_context = CryptContext(
#         schemes=["pbkdf2_sha256"],
#         default="pbkdf2_sha256",
#         pbkdf2_sha256__default_rounds=30000
# )
import getpass, tempfile, os, json, re, pyperclip
username = getpass.getuser()
password_dir = tempfile.gettempdir() + '/JMP/'
master_password = ''

class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.width = width
        self.height = height
        self.setFixedSize(self.width, self.height)
        self.setStyleSheet("""QMainWindow{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")

        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(self.title)
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setText('X')

        self.btn_min = ButtonGray(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        
        self.txtSearch = LineEdit(self)
        self.txtSearch.move(7, 30)
        self.txtSearch.resize(self.width - (7 * 2), 30)
        self.txtSearch.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
        # self.txtSearch.textChanged.connect(self.verify_text)
        passwords = ['password', 'abc123', 'dragon', 'test', 'test2', 'test', 'test2','password', 'abc123', 'dragon', 'test', 'test2', 'test', 'test2']
        site_names = ['google', 'microsoft', 'facebook', 'test', 'test2', 'test', 'test2','google', 'microsoft', 'facebook', 'test', 'test2', 'test', 'test2']

        scroll = QScrollArea(self)
        scroll.move(7, 70)
        scroll.resize(self.width - (7 * 2), 320)
        scroll.setWidgetResizable(True)
        self.content = QWidget()
        scroll.setWidget(self.content)
        lay = QGridLayout(self.content)
        # lay.setColumnStretch(0, 1)
        x = 10
        y = 0

        self.lblName = QLabel(self)
        self.lblName.setText('Website:')
        self.lblName.setAlignment(Qt.AlignLeft)
        self.lblName.setFont(QFont('Calibri', 11))
        lay.addWidget((self.lblName), y, 0)
        self.lblPassword = QLabel(self)
        self.lblPassword.setText('Passwords:')
        self.lblPassword.setAlignment(Qt.AlignLeft)
        self.lblPassword.setFont(QFont('Calibri', 11))
        lay.addWidget((self.lblPassword), y, 1)
        for i, j in enumerate(passwords):
            y += 1
            self.lblWebsiteName = QLabel(self)
            self.lblWebsiteName.setText(site_names[i])
            self.lblWebsiteName.setAlignment(Qt.AlignRight | Qt.AlignCenter)
            self.lblWebsiteName.setFont(QFont('Calibri', 11))
            lay.addWidget((self.lblWebsiteName), y, 0)
            self.btnPassword = QPushButton(self)
            self.btnPassword.setFont(QFont('Calibri', 14))
            self.btnPassword.setFlat(True)
            self.btnPassword.setToolTip('Copy {} to Clipboard'.format(j))
            self.btnPassword.setText(j)
            text = partial(self.copy_password, self.btnPassword.text())
            self.btnPassword.clicked.connect(text)
            lay.addWidget((self.btnPassword), y, 1)
        self.layout().addWidget(scroll)
        scroll.setStyleSheet("QScrollArea{background-color: #131313; border-radius: 3px;border-style: none; border: 1px solid black;}")
        # lay.setStyleSheet("QGridLayout{border-radius: 3px;border-style: none; border: 1px solid darkblue;}")


        # self.update()

    # def paintEvent(self, event):
    #     q = QPainter(self)
    #     q.begin(self)
    #     q.setRenderHint(QPainter.Antialiasing)
    #     q.setPen(QtCore.Qt.black)
    #     q.setBrush(QtCore.Qt.white)
    #     q.drawLine(self.width / 2, 70, self.width/ 2, 320)
    #     q.end()
    def copy_password(self,b):
        pyperclip.copy(b)
        # self.create_master_password()
        # lOGIN ITEMS END
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            # self.login()
            print('pressed')

    # MOVE WINDOW START
    #center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # BUTTON END
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint (event.globalPos() - self.oldPos)
            #print(delta)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            print('oh no')
    # MOVE WINDOW END
    
    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("""QDialog{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")
        self.width = width / 1.5
        self.height = height / 2.5
        self.setFixedSize(self.width, self.height)

        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(self.title + ' - Login')
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setText('X')

        self.btn_min = ButtonGray(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        # TITLE BAR END
        self.lblInfo = QLabel(self)
        self.lblInfo.setText('Password:')
        self.lblInfo.move(7, 60)
        # self.lblInfo.resize(self.width - (7 * 2), 50)
        # LOGIN ITEMS START
        self.btnLogin = ButtonGreen(self)
        self.btnLogin.setText('Login')
        self.btnLogin.move(7,self.height/1.3)
        self.btnLogin.resize(self.width - (7 * 2), 30)
        self.btnLogin.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnLogin.setToolTip('Login to account.')
        self.btnLogin.setFont(QFont('Calibri', 12))
        self.btnLogin.clicked.connect(self.login)
        
        self.txtPassword = LineEdit(self)
        self.txtPassword.setEchoMode(QLineEdit.Password)
        # self.txtPassword.setText('Password')
        self.txtPassword.setToolTip('Your Password')
        self.txtPassword.move(7, self.height / 2)
        self.txtPassword.resize(self.width - (7 * 2), 30)
        self.txtPassword.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
        self.txtPassword.textChanged.connect(self.verify_text)
        self.get_password()
        # lOGIN ITEMS END
        
    def verify_text(self):
        x = list(self.txtPassword.text())
        if len(x) > 0:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #144a85;border-radius: 3px;border-style: none; border: 1px solid darkblue;")
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.login()
            
    def login(self):
        temp = self.txtPassword.text()
        key = load_key()
        f = Fernet(key)
        # master_password = master_password.decode('utf-8')
        decrypted_encrypted = f.decrypt(master_password)
        temp_master = base64.urlsafe_b64decode(decrypted_encrypted)
        temp_master = temp_master.decode('utf-8')

        if temp == temp_master:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
            QtTest.QTest.qWait(1000)
            self.main = MainMenu()
            self.main.setWindowTitle('Main')
            self.main.setFixedSize(width, height)
            self.main.setWindowFlags(Qt.FramelessWindowHint)
            self.main.show()
            self.close()
        else:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
            
    def get_password(self):
        file = open(password_dir + "master.key", "rb")
        global master_password
        master_password = file.read()
        file.close()
    # MOVE WINDOW START
    #center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # BUTTON END
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    # MOVE WINDOW END
    
    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()




class MsgBox(QDialog):
    def __init__(self, message, msgtitle, parent=None):
        super(MsgBox, self).__init__(parent)
        self.title = msgtitle
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.width = width / 2
        self.height = height / 4.5
        self.setFixedSize(self.width, self.height)

        self.setStyleSheet("""QDialog{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")
        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText('  ' + self.title)
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_proceed)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setText('X')

        self.btn_min = ButtonGray(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        

        self.lblMessage = QLabel(self)
        self.lblMessage.setText(message)
        self.lblMessage.move(7, 30)
        
        self.btnOk = ButtonGreen(self)
        self.btnOk.setText('Ok')
        self.btnOk.clicked.connect(self.btn_proceed)
        self.btnOk.resize(btn_size + 20,btn_size)
        self.btnOk.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnOk.move(100,  60)
    
    def btn_proceed(self):
        self.login_popup = Login()
        self.login_popup.setFixedSize(width / 1.5, height / 2.5)
        self.login_popup.setWindowTitle('Login')
        self.login_popup.setWindowFlags(Qt.FramelessWindowHint)
        self.login_popup.show()
        self.close()
    def btn_min_clicked(self):
        self.showMinimized()
    # MOVE WINDOW START
    #center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # BUTTON END
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    # MOVE WINDOW END
class create_password(QDialog):
    def __init__(self, parent=None):
        super(create_password, self).__init__(parent)
        self.check_if_file_exists()
        self.title = title + ' ' + version
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.width = width / 1.5
        self.height = height / 2.5
        self.setFixedSize(self.width, self.height)

        self.setStyleSheet("""QDialog{background-color: #151515; border-radius: 3px; border: 1px solid black;}""")
        # TITLE BAR START
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText('  Create a Password')
        self.menuBarTitle.resize(self.width, btn_size + 1)
        self.menuBarTitle.move(0,0)
        self.menuBarTitle.setFont(QFont('Calibri', 8))
        self.menuBarTitle.setStyleSheet(" background-color: #121212; color: #143f85; border-radius: 3px;  border: 1px solid black; ")

        self.btn_close = ButtonRed(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("background-color: #8b0000; border-radius: 3px;  border-style: none; border: 1px solid black;")
        self.btn_close.move(self.width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
        self.btn_close.setText('X')

        self.btn_min = ButtonGray(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btn_min.move(self.width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        # TITLE BAR END
        # self.lblInfo = QLabel(self)
        # self.lblInfo.setText('Create a Password')
        # self.lblInfo.move(7, 30)
        # self.lblInfo.resize(self.width - (7 * 2), 50)
        # LOGIN ITEMS START
        self.btnCreatePassword = ButtonGreen(self)
        self.btnCreatePassword.setText('Create')
        self.btnCreatePassword.move(7,self.height/1.3)
        self.btnCreatePassword.resize(self.width - (7 * 2), 30)
        self.btnCreatePassword.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        self.btnCreatePassword.setToolTip('Create Password.')
        self.btnCreatePassword.setFont(QFont('Calibri', 12))
        self.btnCreatePassword.clicked.connect(self.create_master_password)
        
        rx = QRegExp('[A-Za-z0-9@#$%^&+=]{8,}')
        validator = QRegExpValidator(rx, self)
        
        self.txtPassword = LineEdit(self)
        # self.txtPassword.setValidator(validator)
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtPassword.setToolTip('Create a Password')
        self.txtPassword.move(7, self.height / 3)
        self.txtPassword.resize(self.width - (7 * 2), 30)
        self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        self.txtPassword.textChanged.connect(self.verify_text)
        
        self.txtPasswordConfirm = LineEdit(self)
        self.txtPasswordConfirm.setEchoMode(QLineEdit.Password)
        self.txtPasswordConfirm.setToolTip('Confirm Your Password')
        self.txtPasswordConfirm.move(7, self.height / 1.8)
        self.txtPasswordConfirm.resize(self.width - (7 * 2), 30)
        self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        self.txtPasswordConfirm.textChanged.connect(self.verify_text)
        self.verify_text()
        # self.create_master_password()
        # lOGIN ITEMS END
        
    def verify_text(self):
        x = list(self.txtPassword.text())
        y = list(self.txtPasswordConfirm.text())
        # if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', self.txtPassword.text()):

        if len(x) < 8:
            self.menuBarTitle.setText('  Create a Password')
            self.btnCreatePassword.setEnabled(False)
            self.btnCreatePassword.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
            self.txtPassword.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
            self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")
        elif len(x) >= 8:
            self.txtPassword.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
            self.menuBarTitle.setText('  Confirm Password')
            if self.txtPasswordConfirm.text() == self.txtPassword.text():
                self.menuBarTitle.setText('  Save Password')
                self.btnCreatePassword.setEnabled(True)
                self.btnCreatePassword.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
                self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #008a11;border-radius: 3px;border-style: none; border: 1px solid darkgreen;")
            else:
                if len(y) >= 1:
                    self.menuBarTitle.setText('  Password Doesn\'t Match')
                self.btnCreatePassword.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
                self.btnCreatePassword.setEnabled(False)
                self.txtPasswordConfirm.setStyleSheet("background-color :#202020;color: #8b0000;border-radius: 3px;border-style: none; border: 1px solid darkred;")

    def keyPressEvent(self, event):
        x = list(self.txtPassword.text())
        y = list(self.txtPasswordConfirm.text())
        if event.key() == Qt.Key_Return:
            if len(x) >= 8 and len(y) >= 1 and  self.txtPasswordConfirm.text() == self.txtPassword.text() and self.btnCreatePassword.isEnabled():
                self.create_master_password()
                
    def create_master_password(self):
        global master_password
        if self.txtPasswordConfirm.text() == self.txtPassword.text():
            text = self.txtPasswordConfirm.text()
            text = text.encode('utf-8')
            new_pass = base64.urlsafe_b64encode(text)
            write_key()
            key = load_key()
            f = Fernet(key)
            encrypted = f.encrypt(new_pass)
            file = open(password_dir + "master.key", "wb")
            file.write(encrypted)
            file.close()
            file = open(password_dir + "master.key", "rb")
            master_password = file.read()
            file.close()
            # buttonReply = QMessageBox.information(self, 'Notice', "Password Saved!\nDo not forget this password!", QMessageBox.Ok, QMessageBox.Ok)
            self.m = MsgBox('Password Saved!\nDo not forget this password!', 'Notice!')
            self.m.show()
            
            self.close()
        
    def check_if_file_exists(self):
        if not os.path.exists(password_dir):
            os.makedirs(password_dir)
            
        if not os.path.exists(password_dir + 'key.key'):
            file = open(password_dir + "key.key", "wb")
            file.write('')
            file.close()
        else:
            file = open(password_dir + "key.key", "rb")
            global master_password
            master_password = file.read()
            file.close()
    # MOVE WINDOW START
    #center
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        # BUTTON END
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    # MOVE WINDOW END
    
    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()
class ButtonRed(QToolButton):
    def __init__(self, parent=None):
        super(ButtonRed, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #9f0000; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #8b0000; border-radius: 3px; border-style: none; border: 1px solid black;")
class ButtonGreen(QToolButton):
    def __init__(self, parent=None):
        super(ButtonGreen, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        if self.isEnabled():
            self.setStyleSheet("color: white; background-color: #109f00; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")
        else:
            self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
            
    def leaveEvent(self,event):
        if self.isEnabled():
            self.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
        else:
            self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
class ButtonGray(QToolButton):
    def __init__(self, parent=None):
        super(ButtonGray, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #565656; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black; ")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
class ButtonBlue(QToolButton):
    def __init__(self, parent=None):
        super(ButtonBlue, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #143c85; border-radius: 3px; border-style: none; border: 1.4px solid black; ")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #144a85; border-radius: 3px; border-style: none; border: 1px solid black;")
class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(LineEdit, self).__init__(parent)
        self.readyToEdit = True

    def mousePressEvent(self, e, Parent=None):
        super(LineEdit, self).mousePressEvent(e) #required to deselect on 2e click
        if self.readyToEdit:
            self.selectAll()
            self.readyToEdit = False

    def focusOutEvent(self, e):
        super(LineEdit, self).focusOutEvent(e) #required to remove cursor on focusOut
        self.deselect()
        self.readyToEdit = True

def write_key():
    key = Fernet.generate_key()
    with open(password_dir +"key.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    return open(password_dir + "key.key", "rb").read()
    
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    m = MainMenu()
    m.show()
    # if not os.path.exists(password_dir):
    #         os.makedirs(password_dir)

    # if not os.path.exists(password_dir + 'key.key'):
    #     file = open(password_dir + "key.key", "w")
    #     file.write('')
    #     file.close()
    #     create_pass_popup = create_password()
    #     create_pass_popup.setFixedSize(width / 1.5, height / 2.5)
    #     create_pass_popup.setWindowTitle('Create Password')
    #     create_pass_popup.setWindowFlags(Qt.FramelessWindowHint)
    #     create_pass_popup.show()
    # else:
    #     if os.stat(password_dir + 'key.key').st_size != 0:
    #         login = Login()
    #         login.setWindowTitle('Login')
    #         login.show()
    #     else:
    #         create_pass_popup = create_password()
    #         create_pass_popup.setFixedSize(width / 1.5, height / 2.5)
    #         create_pass_popup.setWindowTitle('Create Password')
    #         create_pass_popup.setWindowFlags(Qt.FramelessWindowHint)
    #         create_pass_popup.show()

    # if not os.path.exists(password_dir + 'master.key'):
    #     file = open(password_dir + "master.key", "w")
    #     file.write('')
    #     file.close()
    #     create_pass_popup = create_password()
    #     create_pass_popup.setFixedSize(width / 1.5, height / 2.5)
    #     create_pass_popup.setWindowTitle('Create Password')
    #     create_pass_popup.setWindowFlags(Qt.FramelessWindowHint)
    #     create_pass_popup.show()
    # else:
    #     file = open(password_dir + "master.key", "rb")
    #     master_password = file.read()
    #     file.close()
    sys.exit(app.exec_())
