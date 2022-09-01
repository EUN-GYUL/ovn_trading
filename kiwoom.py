from tkinter.messagebox import NO
from sympy import re
from kiwoomWrapper import *
from PyQt5.QtCore import QCoreApplication
from condition import *
from setting import *
from task import *
import pandas as pd
import realdata
from singleton import Singleton

# TODO : 
# 조건 검색식 편입 이탈 종목 관리

#FIXME : 
# 


class Kiwoom(KiwoomWrapper):
    def __init__(self,ovn_q,ovn_del_q) -> None:
        
        super().__init__()
        self.eventloop = QEventLoop()
        
        self.taskdict = {}
        self.callback = {}
        self.trdata = []
        
        #계좌번호리스트
        self.account_list = []
        self.conditions = {}
        
        self.trmanager = TRReqManager()
        self.trmanager.poptr.connect(self.trRequest)
        self.trmanager.start()
        
        self.df = None
        self.data_dict = {}
        self.datas_ohlc = []

        self.ovn_q = ovn_q
        self.ovn_del_q = ovn_del_q

        
        self.codes = None
        self.datas = {}
        
        self.tr_data = None

        

    
    def _OnEventConnect(self, nErrCode: int):
        '''
        상속을 이용
        별도로 connect를 사용하지 않고 바로 정의함
        '''
        if nErrCode == 0:
            print(f'[OnEventConnect] Login OK')
            
            self.account_list = self.GetLoginInfo('ACCNO').split(";")
            self.account_data = dict.fromkeys(self.account_list)


            self.setCodeList('ALL')
            
            for code in self.codes:
                self.datas[code] = realdata.RealData(code)
            self.regRealItem()
            
                                 
        else:
            QCoreApplication.instance().quit()

        self.eventloop.exit()

    def setCodeList(self, option: str) -> None:
        '''
        코드 리스트를 설정한다.
        
            option
                "ALL"    : 모든 KOSPI와 KOSDAQ종목을 등록한다.
                "KOSPI"  : 모든 KOSPI종목을 등록한다.
                "KOSDAQ" : 모든 KOSDAQ종목을 등록한다.
                "code"   : 코드 한개를 등록한다.
                "code0;code1;code2;...;coden" : 복수개의 코드를 등록한다. 코드간 ";"로 구분한다.
        '''
        
        if option == "ALL":
            codeText = self.GetCodeListByMarket("0") + self.GetCodeListByMarket("10")
            self.codes = codeText[:-1].split(";")
        elif option == "KOSPI":
            codeText = self.GetCodeListByMarket("0")
            self.codes = codeText[:-1].split(";")
        elif option == "KOSDAQ":
            codeText = self.GetCodeListByMarket("10")
            self.codes = codeText[:-1].split(";")
        else:
            try:
                self.codes = option.split(";")
            except:
                self.codes = [option]
    
    def regRealItem(self):
        '''
        self.codes에 저장되어 있는 종목코드를 실시간 등록한다.
        '''
        # 키움은 스크린번호당 100개까지 등록 가능
        # --> 한 스크린 번호당 100개씩 등록한다.
        
        nLength   = len(self.codes) # 전체 종목수
        nReqScrNo = int(nLength / 100) + 1 # 100개 단위 필요 스크린 수, +1 --> 100개 단위를 모으고 남은 자투리 항목용
        
        for i in range(nReqScrNo):
            sScreenNo = f"7{i:03}" # 스크린 이름, 이름은 서로 구분만 되면 됨
            start = i*100
            end = start + 100
            sCodes = ";".join(self.codes[start:end]) # 100개의 종목 문자열을 하나의 문자열로 만든다.
            
            sFidList = '20;10;11;12;27;28;15;13;14;16;17;18;25;26;29;30;31;32;228;311;290;691;567;568'                
            self.SetRealReg(sScreenNo,sCodes,sFidList,"0")
            
            
    
    
    
    def _OnReceiveMsg(self, sScreenNo: str, sRqName: str, sTrCode: str, sMsg: str) -> None:
        print(f'[OnReceiveMsg] TR={sTrCode}, sRqName={sRqName}, sMsg={sMsg}')
        
    
    def _OnReceiveRealData(self, sCode: str, sRealType: str, sRealData: str) -> None:
        
        if sRealType == '주식체결':
            
            try :
                if sCode in self.conditions['종가배팅_이격도3+주가중심선'].get_cond_list() :
                    data = []
                    
                    for id in real_data_fid:
                        data.append(self.GetCommRealData(sCode,int(id)))
                        
                    data.insert(0,sCode)
                    data.insert(1,self.GetMasterCodeName(sCode))
                    
                    ovn_data = dict( zip(OVN_COL,data) )
                    self.ovn_q.put(ovn_data)
                
                realdata = []
                for id in REAL_Fid_List.split(";"):
                    realdata.append(self.GetCommRealData(sCode,int(id)))
                self.datas[sCode].push(realdata)
            except :
                print("_OnReceiveRealData 예외 발생")

            
            
    def _OnReceiveTrData(self, sScreenNo: str, sRqName: str, sTrCode: str, sRecordName: str, sPrevNext: str, *NotUsed) -> None:
        
        '''
        sRqName을 Request ID용으로 사용한다.
        '''
        print(f'[OnReceiveTrData] TR={sTrCode}, sRqName={sRqName}, sPrevNext={sPrevNext}')
        
        task_id = sRqName

        try:
            
            if sTrCode == 'opt10081':
                return self.callback[task_id](sScreenNo, sRqName, sTrCode, sRecordName, sPrevNext)

            if sPrevNext == '0':
                del self.callback[task_id]
        except KeyError as e:
            print(e, sRqName)
        
        
    def _OnReceiveConditionVer(self, lRet: int, sMsg: str):
        if (lRet == 1):
            namelist = self.GetConditionNameList()
            namelist = namelist.split(";")
            del namelist[-1]
            for name in namelist:
                self.conditions[name.split("^")[1]] = Condition(name.split("^")[1], name.split("^")[0])
                print(name.split("^")[1], name.split("^")[0])
            print("조건식 로드 성공")
            
        else:
            print("조건식 로드 실패")
        
        self.eventloop.exit()
            
            
    def _OnReceiveTrCondition(self, sScreenNo: str, sCodeList: str, sConditionName: str, nIndex: int,nNext: int):
    
        sCodeList = sCodeList[:-1]
        codelist = sCodeList.split(";")
        del codelist[-1]
        self.conditions[sConditionName].setcondtionlist(codelist)
        self.eventloop.exit()
        
    def _OnReceiveChejanData(self, sGubun: str, nItemCnt: int, sFidList: str) -> None:

        if sGubun == '0': #체결
            pass

            
        if sGubun == '1': #잔고통보:
            pass


    
    def _OnReceiveRealCondition(self, sCode: str, sType: str, sConditionName: str, sConditionIndex: str) -> None:
        
        
        #편입
        if sType == 'I':
            print("*** 새로운 종목 편입:",self.GetMasterCodeName(sCode))
            self.conditions[sConditionName].append(sCode)
            print(sConditionName , "종목 개수" , len(self.conditions[sConditionName].get_cond_list()))
            self.SetRealReg(scr_no_dict['조건식실시간'],sCode,";".join(real_data_fid),'1')
        #이탈
        else :
            try :
                print("*** 종목 이탈:",self.GetMasterCodeName(sCode))
                self.conditions[sConditionName].pop(sCode)
                print(sConditionName , "종목 개수" , len(self.conditions[sConditionName].get_cond_list()))
                self.SetRealRemove(scr_no_dict['조건식실시간'],sCode)
                self.ovn_del_q.put(sCode)
            except TypeError as e:
                print(e)
            
            
    def trRequest(self, task: Task) -> int:
            
        '''
        task 큐에서 넘어온 task에서 각 입력 데이터들을 처리한다.
        '''
        
        for field, value in task.paramtr.items():
            self.SetInputValue(field, value)

        ret = self.CommRqData(*task.paramrq)
        print(task.paramrq)

        self.taskdict[task.id] = task  # TR 연속처리시 재사용하기 위함
        

        return ret
    
    def request_ohlc_day(self,day,stockcode):
        
        task = Task()
        
        task.trcode = "opt10081"
        task.paramtr['종목코드'] = stockcode
        task.paramtr['기준일자'] = day
        task.paramtr['수정주가구분'] = '1'
        
        
        # CommRqData 파라미터 설정용. [sRqName, sTrCode, nPrevNext, sScreenNo] 순으로 설정한다.
        task.paramrq = [task.id , task.trcode, '0', '5000']
        self.callback[task.id] = self.reply_ohlc_day 
        self.trmanager.push(task)       

    def reply_ohlc_day(self,sScreenNo: str, sRqName: str, sTrCode: str, sRecordName: str, sPrevNext: str):
        
        self.datas_ohlc = []
        for i in range(3):
            data = []
            종목코드 = self.GetCommData(sTrCode,sRqName,i,"종목코드")
            data.append(종목코드)
            data.append(self.GetCommData(sTrCode,sRqName,i,"일자"))
            close = int( self.GetCommData(sTrCode,sRqName,i,"현재가"))
            data.append(close)
            data.append(self.GetCommData(sTrCode,sRqName,i,"거래량"))
            data.append(self.GetCommData(sTrCode,sRqName,i,"거래대금"))
            data.append(self.GetCommData(sTrCode,sRqName,i,"고가"))
            data.append(self.GetCommData(sTrCode,sRqName,i,"저가"))
            self.datas_ohlc.append(data)        
        self.eventloop.exit()
    
    def get_curprice(self,code):
        task = Task()
        
        task.trcode = "opt10001"
        task.paramtr['종목코드'] = code

                
        # CommRqData 파라미터 설정용. [sRqName, sTrCode, nPrevNext, sScreenNo] 순으로 설정한다.
        task.paramrq = [task.id , task.trcode, '0',scr_no_dict["opt10001"] ]
        self.callback[task.id] = self.reply_curprice 
        self.trmanager.push(task)      
    
    
    def reply_curprice(self,sScreenNo: str, sRqName: str, sTrCode: str, sRecordName: str, sPrevNext: str): 
        pass
    
    
    def request_account_info(self,acccount_number):
        task = Task()
        
        task.trcode = "OPW00004"
        task.paramtr['계좌번호'] = acccount_number
        task.paramtr['상장폐지조회구분'] = "1"
        task.paramtr['비밀번호입력매체구분'] = 00
    
        task.paramrq = [task.id , task.trcode, '0',scr_no_dict["opt10001"] ]
        self.callback[task.id] = self.reply_account_info 
        self.trmanager.push(task)    
    
    def reply_account_info(self,sScreenNo: str, sRqName: str, sTrCode: str, sRecordName: str, sPrevNext: str): 
        
        data = []
        for col in ACCOUNT_COL:
            data.append(self.GetCommData(sTrCode,sRqName,0,col))
                

    def get_cond_code_list(self,cond_name):
        return self.conditions[cond_name].get_cond_list()
    
    def get_ohlc(self):
        return self.datas_ohlc
    
