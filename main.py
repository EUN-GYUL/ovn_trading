from tkinter.messagebox import NO
from kiwoom import Kiwoom, Kiwoom_Wrapper
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication
import sys
from ovntable import OvntableWidget
import setting
from multiprocessing import Queue
import multiprocessing as mp





if __name__ == "__main__":
    
    app = QApplication(sys.argv)

    ovn_del_q = Queue()
    ovn_q = Queue()
    ovn_order_q = Queue()

    kiwoom = Kiwoom_Wrapper(ovn_q,ovn_del_q,ovn_order_q)
    
    codes = kiwoom.get_cond_list('종가배팅_이격도3+주가중심선','000')
    
    print(codes)
    ovn_table = OvntableWidget(ovn_q,ovn_del_q,ovn_order_q,codes)
    ovn_table.show()

    

    exit(app.exec_())
    
    
