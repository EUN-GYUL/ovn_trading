from multiprocessing import Queue
import multiprocessing as mp
from dbmanager import * 
import threading
from PyQt5 import QtCore
from ovn_trade import *

class Ovn_Producer():
    
    BUY_START_TIME = '1500'
    BUY_END_TIME = '1520'
    SELL_START_TIME = '0850'
    SELL_END_TIME = '1000'
    BUY_STOCK_COUNT = 10
    _buy_count = 0
    
    
    def __init__(self,data_q : Queue,delete_q : Queue, to_worker_q ,codes : list):
        
        super().__init__()
        
        self.data_q = data_q
        self.delete_q = delete_q
        self.to_worker_q = to_worker_q
        
        self.alive = True
        self.data_dict = dict.fromkeys(codes)
        
        self.db = DatabaseMgr()
        t = threading.Thread(target = self.db.read_data_by_count)
        t.start()
        
        print("Reading Db Start")
        t.join()
        print("Reading Db Done")
        self.db_df = self.db.get_data()
        
        self.run()     
        
    def update_data_dict(self,data):
        ppo = self.get_ppo(data['curPrice'],data['stockCode'])
        data_list = list(data.values())
        data_list.append(ppo)
        self.data_dict[data['stockCode']] = data_list
        
    
        
    
    def delete_data_dict(self,code):
        try:
            self.data_dict.pop(code)
        except:
            print(code,"None Data in data_dict")
        
   
    def get_ppo(self,curPrice,code):
        '''
        이격도 계산 (3일)
        '''
        s = int(curPrice) + sum(self.db_df[ code == self.db_df['stockCode'] ]['priceClose'].tolist())
        m = s / 3
        ppo = ( int(curPrice) / m )*100
        return ppo
    
    def run(self):
        
        while self.alive:
            
            print(mp.current_process() , 'run')
            if not self.data_q.empty() :
                data = self.data_q.get()
                self.update_data_dict(data)
        
            if not self.delete_q.empty() :
                code = self.delete_q.get()
                self.delete_data_dict(code)
            
            self.to_worker_q.put(self.data_dict)
    
    def buy(self):
        
        """
        _summary_
        매수시간부터 매수종목갯수 될 때까지 매수함
        10종목 넘으면 3일 이격도 순으로 매수
        
        """
        now = datetime.datetime.now().time().strftime("%H%M%S")
        
        if now >= int(self.BUY_START_TIME) and now <= int(self.BUY_END_TIME) and self._buy_count < self.BUY_STOCK_COUNT:

            #3일 이격도 내림차순으로 정렬                
            buy_list = sorted(self.data_dict.items(),key = lambda x : x[1][-1] , reverse =True)
            buy_list = buy_list[:10][0]

    def sendOrder(self,code):
        pass 