from multiprocessing import Queue
from ovntable import *
            
class Kiwoom_Wrapper(metaclass = Singleton):
    
    
    def __init__(self,ovn_q,ovn_del_q) -> None:
        

        
        self.kiwoom = Kiwoom(ovn_q,ovn_del_q)
        
        
        print('>> Login Start.')
        self.kiwoom.CommConnect()
        self.kiwoom.eventloop.exec()
        
        self.isload_cond = False
        if self.load_condition_list() == 1 :
            self.isload_cond = True
        
        codes = self.get_cond_list('종가배팅_이격도3+주가중심선','000')
        self.ovn_table = OvntableWidget(ovn_q,ovn_del_q,codes)
        self.ovn_table.show()
        
        
        
    def load_condition_list(self):
        
        ret = self.kiwoom.GetConditionLoad()
        self.kiwoom.eventloop.exec()
        return ret
        
    def get_cond_list(self,cond_name,cond_idx):
        
        self.kiwoom.SendCondition(scr_no_dict['조건식조회'],cond_name ,cond_idx , 1)
        self.kiwoom.eventloop.exec()
        codes = self.kiwoom.conditions[cond_name].get_cond_list()
        self.kiwoom.SetRealReg('0002',';'.join(codes),';'.join(real_data_fid),0)
        
        return codes 
    
    #우선 종배로 테스트
    def get_ohlc(self,day,code,interval = 'day'):
        
        self.kiwoom.request_ohlc_day(day,code)
        self.kiwoom.eventloop.exec()
        return self.kiwoom.get_ohlc()
    
    def get_account_info(self,account):
        self.kiwoom.request_account_info(account)
        self.kiwoom.eventloop.exec()
        return self.kiwoom.account_data[account]
        
        
        
            