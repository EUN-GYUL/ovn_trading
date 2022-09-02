import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from ovn import *
import multiprocessing as mp
from multiprocessing import Queue

class OvntableWidget(QWidget):
    
    def __init__(self,data_q,del_q,order_q,codes , parent = None ) -> None:
        super().__init__(parent)
        uic.loadUi("ovn_table.ui", self)
        
        toWorker_q = Queue()
        self.ovn_proc = mp.Process(target=Ovn_Producer,args = (data_q,del_q,toWorker_q,order_q,codes) )
        
        self.ovn_worker = Ovn_Worker(toWorker_q)
        self.ovn_worker.datasent.connect(self.update_table)
        
        self.ovn_proc.start()
        self.ovn_worker.start()
             
        
        

    def update_table(self,data):
        
        self.ovntable.setRowCount(len(data))
        self.ovntable.setColumnCount(len(OVN_COL))

        try:
            for i, row in enumerate(data.values()):
                for j , data in enumerate(row):

                        item = QTableWidgetItem(str(data))
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                        self.ovntable.setItem(i,j,item) 
        except:
            pass
            
            # for j in range(len(OVN_COL)):
            #     item = QTableWidgetItem(str(str(row[j])))
            #     item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            #     self.ovntable.setItem(i,j,item)

    

    