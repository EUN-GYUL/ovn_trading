import time
from PyQt5.QtCore import pyqtSignal,QThread
from collections import deque



class OrderManager(QThread):
    # 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
    pop_order = pyqtSignal(dict)
    
    
    def __init__(self,order_ovn_q,today_money) -> None:
        super().__init__()
        self.alive = True
        self.order_q = order_ovn_q
        self.account_dict = {}
        self.today_money = today_money
    
    def __del__(self):
        self.wait()
        
    
    def run(self)->None:
        while self.alive:
            if not self.order_q.empty() :
                code,price = self.order_q.get()
                qty = self.calculate_quantity(price)
                order = [code,price,qty,'1','']
                self.pop_order.emit(order)
                time.sleep(0.33)
                
    
    def set_account_info(self,account_num,acc_data):
        self.account_dict[account_num] = acc_data
        
    
    
    def calculate_quantity(self,price):
        price = (1+ 0.015) * price 
        qty = int( (self.today_money / 10) / price )
        return qty