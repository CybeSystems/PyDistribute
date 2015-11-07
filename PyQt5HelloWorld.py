import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.executable), 'DLLs'))
sys.path.append(os.path.join(os.path.dirname(sys.executable), 'DLLs\\psutil'))

print(os.path.join(os.path.dirname(sys.executable), 'DLLs\\psutil'))
#Try some hooks_

import psutil
print(psutil.cpu_times())

print ("PsUtil failed")

from PyQt5 import QtWidgets

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    button = QtWidgets.QPushButton("Hello, PyQt!")
    window.setCentralWidget(button)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()