from kiwoom import Kiwoom, Kiwoom_Wrapper
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication
import sys
from ovntable import OvntableWidget
from setting import *
from multiprocessing import Queue
import multiprocessing as mp

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    kiwoom_w = Kiwoom_Wrapper()

    exit(app.exec_())
    
    
