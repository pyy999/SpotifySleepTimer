import keyboard
import time
import sys
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Worker(QObject):
    done = pyqtSignal()
    update_text = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    start = pyqtSignal(int)
    continue_flag = 0

    def run(self, int):
        self.continue_flag = 1
        i = int
        while i > 0:
            if self.continue_flag == 0:
                return
            self.update_text.emit(i)
            time.sleep(1)
            i -= 1
        self.done.emit()

    def stop(self):
        self.continue_flag = 0


class SleepTimer(QWidget):
    toggle = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.start_stop = QPushButton('Start')
        self.start_stop.clicked.connect(self.toggle)
        self.duration = QLineEdit()
        self.duration.setValidator(QIntValidator())
        self.duration.setAlignment(Qt.AlignRight)
        self.banner = QLabel('SLEEPTIMER :)')
        self.countdown = QLabel()
        self.running = QThread()
        self.label = QLabel('Time (Minutes)')

        self.worker = Worker()
        self.worker.moveToThread(self.running)
        self.worker.start.connect(self.worker.run)
        self.worker.done.connect(self.timerDone)
        self.worker.update_text.connect(lambda x: self.countdown.setText("Nighty night in: " + str(datetime.timedelta(seconds=x))))

        glayout = QGridLayout()
        glayout.addWidget(self.banner, 0, 0, 1, 2)
        glayout.addWidget(self.start_stop, 2, 0, 1, 2)
        glayout.addWidget(self.label, 1, 0, 1, 1)
        glayout.addWidget(self.duration, 1, 1, 1, 1)
        glayout.addWidget(self.countdown, 3, 0, 1, 2)
        self.banner.setAlignment(Qt.AlignCenter)
        self.countdown.setAlignment(Qt.AlignCenter)

        self.setLayout(glayout)
        self.show()
        self.setWindowTitle('SleepTimer')

        self.toggle.connect(self.startTimer)
        self.running.start()

    @pyqtSlot()
    def startTimer(self):
        if not self.duration.text():
            self.countdown.setText('Enter a Time!')
            return
        self.start_stop.setText('Stop')
        self.toggle.disconnect()
        self.toggle.connect(self.stopTimer)
        self.worker.start.emit(int(self.duration.text())*60)

    @pyqtSlot()
    def stopTimer(self):
        self.start_stop.setText('Start')
        self.toggle.disconnect()
        self.toggle.connect(self.startTimer)
        self.countdown.setText('')
        self.worker.stop()

    @pyqtSlot()
    def timerDone(self):
        #print('done')
        self.start_stop.setText('Start')
        self.toggle.disconnect()
        self.toggle.connect(self.startTimer)
        self.countdown.setText('')
        keyboard.press_and_release('play/pause')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.toggle.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SleepTimer()
    w.resize(400, 200)
    sys.exit(app.exec_())

