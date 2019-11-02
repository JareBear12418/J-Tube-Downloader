# pip install pyqt5
from PyQt5.QtCore import QDir, Qt, QUrl, QPoint, pyqtSlot
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# pip install youtube-dl / imageio
import sys, os, getpass, shutil, subprocess, youtube_dl, ffmpeg
width = 300
height = 170
title = ' J-Tube Downloader'
version = 'v0.4'
username = getpass.getuser()
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
fileLoc = 0
dl_percentage = 0
btn_size = 25
class main(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setFixedSize(width,height)
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(title + ' ' + version)
        self.menuBarTitle.resize(width, btn_size + 1)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet("""
                                        background-color: #222222;
                                        color: #144a85;""")

        self.btn_close = HoverButtonExit(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("""background-color: #8b0000;
                                    border-radius: 3px; 
                                    border-style: none;
                                    border: 1px solid black;""")
        self.btn_close.move(width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setText('X')

        self.btn_min = HoverButtonMinimize(self)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.resize(btn_size + 10, btn_size)
        self.btn_min.setStyleSheet("""background-color: #444444;
                                   border-radius: 3px;
                                   border-style: none; 
                                   border: 1px solid black;""")
        self.btn_min.move(width - (btn_size + btn_size + 20),0)
        self.btn_min.setFont(QFont('Calibri', 20))
        self.btn_min.setText('-')
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        app.setStyle("Windows Vista")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.black)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.black)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)
        
        self.title = name
        # RADIO BUTTON START
        self.radAudio = QRadioButton(self)
        self.radAudio.setText('Audio')
        self.radAudio.move(10,100)
        # RADIO BUTTON END
        # TEXT BOX START
        self.txtURL = QLineEdit(self)
        self.txtURL.move(40,60)
        self.txtURL.resize(width - 50,30)
        self.txtURL.setToolTip('Paste your YouTube link here.')
        self.txtURL.setStyleSheet("""
                                background-color :#292929;
                                color: #144a85;
                                border-radius: 3px;
                                border-style: none; 
                                border: 1px solid black;
                                """)
        # TEXT BOX END
        # LABEL START
        self.lblTitle = QLabel(self)
        self.lblTitle.move(10,30)
        self.lblTitle.resize(280,20)
        self.lblTitle.setText("")
        
        
        self.lblURL = QLabel(self)
        self.lblURL.move(10,63)
        self.lblURL.resize(30,20)
        self.lblURL.setText("URL: ")
        
        # PROGRESS BAR START
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10, 135, 280, 30)
        self.progress.setValue(0)
        self.progress.hide()
        # PROGRESs BAR END
        
        self.lblState = QLabel(self)
        self.lblState.move(20,135)
        self.lblState.resize(280, 30)
        self.lblState.setText("")
        # LABEL END
        # BUTTON START
        self.btnDownload = DownloadButton(self)
        self.btnDownload.setText('Download')
        self.btnDownload.move(width / 3,100)
        self.btnDownload.resize(80,30)
        self.btnDownload.clicked.connect(self.downloadYoutube)
        self.btnDownload.setFont(QFont('Calibri', 10))
        self.btnDownload.setStyleSheet("""background-color: #39873b; 
                                       border-radius: 3px; 
                                       border-style: none;
                                       border: 1px solid black;""")
        
        self.center()
        self.oldPos = self.pos()
        
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
    def downloadYoutube(self):
        try:
            self.progress.show()
            directory = 'C:/Users/{}/Videos/J-Tube Downloads'.format(username)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            url = self.txtURL.text()
            # if 'https://www.youtube.com/watch?' not in url:
            #     buttonReply = QMessageBox.critical(self, 'Error! :(', "{} is an invalid URL".format(url), QMessageBox.Ok, QMessageBox.Ok)
            #     return
            # if 'https://youtu.be/' not in url:
            #     buttonReply = QMessageBox.critical(self, 'Error! :(', "{} is an invalid URL".format(url), QMessageBox.Ok, QMessageBox.Ok)
            #     return
            if self.radAudio.isChecked() == True:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'postprocessor_args': [
                        '-ar', '16000'
                    ],
                    'prefer_ffmpeg': True,
                    'keepvideo': False,
                    'progress_hooks': [self.my_hook],
                    'noplaylist': True,
                    # 'outtmpl': directory
                }
            else:
                ydl_opts = {
                    'noplaylist': True,
                    'progress_hooks': [self.my_hook]
                    # 'outtmpl': directory
                }
            info_dict = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download = False)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    self.progress.show()
                    ydl.download([url])
            except Exception as e:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "Problem downloading {}\n\nError Log:\n{}".format(url, e), QMessageBox.Ok, QMessageBox.Ok)
                return
                self.explore(directory)
                self.lblState.setText('')
                self.lblTitle.setText('')
                self.progress.setValue(0)
            # This code below gets the file that has been downloaded
            # FIXME improve this to make it more readable and cleaner
            f = os.listdir(os.getcwd())
            t = video_title + '-' + video_id
            for i, j in enumerate(f):
                # print(j, i)
                if t in j:
                    print(j)
                    global fileLoc
                    fileLoc = f[i]
                    print(fileLoc)
                    
            extension = os.path.splitext(fileLoc)[1]
            shutil.move(video_title + '-' + video_id + extension, directory + '/' + video_title + extension)
            self.lblState.setText('Finished!')
            buttonReply = QMessageBox.information(self, 'Success! :)', "Succesfully downloaded!\nDo you want to open the file directory?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                self.explore(directory)
            self.lblState.setText('')
            self.lblTitle.setText('')
            self.progress.setValue(0)
            self.progress.hide()
        except Exception as e:
            buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
            return
            self.explore(directory)
            self.lblState.setText('')
            self.lblTitle.setText('')
            self.progress.setValue(0)
    @pyqtSlot(int)
    def my_hook(self, d):
        self.progress.show()
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
        if d['status'] == 'downloading':
            self.lblTitle.setText(d['filename'])
            self.progress.show()
            p = d['_percent_str']
            p = p.replace('%','')
            self.progress.setValue(float(p))
            self.lblState.setText(d['_total_bytes_str'] + ' at ' + d['_speed_str'] + ' ' + d['_eta_str'])
            # print(d['filename'], d['_percent_str'], d['_eta_str'])
        
    def explore(self, path):
        # explorer would choke on forward slashes
        path = os.path.normpath(path)
        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
    

    def btn_close_clicked(self):
        self.close()

    def btn_min_clicked(self):
        self.showMinimized()

class HoverButtonExit(QToolButton):
    def __init__(self, parent=None):
        super(HoverButtonExit, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("background-color: #9f0000; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")

    def leaveEvent(self,event):
        self.setStyleSheet("background-color: #8b0000; border-radius: 3px; border-style: none; border: 1px solid black;")
        
class HoverButtonMinimize(QToolButton):
    def __init__(self, parent=None):
        super(HoverButtonMinimize, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("background-color: #565656; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black; ")

    def leaveEvent(self,event):
        self.setStyleSheet("background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
        
class DownloadButton(QToolButton):
    def __init__(self, parent=None):
        super(DownloadButton, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("background-color: #099109; border-radius: 3px; border-style: none; border: 1.4px solid black; ")

    def leaveEvent(self,event):
        self.setStyleSheet("background-color: #39873b; border-radius: 3px; border-style: none; border: 1px solid black;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = main('')
    downloader.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")
    # downloader.setWindowFlags(Qt.CustomizeWindowHint)
    downloader.show()
    sys.exit(app.exec_())
