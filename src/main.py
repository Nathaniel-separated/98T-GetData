from windows import *
import sys
import re
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import requests
import bs4
import time
import threading
import pyperclip
path = '../TodayVideoName/'

class Thread_1(QtCore.QThread):
    # 线程1
    mysignal = QtCore.pyqtSignal(tuple)
    ifcomplete = []
    mutex = QtCore.QMutex()
    def __init__(self, urll):
        super().__init__()
        self.url = urll

    def run(self):
        self.getNames()

    def getNames(self):
        info = '正在爬取信息...'
        a = (0, info)
        self.mysignal.emit(a)
        names = self.url.split()
        a = 0
        ts = []
        bts2.clear()
        self.ifcomplete.clear()
        for u in names:
            t1 = threading.Thread(target=self.getName, args=(u,)) 
            # 守护 !!!
            t1.setDaemon(True) 
            # 启动
            t1.start()
            ts.append(t1)
        for t in ts:
            t.join()
        for complete in self.ifcomplete:
            if complete is not True:
                info = "存在url爬取失败!"
                a = (0, info)
                self.mysignal.emit(a)
                return 0
        info = '所有url爬取完毕'
        a = (3, info)
        self.mysignal.emit(a)
        return 0
        
    def getName(self, url):
        try:
            r= requests.get(url)
            r.encoding = 'utf-8' 
            soup = bs4.BeautifulSoup(r.text, 'lxml')
            fname = soup.find('', {'name': 'keywords'})
            result1 = re.match(r'[0-9]*[A-Z]*\-[0-9]{6}', str(fname['content']))
            result2 = re.match(r'[0-9]*[A-Z]*\-[0-9]{5}', str(fname['content']))
            result3 = re.match(r'[0-9]*[A-Z]*\-[0-9]{4}', str(fname['content']))
            result4 = re.match(r'[0-9]*[A-Z]*\-[0-9]{3}', str(fname['content']))
            result5 = re.match(r'FC2[PPV]?\-[0-9]{7}', str(fname['content']))
            result6 = re.match(r'FC2[PPV]?\-[0-9]{6}', str(fname['content']))
            if result1:
                firstname = result1.group() + '-C '
            elif result2:
                firstname = result2.group() + '-C '
            elif result3:
                firstname = result3.group() + '-C '
            elif result4:
                firstname = result4.group() + '-C '
            elif result5:
                firstname = result5.group() + '-C '
            elif result6:
                firstname = result6.group() + '-C '
            lname = soup.find('', {'name': 'description'})
            firstname += str(lname['content']).split('【影片名称】：')[1].split("【出演女优】")[0]
            lastname = str(lname['content']).split('【出演女优】：')[1].split("【影片格式】")[0]
            videoname = firstname + " " + lastname
            self.mutex.lock()
            with open(path + time.strftime("%m-%d") + '.txt', 'a', encoding='UTF-8') as f:
                f.write(videoname + '\n')
            a = (1, videoname)
            self.mysignal.emit(a)
            time.sleep(0.5)
            souptorrent = soup.find('', {'class': 'blockcode'})
            torrent = str(souptorrent.contents[0]).split('<li>')[1].split("</li>")[0]
            with open(path + time.strftime("%m-%d") + '-torrent' + '.txt', 'a', encoding='UTF-8') as fi:
                fi.write(torrent + '\n')
            self.mutex.unlock()
            a = (2, torrent)
            self.mysignal.emit(a)
        except requests.RequestException as e:
            info = "{}网址访问失败！失败信息为：{}".format(url, e)
            a = (0, info)
            self.mysignal.emit(a)
            self.ifcomplete.append(False)
        except IndexError as e:
            info = "{}爬取失败！请检查该网址是否为正确网站！".format(url)
            a = (0, info)
            self.mysignal.emit(a)
            self.ifcomplete.append(False)
        except IOError as e:
            info = "{}爬取失败！请检查{}文件夹是否存在！".format(url, path)
            a = (0, info)
            self.mysignal.emit(a)
            self.ifcomplete.append(False)
        else:
            bts.append(torrent)
            bts2.append(torrent)
            self.ifcomplete.append(True)

