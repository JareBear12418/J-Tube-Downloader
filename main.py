# pip install pyqt5
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# pip install youtube-dl / imageio
import sys, os, getpass, shutil, subprocess, imageio, youtube_dl
width = 300
height = 120
title = 'J-Tube Downloader'
version = 'v0.1'
username = getpass.getuser()
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
fileLoc = 0
class main(QMainWindow):
    def __init__(self, name):
        super().__init__()
        
        # app.setStyleSheet(qdarkgraystyle.load_stylesheet())
        # Force the style to be the same on all OSs:
        app.setStyle("Fusion")

        # Now use a palette to switch to dark colors:
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
        
        self.title = name
        # RADIO BUTTON START
        self.radAudio = QRadioButton(self)
        self.radAudio.setText('Audio')
        self.radAudio.move(10,80)
        # RADIO BUTTON END
        # TEXT BOX START
        self.txtURL = QLineEdit(self)
        self.txtURL.move(10,40)
        self.txtURL.resize(width - 20,30)
        # TEXT BOX END
        # LABEL START
        self.lblTitle = QLabel(self)
        self.lblTitle.move(10,0)
        self.lblTitle.resize(250,20)
        self.lblTitle.setText("")
        
        
        self.lblURL = QLabel(self)
        self.lblURL.move(10,20)
        self.lblURL.resize(250,20)
        self.lblURL.setText("URL: ")
        
        self.lblState = QLabel(self)
        self.lblState.move(210,85)
        self.lblState.setText("")
        # LABEL END
        # BUTTON START
        self.btnDownload = QPushButton(self)
        self.btnDownload.setText('Download')
        self.btnDownload.move(width / 3,80)
        self.btnDownload.clicked.connect(self.downloadYoutube)
        # BUTTON END
    def downloadYoutube(self):
        self.changeText()
        try:
            self.lblState.setText('Downloading...')
            directory = 'C:/Users/{}/Videos/J-Tube Downloads'.format(username)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            url = self.txtURL.text()
            if 'https://www.youtube.com/watch?' not in url:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "{} is an invalid URL".format(url), QMessageBox.Ok, QMessageBox.Ok)
                return
            if self.radAudio.isChecked() == True:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'extractaudio': True,
                    'audioformat': "mp3"
                }
            else:
                ydl_opts = {
                    'format': 'bestaudio/best'
                }
            info_dict = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download = False)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            self.lblTitle.setText(str(video_title))
            
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    self.lblState.setText('Downloading...')
                    ydl.download([url])
            except:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "Problem downloading {}".format(url), QMessageBox.Ok, QMessageBox.Ok)
                return
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
        except Exception as e:
            self.lblState.setText('')
            self.lblTitle.setText("")
            buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
            return
    def changeText(self):
        self.lblState.setText('Downloading...')
    def explore(self, path):
        # explorer would choke on forward slashes
        path = os.path.normpath(path)
        if os.path.isdir(path):
            subprocess.run([FILEBROWSER_PATH, path])
        elif os.path.isfile(path):
            subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = main('hi')
    downloader.setFixedSize(width,height)
    downloader.setWindowTitle(title + ' ' + version)
    downloader.show()
    sys.exit(app.exec_())
