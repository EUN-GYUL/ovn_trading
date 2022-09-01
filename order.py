import time
from PyQt5.QtCore import pyqtSignal,QThread
from collections import deque



class OrderManager(QThread):
    # 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
    pop_order = pyqtSignal(dict)
    orderq = deque()
    
    def __init__(self) -> None:
        super().__init__()
        self.alive = True
    
    def __del__(self):
        self.wait()
        
    
    def run(self)->None:
        while self.alive:
            if not self.orderq.empty() :
                order = self.orderq.get()
                self.pop_order.emit(order)
                time.sleep(0.33)