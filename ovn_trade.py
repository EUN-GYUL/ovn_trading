from multiprocessing import Queue
from tkinter.messagebox import NO
import pandas as pd
from setting import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt



# TODO : 
# 3일 이격도 계산을 위한 DB 

# FIXME:
# 

class Ovn_Worker(QtCore.QThread):
    
    datasent = QtCore.pyqtSignal(dict)
    
    def __init__(self,ovn_q):
        
        super().__init__()
        self.data_q = ovn_q

        self.alive = True
        
    def run(self):

        while self.alive:
            if not self.data_q.empty():
                data = self.data_q.get()
                self.datasent.emit(data)
                
    def put(self,data):
        self.data_q.put(data)


        

    
        
        
    
    
        