# pip install pyqt5
from PyQt5.QtCore import QDir, Qt, QUrl, QPoint, pyqtSlot
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
# pip install youtube-dl / imageio / ffmpeg / eyed3
import sys, os, getpass, shutil, subprocess, youtube_dl, ffmpeg, json, webbrowser, urllib, eyed3
from datetime import datetime
from urllib.request import Request, urlopen
# pip install beautifulsoup4
from bs4 import BeautifulSoup
# pip install google
from googlesearch import search

width = 300
height = 170
title = ' J-Tube Downloader'
version = 'v0.4'
username = getpass.getuser()
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')
directory = 'C:/Users/{}/Videos/J-Tube Downloads'.format(username)
fileLoc = 0
btn_size = 25


file_name = None
file_exten = None
file_owner = None
file_id = None

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(width,height)
        self.menuBarTitle = QLabel(self)
        self.menuBarTitle.setText(title + ' ' + version)
        self.menuBarTitle.resize(width - 1, btn_size + 1)
        self.menuBarTitle.move(1,0)
        self.menuBarTitle.setFont(QFont('Calibri', 10))
        self.menuBarTitle.setStyleSheet("""
                                        background-color: #121212;
                                        color: #143f85;
                                        """)

        self.btn_close = HoverButtonExit(self)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.resize(btn_size + 10,btn_size)
        self.btn_close.setStyleSheet("""background-color: #8b0000;
                                    border-radius: 3px; 
                                    border-style: none;
                                    border: 1px solid black;""")
        self.btn_close.move(width - (btn_size + 10),0)
        self.btn_close.setFont(QFont('Calibri', 15))
        self.btn_close.setToolTip('Close.')
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
        self.btn_min.setToolTip('Minimize.')
        self.btn_min.setText('-')
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        app.setStyle("Fusion")
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(35, 35, 35))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(0, 0,255))
        palette.setColor(QPalette.HighlightedText, Qt.white)
        app.setPalette(palette)
        
        self.windowTitle = title
        # RADIO BUTTON START
        self.radAudio = Button(self)
        self.radAudio.setCheckable(True)
        self.radAudio.setText('Audio')
        self.radAudio.move(30,100)
        self.radAudio.resize(40,30)
        self.radAudio.setChecked(True)
        self.radAudio.setToolTip('Download Youtube Video as Audio.')
        self.radAudio.toggled.connect(self.radPressed)
        self.radAudio.setStyleSheet("""
                                    color: white;
                                    background-color: #144a85; 
                                    border-radius: 3px; 
                                    border-style: none;
                                    border: 1px solid black;""")
        # RADIO BUTTON END
        # TEXT BOX START
        self.txtURL = LineEdit(self)
        self.txtURL.move(10,60)
        self.txtURL.resize(width - 20,30)
        self.txtURL.setText('Paste your YouTube link here.')
        self.txtURL.setToolTip('Paste your YouTube link here.')
        self.txtURL.setStyleSheet("""
                                background-color :#202020;
                                color: #144a85;
                                border-radius: 3px;
                                border-style: none; 
                                border: 1px solid darkblue;;
                                """)
        # TEXT BOX END
        # LABEL START
        self.lblTitle = QLabel(self)
        self.lblTitle.move(10,30)
        self.lblTitle.resize(280,20)
        self.lblTitle.setText("")
        
        
        # self.lblURL = QLabel(self)
        # self.lblURL.move(10,63)
        # self.lblURL.resize(30,20)
        # self.lblURL.setText("URL: ")
        
        # PROGRESS BAR START
        self.progress = QProgressBar(self)
        self.progress.setGeometry(10, 135, 280, 30)
        self.progress.setToolTip('Progress bar.')
        self.progress.setStyleSheet("""
                                    QProgressBar{
                                        border: 2px solid darkblue;
                                        border-radius: 3px;
                                        text-align: 140
                                    }

                                    QProgressBar::chunk {
                                        background-color: blue;
                                        margin: 1px;
                                    }
                                    """)
        self.progress.setValue(0)
        self.progress.setFormat('')
        self.progress.hide()
        # PROGRESs BAR END
        
        self.lblState = QLabel(self)
        self.lblState.move(20,135)
        self.lblState.resize(280, 30)
        self.lblState.setText("")
        # LABEL END
        # BUTTON START
        self.btnDownload = Button(self)
        self.btnDownload.setText('Download')
        self.btnDownload.move(70,100)
        self.btnDownload.resize(80,30)
        self.btnDownload.clicked.connect(self.downloadYoutube)
        self.btnDownload.setFont(QFont('Calibri', 10))
        self.btnDownload.setToolTip('Download the current YouTube URL Video.')
        self.btnDownload.setStyleSheet("""background-color: #144a85; 
                                       border-radius: 3px; 
                                       border-style: none;
                                       border: 1px solid black;""")
        
        self.btnSearch = Button(self)
        self.btnSearch.setText('Search YouTube')
        self.btnSearch.move(150,100)
        self.btnSearch.resize(120,30)
        self.btnSearch.clicked.connect(self.search_song)
        self.btnSearch.setFont(QFont('Calibri', 10))
        self.btnSearch.setToolTip('Search YouTube for a video.')
        self.btnSearch.setStyleSheet("""background-color: #144a85; 
                                       border-radius: 3px; 
                                       border-style: none;
                                       border: 1px solid black;""")
        
        
        self.center()
        self.oldPos = self.pos()
        # self.file_name()
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
    def show_file_name(self):
        # self.close()
        
        # import threading
        # threading.Thread(target=change_file_name).start()
        self.cfn = change_file_name()
        self.cfn.setFixedSize(215, 190)
        self.cfn.setWindowTitle('File Name')
        self.cfn.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.cfn.show()
    def radPressed(self):
        if self.radAudio.isChecked():
            self.radAudio.setText('Audio')
            self.radAudio.setToolTip('Download Youtube Video as Audio.')
        else:
            self.radAudio.setText('Video')
            self.radAudio.setToolTip('Download Youtube Video as Video.')
    def downloadYoutube(self):
        # import threading
        # threading.Thread(target=self.StartDownloadYoutubeThread).start()
        self.StartDownloadYoutubeThread()
    @pyqtSlot()
    def StartDownloadYoutubeThread(self):
        print('starting')
        self.lblState.setText('downloading...')
        import time
        try:
            global file_name
            global file_exten
            global file_id
            global file_owner
            global fileLoc
            self.progress.show()
           
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            url = self.txtURL.text()
            if 'youtu' not in url:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "{} is an invalid URL".format(url), QMessageBox.Ok, QMessageBox.Ok)
                return
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
                    'format': 'best',
                    'noplaylist': True,
                    'progress_hooks': [self.my_hook]
                    # 'outtmpl': directory
                }
            info_dict = youtube_dl.YoutubeDL(ydl_opts).extract_info(url, download = False)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            file_name = video_title
            file_id = video_id
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html.parser')
            html = soup.prettify('utf-8')
            video_details = {}
            other_details = {}
            for span in soup.findAll('span',attrs={'class': 'watch-title'}):
                video_details['TITLE'] = span.text.strip()
            for script in soup.findAll('script',attrs={'type': 'application/ld+json'}):
                channelDescription = json.loads(script.text.strip())
                video_details['CHANNEL_NAME'] = channelDescription['itemListElement'][0]['item']['name']
            try:
                file_owner = video_details['CHANNEL_NAME']
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    self.progress.show()
                    ydl.download([url])
            except Exception as e:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "Problem downloading/converting {}\n\nError Log:\n{}".format(url, e), QMessageBox.Ok, QMessageBox.Ok)
                self.progress.hide()
                self.lblState.setText('')
                self.lblTitle.setText('')
                self.progress.setValue(0)
                return
            # This code below gets the file that has been downloaded
            # FIXME improve this to make it more readable and cleaner
            f = os.listdir(os.getcwd())
            t = video_title + '-' + video_id
            for filename in f:
                if t in filename:
                    fileLoc = filename
            file_exten = os.path.splitext(fileLoc)[1]
            self.lblState.setText('Finished!')
            if self.radAudio.isChecked() == True:
                print(os.path.dirname(os.path.realpath(__file__)) + '/' + file_name + '-' + file_id + file_exten, directory + '/' + file_name + ' - ' + file_owner + file_exten)
                # import threading
                # threading.Thread(target=self.file_name1).start()
                self.show_file_name()
            else:
                print(os.path.dirname(os.path.realpath(__file__)) + '/' + file_name + '-' + file_id + file_exten, directory + '/' + file_name + ' - ' + file_owner + file_exten)
                shutil.move(os.path.dirname(os.path.realpath(__file__)) + '/' + file_name + '-' + file_id + file_exten, directory + '/' + file_name + ' - ' + file_owner + file_exten)
                buttonReply = QMessageBox.information(self, 'Success! :)', "Success!\nDo you want to open the file directory?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if buttonReply == QMessageBox.Yes:
                    explore(directory)
            self.lblState.setText('')
            self.lblTitle.setText('')
            self.progress.setValue(0)
            self.progress.hide()
        except Exception as e:
            buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
            self.progress.hide()
            self.lblState.setText('')
            self.lblTitle.setText('')
            self.progress.setValue(0)
            return
    @pyqtSlot()
    def my_hook(self, d):
        self.progress.show()
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
            self.save_history(d['filename'])
            
        if d['status'] == 'downloading':
            self.lblTitle.setText(d['filename'])
            self.progress.show()
            p = d['_percent_str']
            p = p.replace('%','')
            self.progress.setValue(float(p))
            if not p == 100:
                if d.get("_total_bytes_str") != None:
                    self.lblState.setText(d['_total_bytes_str'] + ' at ' + d['_speed_str'] + ' ' + d['_eta_str'])
                else:
                    self.lblState.setText(d['_total_bytes_estimate_str'] + ' at ' + d['_speed_str'] + ' ' + d['_eta_str'])
            else:
                self.lblState.setText('Finishing up...')
                
            print(d['filename'], d['_percent_str'], d['_eta_str'])
    def save_history(self, song):
        try:
            req = Request(self.txtURL.text(), headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, 'html.parser')
            html = soup.prettify('utf-8')
            video_details = {}
            other_details = {}
            for script in soup.findAll('script',attrs={'type': 'application/ld+json'}):
                channelDescription = json.loads(script.text.strip())
                video_details['CHANNEL_NAME'] = channelDescription['itemListElement'][0]['item']['name']
            with open(directory + '/J-Tube Download History.txt', 'a+', encoding='utf-8') as file:
                file.write('Downloaded on: ' + str(datetime.now()) + ' Song Name: ' +  song + ' Uploaded by: ' + video_details['CHANNEL_NAME'] + '\n')
        except Exception as e:
            buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
            return
    def search_song(self):
        global file_owner
        # message box input string
        text, okPressed = QInputDialog.getText(self, " ","Video name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            # url = 'youtube '
            url = 'https://www.youtube.com/watch?v='
            query = url + text
            try:
                for url in search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2):
                    print(url)
                    if 'watch' in url:
                        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                        webpage = urlopen(req).read()
                        soup = BeautifulSoup(webpage, 'html.parser')
                        html = soup.prettify('utf-8')
                        video_details = {}
                        other_details = {}
                        for span in soup.findAll('span',attrs={'class': 'watch-title'}):
                            video_details['TITLE'] = span.text.strip()
                        for script in soup.findAll('script',attrs={'type': 'application/ld+json'}):
                            channelDescription = json.loads(script.text.strip())
                            video_details['CHANNEL_NAME'] = channelDescription['itemListElement'][0]['item']['name']
                        # try:
                        file_owner = video_details['CHANNEL_NAME']
                        # except KeyError:
                        #     buttonReply = QMessageBox.critical(self, 'Error! :(', "Oh no! There seems too be somthing wrong\nwith your internet connection.\nTry again later.", QMessageBox.Ok, QMessageBox.Ok)
                        #     return
                        urlLink=" <a href=\"{}\">{} </a>\n".format(url, url)
                        self.setStyleSheet("QMessageBox{border: 2px solid #121212; border-radius: 1px;}")
                        buttonReply = QMessageBox.information(self, 'Result', "URL: {}\nVideo Name: {}\nUploaded by: {}\n\nIs this the video/song you want to download?".format(url, video_details['TITLE'], video_details['CHANNEL_NAME']), QMessageBox.Yes | QMessageBox.Retry | QMessageBox.Cancel, QMessageBox.Yes)
                        if buttonReply == QMessageBox.Yes:
                            self.txtURL.setText(url)
                            return
                        if buttonReply == QMessageBox.Cancel:
                            return
                    else:
                        continue
            except Exception as e:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
                return
    def btn_close_clicked(self):
        self.close()
    def btn_min_clicked(self):
        self.showMinimized()
class change_file_name(QWidget):
        def __init__(self):
            super().__init__()
            self.setStyleSheet("QDialog{border: 2px solid #121212; border-radius: 1px;}")
            self.menuBarTitle = QLabel(self)
            self.menuBarTitle.setText(" Modify file tags")
            self.menuBarTitle.resize(width - 1, btn_size + 1)
            self.menuBarTitle.setFont(QFont('Calibri', 10))
            self.menuBarTitle.setStyleSheet("""
                                            background-color: #121212;
                                            color: #143f85;""")
            self.setFixedSize(width,height)
            
            self.lblTitle = QLabel(self)
            self.lblTitle.setText('Title:')
            self.lblTitle.move(5,30)
            self.lblTitle.setFont(QFont('Calibri', 16))
            
            self.lblArtist = QLabel(self)
            self.lblArtist.setText('Artist:')
            self.lblArtist.move(5,70)
            self.lblArtist.setFont(QFont('Calibri', 16))
            
            self.lblAlbum = QLabel(self)
            self.lblAlbum.setText('Album:')
            self.lblAlbum.move(5,110)
            self.lblAlbum.setFont(QFont('Calibri', 16))
            
            self.txtTitle = LineEdit(self)
            self.txtTitle.setText(file_name)
            self.txtTitle.move(80,30)
            self.txtTitle.resize(130,40)
            self.txtTitle.setAlignment(Qt.AlignCenter)
            self.txtTitle.setFont(QFont('Calibri', 10))
            self.txtTitle.setToolTip('The name of the Song')
            self.txtTitle.setStyleSheet("""
                                        background-color :#292929;
                                        color: #144a85;
                                        border-radius: 3px;
                                        border-style: none; 
                                        border: 1px solid darkblue;
                                        """)
            
            self.txtArtist = LineEdit(self)
            self.txtArtist.setText(file_owner)
            self.txtArtist.move(80,70)
            self.txtArtist.resize(130,40)
            self.txtArtist.setAlignment(Qt.AlignCenter)
            self.txtArtist.setFont(QFont('Calibri', 10))
            self.txtArtist.setToolTip('The name of the Artist')
            self.txtArtist.setStyleSheet("""
                                        background-color :#292929;
                                        color: #144a85;
                                        border-radius: 3px;
                                        border-style: none; 
                                        border: 1px solid darkblue;;
                                        """)
            
            self.txtAlbum = LineEdit(self)
            self.txtAlbum.setText('')
            self.txtAlbum.move(80,110)
            self.txtAlbum.resize(130,40)
            self.txtAlbum.setAlignment(Qt.AlignCenter)
            self.txtAlbum.setFont(QFont('Calibri', 10))
            self.txtAlbum.setToolTip('The name of the album')
            self.txtAlbum.setStyleSheet("""
                                        background-color :#292929;
                                        color: #144a85;
                                        border-radius: 3px;
                                        border-style: none; 
                                        border: 1px solid darkblue;;
                                        """)
            
            self.btnYes = HoverButtonModify(self)
            self.btnYes.setText('Modify')
            self.btnYes.move(1,160 - 1)
            self.btnYes.resize(215/2,30)
            self.btnYes.clicked.connect(self.modify)
            self.btnYes.setFont(QFont('Calibri', 10))
            self.btnYes.setToolTip('Modify file tags.')
            self.btnYes.setStyleSheet("""
                                      background-color: #008a11; 
                                      border-radius: 3px; 
                                      border-style: none;
                                      border: 1px solid black;
                                      """)
            
            self.btnNo = HoverButtonExit(self)
            self.btnNo.setText('Cancel')
            self.btnNo.move(215/2,160 - 1)
            self.btnNo.resize(215/2,30)
            self.btnNo.clicked.connect(self.cancel)
            self.btnNo.setFont(QFont('Calibri', 10))
            self.btnNo.setToolTip('Do not modify file tags.')
            self.btnNo.setStyleSheet("""
                                     background-color: #8b0000; 
                                     border-radius: 3px; 
                                     border-style: none;
                                     border: 1px solid black;
                                     """)
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
        def modify(self):
            self.update_id3(os.path.dirname(os.path.realpath(__file__)) + '/' + file_name + '-' + file_id + file_exten, self.txtAlbum.text(), self.txtArtist.text(), self.txtTitle.text())
        def cancel(self):
            try:
                shutil.move(os.path.dirname(os.path.realpath(__file__)) + '/' + file_name + '-' + file_id + file_exten, directory + '/' + file_name + ' - ' + file_owner + file_exten)
            except Exception as e:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
                return
            self.close()
            buttonReply = QMessageBox.information(self, 'Success! :)', "Success!\nDo you want to open the file directory?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                explore(directory)
        def update_id3(self, mp3_file_name, album, artist, item_title):    
            #edit the ID3 tag to add the title, artist, artwork, date, and genre
            audiofile = eyed3.load(mp3_file_name)
            audiofile.tag.artist = artist
            audiofile.tag.album = album
            audiofile.tag.album_artist = artist
            audiofile.tag.title = item_title
            audiofile.tag.save()
            try:
                shutil.move(file_name + '-' + file_id + file_exten, directory + '/' + self.txtTitle.text() + ' - ' + self.txtArtist.text() + file_exten)
            except Exception as e:
                buttonReply = QMessageBox.critical(self, 'Error! :(', "{}".format(e), QMessageBox.Ok, QMessageBox.Ok)
                return
            self.close()
            buttonReply = QMessageBox.information(self, 'Success! :)', "Success!\nDo you want to open the file directory?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            if buttonReply == QMessageBox.Yes:
                explore(directory)
class HoverButtonExit(QToolButton):
    def __init__(self, parent=None):
        super(HoverButtonExit, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #9f0000; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #8b0000; border-radius: 3px; border-style: none; border: 1px solid black;")
class HoverButtonModify(QToolButton):
    def __init__(self, parent=None):
        super(HoverButtonModify, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #109f00; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black;")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #008a11; border-radius: 3px; border-style: none; border: 1px solid black;")
class HoverButtonMinimize(QToolButton):
    def __init__(self, parent=None):
        super(HoverButtonMinimize, self).__init__(parent)
        self.setMouseTracking(True)

    def enterEvent(self,event):
        self.setStyleSheet("color: white; background-color: #565656; border-radius: 3px; border-style: none;  font-weight: bold;  border: 1.4px solid black; ")

    def leaveEvent(self,event):
        self.setStyleSheet("color: white; background-color: #444444; border-radius: 3px; border-style: none; border: 1px solid black;")
class Button(QToolButton):
    def __init__(self, parent=None):
        super(Button, self).__init__(parent)
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
def explore(path):
    # explorer would choke on forward slashes
    path = os.path.normpath(path)
    if os.path.isdir(path):
        subprocess.run([FILEBROWSER_PATH, path])
    elif os.path.isfile(path):
        subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
# test
if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = main()
    # FIXME fix CSS 
    downloader.setStyleSheet("""QMainWindow
                            {
                                border: 2px solid #121212; 
                                border-radius: 1px;
                            }
                            /*QPushButton
                            {
                                color: white; 
                                background-color: #144a85; 
                                border-radius: 3px; 
                                border-style: none;
                                border: 1px solid black;
                                width: 100%;
                                font-size: 16px;
                                height: 30%;
                            }
                            QLineEdit
                            {
                                background-color :#202020;
                                color: #144a85;
                                border-radius: 3px;
                                border-style: none; 
                                border: 1px solid darkblue;;
                            }*/
                            """)
    downloader.show()
    sys.exit(app.exec_())
