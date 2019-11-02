# pip install pyqt5
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# pip install youtube-dl / imageio
import sys, os, getpass, shutil, subprocess, youtube_dl
width = 300
height = 150
title = 'J-Tube Downloader'
version = 'v0.4'
username = getpass.getuser()
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
fileLoc = 0
dl_percentage = 0
class main(QMainWindow):
    def __init__(self, name):
        super().__init__()
        
        # app.setStyle("Windows Vista")
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
        self.txtURL.move(40,40)
        self.txtURL.resize(width - 50,30)
        self.txtURL.setToolTip('Paste your YouTube link here.')
        # TEXT BOX END
        # LABEL START
        self.lblTitle = QLabel(self)
        self.lblTitle.move(10,0)
        self.lblTitle.resize(280,20)
        self.lblTitle.setText("")
        
        
        self.lblURL = QLabel(self)
        self.lblURL.move(10,43)
        self.lblURL.resize(30,20)
        self.lblURL.setText("URL: ")
        
        # PROGRESS BAR START
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10, 115, 280, 30)
        self.progress.setValue(0)
        self.progress.hide()
        # PROGRESs BAR END
        
        self.lblState = QLabel(self)
        self.lblState.move(20,115)
        self.lblState.resize(280, 30)
        self.lblState.setText("")
        # LABEL END
        # BUTTON START
        self.btnDownload = QPushButton(self)
        self.btnDownload.setText('Download')
        self.btnDownload.move(width / 3,80)
        self.btnDownload.clicked.connect(self.downloadYoutube)
        
        # BUTTON END
    def downloadYoutube(self):
        try:
            self.progress.show()
            directory = 'C:/Users/{}/Videos/J-Tube Downloads'.format(username)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            url = self.txtURL.text()
            if 'https://www.youtube.com/watch?' not in url:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "{} is an invalid URL".format(url), QMessageBox.Ok, QMessageBox.Ok)
                return
            # if 'https://youtu.be/' not in url:
            #     buttonReply = QMessageBox.critical(self, 'Error! :(', "{} is an invalid URL".format(url), QMessageBox.Ok, QMessageBox.Ok)
            #     return
            if self.radAudio.isChecked() == True:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'extractaudio': True,
                    'audioformat': "mp3",
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
                self.lblState.setText('')
                buttonReply = QMessageBox.critical(self, 'Error! :(', "Problem downloading {}\n\nError Log:\n{}".format(url, e), QMessageBox.Ok, QMessageBox.Ok)
                return
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
            self.lblState.setText('')
            self.lblTitle.setText("")
            buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
            return
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
if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = main('')
    downloader.setFixedSize(width,height)
    downloader.setWindowTitle(title + ' ' + version)
    downloader.show()
    sys.exit(app.exec_())
