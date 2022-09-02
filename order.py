import time
from PyQt5.QtCore import pyqtSignal,QThread
from collections import deque



class OrderManager(QThread):
    # 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
    pop_order = pyqtSignal(dict)
    
    
    def __init__(self,order_ovn_q) -> None:
        super().__init__()
        self.alive = True
        self.order_q = order_ovn_q
    
    def __del__(self):
        self.wait()
        
    
    def run(self)->None:
        while self.alive:
            if not self.order_q.empty() :
                order = self.order_q.get()
                self.pop_order.emit(order)
                time.sleep(0.33)