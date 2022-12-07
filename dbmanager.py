from sqlalchemy import create_engine
import pandas as pd
import datetime

class DatabaseMgr():
    
    def __init__(self) -> None:
        try:
            self.engine = create_engine("mssql+pyodbc://DESKTOP-EKFU39H/stock?driver=SQL+Server", echo=False)
        except:
            print("db 엔진 초기화 실패")
        self.db_data = None
        self.t = None
           
    def read_data(self, table ,start ,end):
        
        q = f"select * from {table} where logdate between {start} and {end}"

        try:
            self.db_data = pd.read_sql_query(q, con=self.engine)
            print(table,len(self.db_data),"개 자료 ","읽기 완료")            
        except:
            print("db 읽기 에러")
        self.db_data['stockCode'] = self.db_data['stockCode'].apply(lambda x : x[1:])
    
    def read_data_by_count(self,table = 'logday',count = 3):
        
        now = datetime.datetime.today() - datetime.timedelta(days=7)
        weekago = int( now.strftime("%Y%m%d") )
        q= f'''
            select * from ( select * , ROW_NUMBER() OVER ( partition by stockCode order by logdate desc ) 
                as rownum from {table}
                where logdate > {weekago}
                ) a
                where a.rownum between 2 and {count} 
            '''

        try:
            self.db_data = pd.read_sql_query(q, con=self.engine)
            self.db_data['stockCode'] = self.db_data['stockCode'].apply(lambda x : x[1:])
            print(table,len(self.db_data),"개 자료 ","읽기 완료")
            print(self.db_data.head())         
        except:
            print("db 읽기 에러")
        
          
    def get_data(self):
        return self.db_data
