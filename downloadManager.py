from threading import Thread

__author__ = "Harshit"

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dm2.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot, SIGNAL
import sys
from ui import Ui_Form
import urllib2
from threading import Thread



def exitFun():
    exit(1)

class GetTitleThread(Thread):

    def __init__(self,tname, url,start,end, part):
        self.tname = tname
        self.part =None
        self.url = url
        self.startPos = str(start)
        self.end = str(end)
        super(GetTitleThread, self).__init__()

    def run(self):
        print self.tname + self.url + self.startPos + self.end
        req = urllib2.Request(self.url, headers={'Range': 'bytes=' + self.startPos + '-' + self.end})
        print req
        data = urllib2.urlopen(req).read()
        # print data
        self.part = data


def download_part(threadName, url, start,end, partName):
    print threadName + url + str(start) + str(end)
    req = urllib2.Request(url, headers={'Range': 'bytes='+str(start)+'-'+str(end)})
    print req
    data = urllib2.urlopen(req).read()
    # print data
    partName = data


class Main(QtGui.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        # build ui
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # connect signals
        # self.ui.pushButton.connect(self.on_button)
        self.ui.progressBar.reset()
        self.ui.pushButton.clicked.connect(self.download)

        self.ui.pushButton_2.clicked.connect(self.exitFun)


    def download(self):
        self.ui.progressBar.reset()
        url = str(self.ui.textEdit.toPlainText())
        request = urllib2.Request(url)
        request.get_method = lambda : 'HEAD'

        response = urllib2.urlopen(request)
        response.close()
        # print response.info()
        con_length= response.headers['content-length']
        packet_size = int(con_length)/4
        part1=part2=part3=part4= ''

        threads =[]
        try:
            # t1=Thread(target=download_part,args= ("Thread-1", url,0,packet_size, part1))
            t1 = GetTitleThread("Thread-1", url,0,packet_size, part1)
            threads.append(t1)

            # t2=Thread(target=download_part,args= ("Thread-2", url,packet_size,packet_size*2, part2))
            t2 = GetTitleThread("Thread-2", url,packet_size+1,packet_size*2, part2)
            threads.append(t2)

            # t3=Thread(target=download_part,args= ("Thread-3", url, packet_size*2, packet_size * 3, part3))
            t3 = GetTitleThread("Thread-3", url, packet_size*2+1, packet_size * 3, part3)
            threads.append(t3)

            # t4=Thread(target=download_part,args= ("Thread-4", url, packet_size*3, packet_size *4, part4))
            t4 = GetTitleThread("Thread-4", url, packet_size*3+1, packet_size *4, part4)
            threads.append(t4)

            t1.start()
            t2.start()
            t3.start()
            t4.start()
        except:
            print "Error: unable to start thread"


        for t in threads:
            t.join()

        target = open(str(self.ui.textEdit_2.toPlainText()),'wb')
        data =''
        for t in threads:
            data += t.part
        target.write(data)

        target.close()

        self.ui.progressBar.setValue(100)
        print 'Button clicked!'

    def exitFun(self):
        exit(1)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
