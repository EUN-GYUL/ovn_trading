
class Condition:
    def __init__(self, name, index) -> None:
        self.name = name
        self.index = index
        self.codelist = []

    def setcondtionlist(self, codelist : list) -> None:
        self.codelist = codelist
        
    def get_cond_list(self):
        if len( self.codelist ) == 0 :
            return None
        return self.codelist
          
    def append(self,code):
        self.codelist.append(code)
    
    def pop(self,code):
        try :
            self.codelist.remove(code)
        except :
            print(" * 조건식 실시간 종목 이탈 오류")
            print(" * 검색식 이름:" ,self.name)
            print(" * 종목 코드:" ,code)
            print(" * 검색식 종목 리스트: ", self.codelist) 
    def isin(self,code):
        return code in self.codelist
    