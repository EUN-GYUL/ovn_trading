from multiprocessing import Queue
import multiprocessing as mp
from dbmanager import * 
import threading
from PyQt5 import QtCore
from kiwoom import Kiwoom_Wrapper
from ovn_trade import *
import setting 
import time



class Ovn_Producer():
    
    BUY_START_TIME = '130000'
    BUY_END_TIME = '152000'
    SELL_START_TIME = '085000'
    SELL_END_TIME = '100000'
    BUY_STOCK_COUNT = 10
    _buy_count = 0
    
    
    def __init__(self,data_q ,delete_q , to_worker_q, ovn_order_q, codes ):
        
        super().__init__()
        
        self.data_q = data_q
        self.delete_q = delete_q
        self.to_worker_q = to_worker_q
        self.ovn_order_q = ovn_order_q
        
        self.alive = True
        self.data_dict = dict.fromkeys(codes)
        self.order_dict = {}
        self.available_buy_count = self.BUY_STOCK_COUNT
        
        self.db = DatabaseMgr()
        t = threading.Thread(target = self.db.read_data_by_count)
        t.start()
        
        print("Reading Db Start")
        t.join()
        print("Reading Db Done")
        self.db_df = self.db.get_data()
        
        print( self.get_rank() )
        
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
    
    def get_rank(self,row_bd = 10 ,cat = 'amount',window = 3 ,reverse = True):
        
        """_summary_
        
        
        
        
        
        
        
        Args:
            row_bd (int, optional): 가장 낮은 순위 . Defaults to 10.
            cat (str, optional): 범주 amount(거래대금),marketCap(시가총액),ppo(이격도) . Defaults to 'amount'.
            window : 기간
            reverse : 내림차순 True 오름차순 False
        return 
            DataFrame
        """
        rename = cat+"_rank" 
        new_col = self.db_df.sort_values(by='logDate',ascending=False).groupby('stockCode')[cat].rolling(window,min_periods = 1 ).mean().rename(rename).reset_index(drop = True, level = 0)
        df = pd.concat([self.db_df,new_col],axis=1)
        
        return df.nlargest(row_bd,rename,keep='all')
    
    def run(self):
        
        while self.alive:
            
            if not self.data_q.empty() :
                data = self.data_q.get()
                self.update_data_dict(data)
        
            if not self.delete_q.empty() :
                code = self.delete_q.get()
                self.delete_data_dict(code)
            
            self.to_worker_q.put(self.data_dict)
            time.sleep(0.01)
            self.buy()
    
    def buy(self):
        
        """
        _summary_
        매수시간부터 매수종목갯수 될 때까지 매수함
        10종목 넘으면 3일 이격도 순으로 매수
        
        """
        now = int( datetime.datetime.now().time().strftime("%H%M%S") )
        
        if  self.available_buy_count > 0 and None not in self.data_dict.values() and now >= int(self.BUY_START_TIME) and now <= int(self.BUY_END_TIME) and self._buy_count < self.BUY_STOCK_COUNT :
            
            buy_stocks = { k:v for k ,v in self.data_dict.items() if k not in self.order_dict.keys() or self.order_dict[k] == 0} 
             
            buy_list = sorted(buy_stocks.items(),key = lambda x : x[1][-1] , reverse =True)
            buy_list = buy_list[:self.available_buy_count]
            for order in buy_list:
                self.sendOrder(order[0],order[1][2])
                self.available_buy_count -= 1
            print("주문 가능한 종목 수 : ",self.available_buy_count)

    def sendOrder(self,code,curPrice):
        self.order_dict[code] = 1
        order = (code,curPrice)
        self.ovn_order_q.put(order)