bts = []
bts2 = []
class MyWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setWindowOpacity(0.8)  # 设置窗口透明度
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint)  # 隐藏边框
        self.setupUi(self)
        self.quit.clicked.connect(self.close)   # 点击按钮之后关闭窗口
        self.reduce.clicked.connect(self.showMinimized) #点击按钮之后缩放窗口
        self.copythis.clicked.connect(self.copythisurl)
        self.copyall.clicked.connect(self.copyallurl)
        self.start.clicked.connect(self.threadurl)
        self.textEdit.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textEdit.customContextMenuRequested.connect(self.create_rightmenu)
        self.progressBar.setValue(0)
    #创建右键菜单函数
    def create_rightmenu(self):
        #菜单对象
        self.groupBox_menu = QMenu(self)
        # self.groupBox_menu.setStyleSheet("background-color: rgb(148, 213, 172);color: rgb(104, 116, 109);")
        self.actionA = QAction('回车',self)#创建菜单选项对象
        self.actionA.setShortcut('Enter')#设置快捷键
        self.groupBox_menu.addAction(self.actionA)#把动作A选项对象添加到菜单self.groupBox_menu上
        self.actionA.triggered.connect(self.entertext) #将动作A触发时连接到槽函数 button

        self.actionB = QAction('select ALL',self)#创建菜单选项对象
        self.actionB.setShortcut('Ctrl+A')#设置快捷键
        self.groupBox_menu.addAction(self.actionB)#把动作A选项对象添加到菜单self.groupBox_menu上
        self.actionB.triggered.connect(self.textEdit.selectAll) #将动作A触发时连接到槽函数 button

        self.groupBox_menu.popup(QCursor.pos())#声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，

    def entertext(self):
        self.textEdit.append('')

    def mouseMoveEvent(self, event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self._endPos = event.pos() - self._startPos
            self.move(event.globalPos()-self.m_Position)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.buttons() == QtCore.Qt.LeftButton:
            self._startPos = QtCore.QPoint(QMouseEvent.x(), QMouseEvent.y())
            self.m_flag = True
            self.m_Position = QMouseEvent.globalPos()-self.pos()  # 获取鼠标相对窗口的位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False

    def threadurl(self):
        self.urls = str(self.textEdit.toPlainText())
        bts2.clear()
        a = self.urls.split()
        self.b = 0
        self.progressBarimum = 0
        for i in a:
            self.b += 1
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(self.b)
        self.progressBar.setValue(0)
        self.thread = Thread_1(self.urls)
        self.thread.mysignal.connect(self.getinfo)
        self.thread.start()
    
    def getinfo(self, info):
        if(info[0] == 1):
            self.textBrowser.append(info[1] + "----已写入" + time.strftime("%m-%d") + '.txt')
        elif info[0] == 2:
            self.textBrowser.append(info[1] + "----已写入" + time.strftime("%m-%d") + '-torrent' + '.txt')
            self.progressBarimum += 1
            self.progressBar.setValue(self.progressBarimum)
        elif info[0] == 3:
            self.textBrowser.append(info[1])
            self.textEdit.setPlainText('')
            self.thread.quit()
            self.thread.terminate()
            self.thread.wait()
            del self.thread
        else:
            self.textBrowser.append(info[1])
    
    def copythisurl(self):
        torrents = '\n'.join(bts2)
        pyperclip.copy(torrents)
        self.textBrowser.append('已复制种子！\n')

    def copyallurl(self):
        torrents = '\n'.join(bts)
        pyperclip.copy(torrents)
        self.textBrowser.append('已复制种子！\n')

    def enterText(self ):
        self.textEdit.insertPlainText('\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())