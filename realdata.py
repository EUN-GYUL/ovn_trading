import threading
import datetime
import numpy as np
import setting
import csv
import psutil

class RealData:
    DATA_FULL_SIZE = 1000 # 데이터가 계속 추가되다 크기가 DATA_FULL_SIZE되면 자동 저장을 실시한다.

    def __init__(self, code: str):
        
        self.code   = code
        self.tick_list = []
                
        now = datetime.datetime.now().strftime("%Y%m%d")
        FileName = f"{now}_{self.code}.csv"
        DirName = 'd:\\Datas\\Data_Kiwoom'
        self.DirFileName = f"{DirName}\\{FileName}" 
        
        
    def get_tick_count(self):
        return len(self.tick_list)
        
    def push(self,realdata):
        
        self.tick_list.append(realdata)
        
        
        if ( len(self.tick_list) > RealData.DATA_FULL_SIZE ):
            t = threading.Thread(target=self._save_data)
            t.start()
        
          
    def _save_data(self):
        
        tick_list = self.tick_list.copy()
        self.tick_list = []
        
        try:
            with open(self.DirFileName,'w') as f:
                wr = csv.writer(f)
                wr.writerows(tick_list)

            print(f"File writting complete : {self.DirFileName} [{self.code}]")
            mem = dict(psutil.virtual_memory()._asdict())
            used_mem = round(mem['used']/(1024*1024))
            print("현재 메모리 사용량 >>",used_mem)
            
        except Exception as e:
            print(f"File writting error : {e}")
            
        
        
        
  


