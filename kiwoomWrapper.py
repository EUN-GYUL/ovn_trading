from PyQt5.QtCore import *
from PyQt5 import QAxContainer
from singleton import Singleton

class KiwoomWrapper(QAxContainer.QAxWidget):

    __slots__ = ('name', 'path', 'mode')

    progID = 'KHOPENAPI.KHOpenAPICtrl.1'
    CLSID = '{A1574A0D-6BFA-4BD7-9020-DED88711818D}'

    def __init__(self) -> None:
        super().__init__()

        self.setControl(self.__class__.progID)

        '''
        이벤트 시그널 연결

        상속을 이용하여 이벤트 함수를 재사용할 수 있다.

        On~으로 시작하는 이벤트들은 객체이므로 이벤트 동작 함수는 동일이름이 되지 않게 정의한다.
        만약 동일 이름으로 정의하면 상속되어지는 클래스에서 On~.connect를 사용할 수 없다. 
        '''

        self.OnEventConnect.connect(self._OnEventConnect)
        self.OnReceiveChejanData.connect(self._OnReceiveChejanData)
        self.OnReceiveConditionVer.connect(self._OnReceiveConditionVer)
        self.OnReceiveMsg.connect(self._OnReceiveMsg)
        self.OnReceiveRealCondition.connect(self._OnReceiveRealCondition)
        self.OnReceiveRealData.connect(self._OnReceiveRealData)
        self.OnReceiveTrCondition.connect(self._OnReceiveTrCondition)
        self.OnReceiveTrData.connect(self._OnReceiveTrData)

    def __del__(self) -> None:
        if self.control() != '':
            self.SetRealRemove('ALL', 'ALL')

    ##########################################
    #
    # Kiwoom Function Wrapper
    #
    ##########################################

    # 로그인 버전처리

    def CommConnect(self) -> int:
        '''
        LONG CommConnect()

        수동 로그인설정인 경우 로그인창을 출력해서 로그인을 시도하거나
        자동로그인 설정인 경우 로그인창 출력없이 로그인을 시도합니다.

        반환값
            0 : 성공
            음수값은 실패

        ※ 동일 프로세스 내에서 객체를 여러개를 생성해도 로그인 상태는 서로 공유한다.
        '''
        return self.dynamicCall('CommConnect()')

    def CommTerminate(self) -> None:
        '''
        void CommTerminate()

        더 이상 사용할 수 없는 함수입니다.
        '''

    def GetConnectState(self) -> int:
        '''
        LONG GetConnectState()

        현재 로그인 상태를 알려줍니다.

        반환값
            1: 연결
            0: 연결안됨
        '''
        return self.dynamicCall('GetConnectState()')

    def GetLoginInfo(self, sTag: str) -> str:
        '''
        BSTR GetLoginInfo(BSTR sTag)

            sTag : 사용자 정보 구분 TAG값 (비고)

        로그인 후 사용할 수 있으며 인자값에 대응하는 정보를 얻을 수 있습니다.
        인자는 다음값을 사용할 수 있습니다.

            'ACCOUNT_CNT'          : 보유계좌 수를 반환합니다.
            'ACCLIST' 또는 'ACCNO' : 구분자 ';'로 연결된 보유계좌 목록을 반환합니다.
            'USER_ID'              : 사용자 ID를 반환합니다.
            'USER_NAME'            : 사용자 이름을 반환합니다.
            'KEY_BSECGB'           : 키보드 보안 해지여부를 반환합니다.(0 : 정상, 1 : 해지)
            'FIREW_SECGB'          : 방화벽 설정여부를 반환합니다.(0 : 미설정, 1 : 설정, 2 : 해지)
            'GetServerGubun'       : 접속서버 구분을 반환합니다.(1 : 모의투자, 나머지 : 실서버)

        [보유계좌 목록 예시]

            CString strAcctList = GetLoginInfo('ACCLIST');

            여기서 strAcctList는 ';'로 분리한 보유계좌 목록임
            예) '3040525910;567890;3040526010'

        반환값
            TAG값에 따른 데이터 반환
        '''
        return self.dynamicCall('GetLoginInfo(str)', [sTag]).strip()

    # @ 이벤트 함수

    def _OnEventConnect(self, nErrCode: int) -> None:
        '''
        void OnEventConnect(LONG nErrCode);

            nErrCode : 로그인 상태를 전달하는데 자세한 내용은 아래 상세내용 참고

        로그인 처리 이벤트입니다.
        성공이면 인자값 nErrCode가 0이며 에러는 다음과 같은 값이 전달됩니다.

        nErrCode별 상세내용
            -100 : 사용자 정보교환 실패
            -101 : 서버접속 실패
            -102 : 버전처리 실패
        '''

    def _OnReceiveMsg(self, sScreenNo: str, sRQName: str, sTrCode: str, sMsg: str) -> None:
        '''
        void OnReceiveMsg(LPCTSTR sScreenNo, LPCTSTR sRQName, LPCTSTR sTrCode, LPCTSTR sMsg)

            sScreenNo : 화면번호
            sRQName   : 사용자 구분명
            sTrCode   : TR이름
            sMsg      : 서버에서 전달하는 메시지

        서버통신 후 수신한 메시지를 알려줍니다.
        메시지에는 6자리 코드번호가 포함되는데 이 코드번호는 통보없이 수시로 변경될 수 있습니다.
        따라서 주문이나 오류관련처리를 이 코드번호로 분류하시면 안됩니다.
        '''

    # 조회와 실시간데이터처리

    def CommRqData(self, sRqName: str, sTrCode: str, nPrevNext: int, sScreenNo: str) -> int:
        '''
        LONG CommRqData(BSTR sRQName, BSTR sTrCode, long nPrevNext, BSTR sScreenNo)

            sRQName   : 사용자 구분명
            sTrCode   : 조회하려는 TR이름
            nPrevNext : 연속조회여부
            sScreenNo : 화면번호

        조회요청함수이며 빈번하게 조회요청하면 시세과부하 에러값으로 -200이 전달됩니다.

        반환값
            0이면 조회요청 정상 나머지는 에러
                -200 (OP_ERR_SISE_OVERFLOW)  - 과도한 시세조회로 인한 통신불가
                -201 (OP_ERR_RQ_STRUCT_FAIL) - 입력 구조체 생성 실패
                -202 (OP_ERR_RQ_STRING_FAIL) - 요청전문 작성 실패
                   0 (OP_ERR_NONE)           - 정상처리
        '''
        return self.dynamicCall('CommRqData(str, str, int, str)', [sRqName, sTrCode, nPrevNext, sScreenNo])

    def SetInputValue(self, sId: str, sValue: str) -> None:
        '''
        void SetInputValue(BSTR sID, BSTR sValue)

            sID    : TR에 명시된 Input이름
            sValue : Input이름으로 지정한 값

        조회요청시 TR의 Input값을 지정하는 함수이며
        조회 TR 입력값이 많은 경우 이 함수를 반복적으로 호출합니다.

        [OPT10081 : 주식일봉차트조회요청예시]

            SetInputValue('종목코드'    ,  '039490'); // 첫번째 입력값 설정
            SetInputValue('기준일자'    ,  '20160101');// 두번째 입력값 설정
            SetInputValue('수정주가구분'  ,  '1'); // 세번째 입력값 설정
            LONG lRet = CommRqData( 'RQName','OPT10081', '0','0600');// 조회요청
        '''
        self.dynamicCall('SetInputValue(str, str)', [sId, sValue])

    def DisconnectRealData(self, sScreenNo: str) -> None:
        '''
        void DisconnectRealData(LPCTSTR sScreenNo)

            sScreenNo : 화면번호[4]

        화면번호 설정한 실시간 데이터를 해지합니다.

        화면을 종료할 때 반드시 위 함수를 호출해야 한다.

        Ex) openApi.DisconnectRealData('0101');
        '''
        self.dynamicCall('DisconnectRealData(str)', [sScreenNo])

    def GetRepeatCnt(self, sTrCode: str, sRecordName: str) -> int:
        '''
        LONG GetRepeatCnt(LPCTSTR sTrCode, LPCTSTR sRecordName)

            sTrCode     : TR 이름
            sRecordName : 레코드 이름

        조회수신한 멀티데이터의 갯수(반복)수를 얻을수 있습니다.
        예를들어 차트조회는 한번에 최대 900개 데이터를 수신할 수 있는데
        이렇게 수신한 데이터갯수를 얻을때 사용합니다.
        이 함수는 반드시 OnReceiveTRData()이벤트가 호출될때 그 안에서 사용해야 합니다.

        [OPT10081 : 주식일봉차트조회요청예시]

            OnReceiveTrDataKhopenapictrl(...)
            {
                if(strRQName == _T('주식일봉차트'))
                {
                    int nCnt = OpenAPI.GetRepeatCnt(sTrcode, strRQName);
                    for (int nIdx = 0; nIdx < nCnt; nIdx++)
                    {
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('종목코드'));   strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('거래량'));   strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('시가'));   strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('고가'));   strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('저가'));   strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('현재가'));   strData.Trim();
                    }
                }
            }

        반환값
            레코드의 반복횟수
        '''
        return self.dynamicCall('GetRepeatCnt(str, str)', [sTrCode, sRecordName])

    def CommKwRqData(self, sArrCode: str, bNext: bool, nCodeCount: int, nTypeFlag: int, sRQName: str,
                     sScreenNo: str) -> int:
        '''
        LONG CommKwRqData(LPCTSTR sArrCode, BOOL bNext, int nCodeCount, int nTypeFlag, LPCTSTR sRQName, LPCTSTR sScreenNo)

            sArrCode   : 조회하려는 종목코드 리스트, 한번에 100종목까지 조회가능하며 종목코드사이에 세미콜론(;)으로 구분.
            bNext      : 연속조회 여부 0:기본값, 1:연속조회(지원안함), api 문서는 bool 타입이지만, int로 처리(0: 조회, 1: 남은 데이터 이어서 조회)
            nCodeCount : 종목코드 갯수
            nTypeFlag  : 0:주식 관심종목, 3:선물옵션 관심종목
            sRQName    : 사용자 구분명
            sScreenNo  : 화면번호

        한번에 100종목을 조회할 수 있는 관심종목 조회함수인데
        영웅문HTS [0130] 관심종목 화면과는 이름만 같은뿐 전혀관련이 없습니다.
        함수인자로 사용하는 종목코드 리스트는 조회하려는 종목코드 사이에 구분자';'를 추가해서 만들면 됩니다.
        조회데이터는 관심종목정보요청(OPTKWFID) Output을 참고하시면 됩니다.
        이 TR은 CommKwRqData()함수 전용으로 임의로 사용하시면 에러가 발생합니다.

        복수종목조회 메서드(관심종목조회 메서드라고도 함).

        이 메서드는 setInputValue() 메서드를 이용하여, 사전에 필요한 값을 지정하지 않는다.
        단지, 메서드의 매개변수에서 직접 종목코드를 지정하여 호출하며,
        데이터 수신은 receiveTrData() 이벤트에서 아래 명시한 항목들을 1회 수신하며,
        이후 receiveRealData() 이벤트를 통해 실시간 데이터를 얻을 수 있다.

        복수종목조회 TR 코드는 OPTKWFID임.

        반환값
            OP_ERR_RQ_STRING - 요청 전문 작성 실패
            OP_ERR_NONE      - 정상처리

        '''
        return self.dynamicCall('CommKwRqData(str, int, int, int, str, str)',
                                [sArrCode, bNext, nCodeCount, nTypeFlag, sRQName, sScreenNo])

    def GetCommData(self, sTrCode: str, sRecordName: str, nIndex: int, sItemName: str) -> str:
        '''
        BSTR GetCommData(LPCTSTR sTrCode, LPCTSTR sRecordName, long nIndex, LPCTSTR strItemName)

            sTrCode     : TR 이름
            sRecordName : 레코드이름
            nIndex      : TR반복부, 복수데이터 인덱스
            sItemName   : TR에서 얻어오려는 출력항목이름

        OnReceiveTRData()이벤트가 호출될때 조회데이터를 얻어오는 함수입니다.
        이 함수는 반드시 OnReceiveTRData()이벤트가 호출될때 그 안에서 사용해야 합니다.

        Ex)현재가출력 - openApi.GetCommData('OPT00001', '주식기본정보', 0, '현재가');

        ※ TR Request에 대해 OUTPUT은 싱글데이터와 멀티데이터가 있는 경우가 있음
           이때 데이터 취득에는 싱글과 멀티의 구분이 필요없음
           단순히 출력항목이름으로 데이터를 취득하면됨

           예) opt10080 : 주식분봉차트조회
               싱글데이터 '종목코드' : openApi.GetCommData('opt10080', '주식분차트', 0, '종목코드');

        ※※ sRecordName은 TR목록에서 확인할 수 있지만 정확히 쓰지 않아도 데이터를 취득할 수 있음
             출력항목이름으로 데이터를 가져오는 것 같음, 단 sTrCode는 틀리면 안됨

        [OPT10081 : 주식일봉차트조회요청예시]

            OnReceiveTrDataKhopenapictrl(...)
            {
                if(strRQName == _T('주식일봉차트'))
                {
                    int nCnt = OpenAPI.GetRepeatCnt(sTrcode, strRQName);
                    for (int nIdx = 0; nIdx < nCnt; nIdx++)
                    {
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('종목코드')); strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('거래량'));   strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('시가'));     strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('고가'));     strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('저가'));     strData.Trim();
                        strData = OpenAPI.GetCommData(sTrcode, strRQName, nIdx, _T('현재가'));   strData.Trim();
                    }
                }
            }

        반환값
            수신 데이터
        '''
        return self.dynamicCall('GetCommData(str, str, int, str)', [sTrCode, sRecordName, nIndex, sItemName]).strip()

    def GetCommRealData(self, sCode: str, nFid: int) -> str:
        '''
        BSTR GetCommRealData(LPCTSTR sCode, long nFid)

            sCode : 종목코드
            Fid   : 실시간 타입에 포함된FID

        OnReceiveRealData()이벤트가 호출될때 실시간데이터를 얻어오는 함수입니다.
        이 함수는 반드시 OnReceiveRealData()이벤트가 호출될때 그 안에서 사용해야 합니다.

        Ex) 현재가출력 - openApi.GetCommRealData('039490', 10);
        참고) sCode는 OnReceiveRealData 첫번째 매개변수를 사용

        [주식체결 실시간 데이터 예시]

            if(strRealType == _T('주식체결'))
            {
                strRealData = m_KOA.GetCommRealData(strCode, 10);   // 현재가
                strRealData = m_KOA.GetCommRealData(strCode, 13);   // 누적거래량
                strRealData = m_KOA.GetCommRealData(strCode, 228);    // 체결강도
                strRealData = m_KOA.GetCommRealData(strCode, 20);  // 체결시간
            }

        반환값
            수신 데이터
        '''
        return self.dynamicCall('GetCommRealData(str, int)', [sCode, nFid]).strip()

    def GetCommDataEx(self, sTrCode: str, sRecordName: str) -> list:
        '''
        VARIANT GetCommDataEx(LPCTSTR sTrCode, LPCTSTR sRecordName)

        sTrCode     : TR 이름
        sRecordName : 레코드이름

        조회 수신데이터 크기가 큰 차트데이터를 한번에 가져올 목적으로 만든 전용함수입니다.

        ※ 리스트를 반환하고, 리스트 내부는 개별 조회 항목 전체 값의 리스트로 구성되어 있음

            [ [첫번째 조회 항목들], [두번째 조회 항목들], ..., [n번째 조회 항목들] ]

        [차트일봉데이터 예시]

            OnReceiveTrDataKhopenapictrl(...)
            {
                if(strRQName == _T('주식일봉차트'))
                {
                    VARIANT   vTemp = OpenAPI.GetCommDataEx(strTrCode, strRQName);
                    long    lURows, lUCols;
                    long    nIndex[2]
                    COleSafeArray saMatrix(vTemp);
                    VARIANT vDummy;

                    VariantInit(&vDummy);
                    saMatrix.GetUBound(1, &lURows); // 데이터 전체갯수(데이터 반복횟수)
                    saMatrix.GetUBound(2, &lUCols); // 출력항목갯수

                    for(int nRow = 0; nRow <= lURows; nRow ++)
                    {
                        for(int nCol = 0; nCol <= lUCols; nCol ++)
                        {
                            nIndex[0] = lURows;
                            nIndex[1] = lUCols;
                            saMatrix.GetElement(nIndex, &vDummy);
                            ::SysFreeString(vDummy.bstrVal);
                        }
                    }
                    saMatrix.Clear();
                    VariantClear(&vTemp);
                }
            }
        '''
        return self.dynamicCall('GetCommDataEx(str, str)', [sTrCode, sRecordName])

    # @ 이벤트 함수

    def _OnReceiveTrData(self, sScreenNo: str, sRqName: str, sTrCode: str, sRecordName: str, sPrevNext: str,
                         nDataLength: int, sErrorCode: str, sMessage: str, sSplmMsg: str) -> None:
        '''
        void OnReceiveTrData(LPCTSTR sScreenNo, LPCTSTR sRQName, LPCTSTR sTrCode, LPCTSTR sRecordName, LPCTSTR sPreNext, LONG nDataLength, LPCTSTR sErrorCode, LPCTSTR sMessage, LPCTSTR sSplmMsg)

            sScreenNo   : 화면번호
            sRQName     : 사용자 구분명
            sTrCode     : TR이름
            sRecordName : 레코드 이름
            sPrevNext   : 연속조회 유무를 판단하는 값 0: 연속(추가조회)데이터 없음, 2:연속(추가조회) 데이터 있음
            nDataLength : 사용안함.
            sErrorCode  : 사용안함.
            sMessage    : 사용안함.
            sSplmMsg    : 사용안함.

        조회요청 응답을 받거나 조회데이터를 수신했을때 호출됩니다.
        조회데이터는 이 이벤트내부에서 GetCommData()함수를 이용해서 얻어올 수 있습니다.

        sRQName – CommRqData의 sRQName과 매핑되는 이름이다.
        sTrCode – CommRqData의 sTrCode과 매핑되는 이름이다.
        '''

    def _OnReceiveRealData(self, sCode: str, sRealType: str, sRealData: str) -> None:
        '''
        void OnReceiveRealData(LPCTSTR sCode, LPCTSTR sRealType, LPCTSTR sRealData)

        sCode     : 종목코드
        sRealType : 리얼타입
        sRealData : 실시간 데이터 전문

        실시간 데이터 수신할때마다 호출되며 SetRealReg()함수로 등록한 실시간 데이터도 이 이벤트로 전달됩니다.
        GetCommRealData()함수를 이용해서 실시간 데이터를 얻을수 있습니다.

        참고

            실시간으로 전달되는 데이터는 OpenAPI를 포함하여 영웅문4 HTS, 영웅문S MTS 매체들이
            동일한 데이터패킷을 전송받습니다.
            실제로 '주식체결' 타입으로 전달되는 항목들은 40여개 이상이며
            이중에는 HTS에서만 쓰이거나 MTS에서만 쓰이는 항목도 존재합니다.
            KOA스튜디오에는 OpenAPI에서 다루어지는 데이터들만 나열되어있습니다.
        '''

    # 주문과 잔고처리

    def SendOrder(self, sRQName: str, sScreenNo: str, sAccNo: str, nOrderType: int, sCode: str, nQty: int, nPrice: int,
                  sHogaGb: str, sOrgOrderNo: str) -> int:
        '''
        LONG SendOrder( BSTR sRQName, BSTR sScreenNo, BSTR sAccNo, LONG nOrderType, BSTR sCode
            , LONG nQty, LONG nPrice, BSTR sHogaGb, BSTR sOrgOrderNo)

            sRQName     : 사용자 구분명
            sScreenNo   : 화면번호 [4] -> 자리수 4개를 지킬 것
            sAccNo      : 계좌번호 10자리
            nOrderType  : 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
            sCode       : 종목코드
            nQty        : 주문수량
            nPrice      : 주문가격
            sHogaGb     : 거래구분(혹은 호가구분)은 아래 참고
            sOrgOrderNo : 원주문번호입니다. 신규주문에는 공백, 정정(취소)주문할 원주문번호를 입력합니다.

        9개 인자값을 가진 국내 주식주문 함수이며 반환값이 0이면 성공이며 나머지는 에러입니다.
        1초에 5회만 주문가능하며 그 이상 주문요청하면 에러 -308을 리턴합니다.

        [거래구분]
        모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.
            00 : 지정가
            03 : 시장가
            05 : 조건부지정가
            06 : 최유리지정가
            07 : 최우선지정가
            10 : 지정가IOC
            13 : 시장가IOC
            16 : 최유리IOC
            20 : 지정가FOK
            23 : 시장가FOK
            26 : 최유리FOK
            61 : 장전시간외종가
            62 : 시간외단일가매매
            81 : 장후시간외종가

        ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK,
           장전시간외, 장후시간외 주문시 주문가격을 입력하지 않습니다.

        반환값
            에러코드

        [참고 - 주문관련 이벤트,체결응답]

        주문과 관련된 이벤트는 OnReceiveMsg(), OnReceiveTrData(), OnReceiveChejanData()입니다.

        1. OnReceiveMsg()이벤트
            이 이벤트는 주문실패를 포함해서 주문과 관련된 메시지가 전달되며
            주문외에도 일부 계좌관련 조회후 이 이벤트가 호출됩니다.

        2. OnReceiveTrData()이벤트
            이 이벤트에서는 '주문번호'만 확인할 수 있습니다.
            만일 '주문번호'가 공백이면 주문실패이며
            그 원인은 OnReceiveMsg()로 전달되는 메시지 내용을 확인하실수 있습니다.

            OnReceiveTRData이벤트에서 '주문번호' 확인방법을 정리하면 다음과 같습니다.
            조회데이터 처리와 같습니다.

                OnReceiveTRData(sScreenNo, sRqName, sTrCode, ....) // 이벤트 처리부분
                {
                    sData = OpenAPI.GetCommData(sTrCode, sRqName, 0, '주문번호')
                }

            OnReceiveTrData에 넘어오는  TR Code
                'KOA_NORMAL_BUY_KP_ORD'  - 코스피매수
                'KOA_NORMAL_BUY_KQ_ORD'  - 코스닥매수
                'KOA_NORMAL_SELL_KP_ORD' - 코스피매도
                'KOA_NORMAL_SELL_KQ_ORD' - 코스닥매도
                'KOA_NORMAL_KP_CANCEL'   - 코스피취소
                'KOA_NORMAL_KQ_CANCEL'   - 코스닥취소
                'KOA_NORMAL_KP_MODIFY'   - 코스피정정
                'KOA_NORMAL_KQ_MODIFY'   - 코스닥정정

        3. OnReceiveChejanData()이벤트
            주문에 대한 상세정보는 이 이벤트로 전달되는데
            첫번째 인자 sGubun 값이 0이면 주문체결통보가 1이면 잔고통보 데이터가 전달된것입니다.

            만일 주문이 체결되면 체결통보와 잔고통보가 연이어 전달됩니다.

            주문요청에 대한 응답은 주문접수, 주문체결, 잔고수신 순서로 진행됩니다.
            이때 주문번호는 처음 접수되었을 때 한번 부여되지만 체결번호는 체결될 때마다 채번되서 전달됩니다.
            이상의 과정을 간단히 정리하면 다음과 같습니다.

            주문 ---> 접수 ---> 체결1 ---> 잔고1 ---> 체결2 ---> 잔고2... ---> 체결n ---> 잔고n

            OnReceiveChejanData()이벤트에 전달되는 sGubun값, sFidList값을 파싱해서
            GetChejanData()함수호출 시 인자로 사용하시면 보다 상세한 내용을 얻을 수 있습니다.

        4. 외부주문과의 차이점
            내부주문(API주문)
                1. 통신메시지 이벤트 수신 : OnReceiveMsg()
                2. TR수신 이벤트 수신     : OnReceiveTrData()
                3. 체결/잔고 이벤트 수신  : OnReceiveChejanData()

            외부주문(HTS/MTS 등...)
                1. 체결/잔고 이벤트 수신  : OnReceiveChejanData()
        '''
        return self.dynamicCall('SendOrder(str, str, str, int, str, int, int, str, str)',
                                [sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo])

    def SendOrderFO(self, sRQName: str, sScreenNo: str, sAccNo: str, sCode: str, lOrdKind: int, sSlbyTp: str,
                    sOrdTp: str, lQty: int, sPrice: str, sOrgOrdNo: str) -> int:
        '''
        LONG SendOrderFO(BSTR sRQName, BSTR sScreenNo, BSTR sAccNo, BSTR sCode, LONG lOrdKind
            , BSTR sSlbyTp, BSTR sOrdTp, LONG lQty, BSTR sPrice, BSTR sOrgOrdNo)

            sRQName   : 사용자 구분명
            sScreenNo : 화면번호
            sAccNo    : 계좌번호 10자리
            sCode     : 종목코드
            lOrdKind  : 주문종류 1:신규매매, 2:정정, 3:취소
            sSlbyTp   : 매매구분  1: 매도, 2:매수
            sOrdTp    : 거래구분(혹은 호가구분)은 아래 참고
            lQty      : 주문수량
            sPrice    : 주문가격
            sOrgOrdNo : 원주문번호

        코스피지수200 선물옵션, 주식선물 전용 주문함수입니다.

        [거래구분]
            1 : 지정가
            2 : 조건부지정가
            3 : 시장가
            4 : 최유리지정가
            5 : 지정가(IOC)
            6 : 지정가(FOK)
            7 : 시장가(IOC)
            8 : 시장가(FOK)
            9 : 최유리지정가(IOC)
            A : 최유리지정가(FOK)

        sHogaGb – 00:지정가, 03:시장가, 05:조건부지정가, 06:최유리지정가, 07:최우선지정가
            , 10:지정가IOC, 13:시장가IOC, 16:최유리IOC, 20:지정가FOK, 23:시장가FOK, 26:최유리FOK
            , 61:장전시간외종가, 62:시간외단일가, 81:장후시간외종가

        ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK
            , 장전시간외, 장후시간외 주문시 주문가격을 입력하지 않습니다.
            ex)
            지정가 매수 - openApi.SendOrder('RQ_1', '0101', '5015123410', 1, '000660', 10, 48500, '00', '');
            시장가 매수 - openApi.SendOrder('RQ_1', '0101', '5015123410', 1, '000660', 10, 0,     '03', '');
            매수 정정   - openApi.SendOrder('RQ_1', '0101', '5015123410', 5, '000660', 10, 49500, '00', '1');
            매수 취소   - openApi.SendOrder('RQ_1', '0101', '5015123410', 3, '000660', 10, 0,     '00', '2');

        반환값
            에러코드
        '''
        return self.dynamicCall('SendOrderFO(str, str, str, str, int, str, str, int, str, str)',
                                [sRQName, sScreenNo, sAccNo, sCode, lOrdKind, sSlbyTp, sOrdTp, lQty, sPrice, sOrgOrdNo])

    def SendOrderCredit(self, sRQName: str, sScreenNo: str, sAccNo: str, nOrderType: int, sCode: str, nQty: int,
                        nPrice: int, sHogaGb: str, sCreditGb: str, sLoanDate: str, sOrgOrderNo: str) -> int:
        '''
        LONG SendOrderCredit(LPCTSTR sRQName , LPCTSTR sScreenNo , LPCTSTR sAccNo
            , LONG nOrderType , LPCTSTR sCode , LONG nQty , LONG nPrice , LPCTSTR sHogaGb
            , LPCTSTR sCreditGb, LPCTSTR sLoanDate, LPCTSTR sOrgOrderNo)

            sRQName     : 사용자 구분명
            sScreenNo   : 화면번호
            sAccNo      : 계좌번호 10자리
            nOrderType  : 주문유형, 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
            sCode       : 종목코드
            nQty        : 주문수량
            nPrice      : 주문가격
            sHogaGb     : 거래구분(혹은 호가구분)은 아래 참고
            sCreditGb   : 신용거래구분
            sLoanDate   : 대출일
            sOrgOrderNo : 원주문번호

        국내주식 신용주문 전용함수입니다.
        대주거래는 지원하지 않습니다.

        [거래구분]
        모의투자에서는 지정가 주문과 시장가 주문만 가능합니다.

            00 : 지정가
            03 : 시장가
            05 : 조건부지정가
            06 : 최유리지정가
            07 : 최우선지정가
            10 : 지정가IOC
            13 : 시장가IOC
            16 : 최유리IOC
            20 : 지정가FOK
            23 : 시장가FOK
            26 : 최유리FOK
            61 : 장전시간외종가
            62 : 시간외단일가매매
            81 : 장후시간외종가

        [신용거래]
        신용거래 구분은 다음과 같습니다.
            03 : 신용매수 - 자기융자
            33 : 신용매도 - 자기융자
            99 : 신용매도 자기융자 합

        대출일은 YYYYMMDD형식이며 신용매도 - 자기융자 일때는 종목별 대출일을 입력하고 신용매도 - 융자합이면 '99991231'을 입력합니다.

        sCreditGb – 신용구분 (신용매수:03, 신용매도 융자상환:33,신용매도 융자합:99)
        신용매수 주문
            - 신용구분값 '03', 대출일은 '공백'
        신용매도 융자상환 주문
            - 신용구분값 '33', 대출일은 종목별 대출일 입력
            - OPW00005/OPW00004 TR조회로 대출일 조회
        신용매도 융자합 주문시
            - 신용구분값 '99', 대출일은 '99991231'
            - 단 신용잔고 5개까지만 융자합 주문가능
        나머지 입력값은 SendOrder()함수 설명참고

        반환값
            에러코드
        '''
        return self.dynamicCall('SendOrderCredit(str, str, str, int, str, int, int, str, str, str, str)',
                                [sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sCreditGb,
                                 sLoanDate, sOrgOrderNo])

    def GetChejanData(self, nFid: int) -> str:
        '''
        BSTR GetChjanData(long nFid)

            nFid : 실시간 타입에 포함된FID

        OnReceiveChejan()이벤트가 호출될때 체결정보나 잔고정보를 얻어오는 함수입니다.
        이 함수는 반드시 OnReceiveChejan()이벤트가 호출될때 그 안에서 사용해야 합니다.

        반환값
            수신데이터
        '''
        return self.dynamicCall('GetChejanData(int)', [nFid]).strip()

    # @ 이벤트 함수

    def _OnReceiveChejanData(self, sGubun: str, nItemCnt: int, sFidList: str) -> None:
        '''
        void OnReceiveChejanData(LPCTSTR sGubun, LONG nItemCnt, LPCTSTR sFidList);

            sGubun   : 체결구분, 접수와 체결시 '0'값, 국내주식 잔고전달은 '1'값, 파생잔고 전달은 '4'
                       0:주문체결통보, 1:잔고통보, 3:특이신호
            nItemCnt : 아이템 갯수
            sFidList : 데이터 리스트, 데이터 구분은 ';' 이다.

        주문요청후 주문접수, 체결통보, 잔고통보를 수신할 때 마다 호출되며
        GetChejanData()함수를 이용해서 상세한 정보를 얻을수 있습니다.
        '''

    # 조건검색

    def GetConditionLoad(self) -> int:
        '''
        long GetConditionLoad()

        사용자 조건검색 목록을 서버에 요청합니다.
        조건검색 목록을 모두 수신하면 OnReceiveConditionVer()이벤트가 호출됩니다.
        조건검색 목록 요청을 성공하면 1, 아니면 0을 리턴합니다.
        '''
        return self.dynamicCall('GetConditionLoad()')

    def GetConditionNameList(self) -> str:
        '''
        BSTR GetConditionNameList()

        서버에서 수신한 사용자 조건식을 조건명 인덱스와 조건식 이름을 한 쌍으로 하는 문자열들로 전달합니다.
        조건식 하나는 조건명 인덱스와 조건식 이름은 '^'로 나뉘어져 있으며
        각 조건식은 ';'로 나뉘어져 있습니다.
        이 함수는 반드시 OnReceiveConditionVer()이벤트에서 사용해야 합니다.

        반환값
            조건명 리스트(인덱스^조건명)
            조건명 리스트를 구분(';')하여 받아온다.
            Ex) 인덱스1^조건명1;인덱스2^조건명2;인덱스3^조건명3;…
        '''
        return self.dynamicCall('GetConditionNameList()').strip()

    def SendCondition(self, sScreenNo: str, sConditionName: str, nIndex: int, nSearch: int) -> bool:
        '''
        BOOL SendCondition(LPCTSTR strScrNo, LPCTSTR strConditionName, int nIndex, int nSearch)

            sScreenNo      : 화면번호
            sConditionName : 조건식 이름
            nIndex         : 조건명 인덱스
            nSearch        : 조회구분, 0:조건검색, 1:실시간 조건검색 (0:일반조회, 1:실시간조회, 2:연속조회)

        서버에 조건검색을 요청하는 함수로
        맨 마지막 인자값으로 조건검색만 할것인지 실시간 조건검색도 할 것인지를 지정할 수 있습니다.
        여기서 조건식 인덱스는 GetConditionNameList()함수가
        조건식 이름과 함께 전달한 조건명 인덱스를 그대로 사용해야 합니다.
        요청한 조건식이 없거나 조건명 인덱스와 조건식이 서로 안맞거나 조회횟수를 초과하는 경우 실패하게 됩니다.

        단순 조건식에 맞는 종목을 조회하기 위해서는 조회구분을 0으로 하고,
        실시간 조건검색을 하기 위해서는 조회구분을 1로 한다.
        OnReceiveTrCondition으로 결과값이 온다.
        연속조회가 필요한 경우에는 응답받는 곳에서 연속조회 여부에 따라 연속조회를 송신하면된다.

        [조건검색 사용예시]
            GetConditionNameList()함수로 얻은 조건식 목록이
            '0^조건식1;3^조건식1;8^조건식3;23^조건식5'일때 조건식3을 검색

            long lRet = SendCondition('0156', '조건식3', 8, 1);

        반환값
            성공 1, 실패 0
        '''
        return bool(self.dynamicCall('SendCondition(str, str, int, int)', [sScreenNo, sConditionName, nIndex, nSearch]))

    def SendConditionStop(self, sScreenNo: str, sConditionName: str, nIndex: int) -> None:
        '''
        Void SendConditionStop(LPCTSTR strScrNo, LPCTSTR strConditionName, int nIndex)

            sScreenNo      : 화면번호
            sConditionName : 조건식 이름
            nIndex         : 조건명 인덱스

        조건검색을 중지할 때 사용하는 함수입니다.
        조건식 조회할때 얻는 조건식 이름과 조건명 인덱스 쌍을 맞춰서 사용해야 합니다.

        해당 조건명의 실시간 조건검색을 중지하거나,
        다른 조건명으로 바꿀 때 이전 조건명으로 실시간 조건검색을 반드시 중지해야한다.
        화면 종료시에도 실시간 조건검색을 한 조건명으로 전부 중지해줘야 한다.
        '''
        self.dynamicCall('SendConditionStop(str, str, int)',
                         [sScreenNo, sConditionName, nIndex])

    def SetRealReg(self, sScreenNo: str, sCodeList: str, sFidList: str, sOptType: str) -> int:
        '''
        LONG SetRealReg(LPCTSTR strScreenNo, LPCTSTR strCodeList, LPCTSTR strFidList, LPCTSTR strRealType)

            sScreenNo : 화면번호
            sCodeList : 종목코드 리스트(복수종목가능 – '종목1;종목2;종목3;….')
            sFidList  : 실시간 FID리스트('FID1;FID2;FID3;…..')
            sOptType  : 실시간 등록 타입, 0 또는 1

        실시간 시세를 받으려는 종목코드와 FID 리스트를 이용해서 실시간 시세를 등록하는 함수입니다.
        한번에 등록가능한 종목과 FID갯수는 100종목, 100개 입니다.
        실시간 등록타입을 0으로 설정하면 등록한 종목들은 실시간 해지되고 등록한 종목만 실시간 시세가 등록됩니다.
        실시간 등록타입을 1로 설정하면 먼저 등록한 종목들과 함께 실시간 시세가 등록됩니다.

        strRealType이 '0' 으로 하면 같은화면에서 다른종목 코드로 실시간 등록을 하게 되면
        마지막에 사용한 종목코드만 실시간 등록이 되고 기존에 있던 종목은 실시간이 자동 해지됨.
        '1'로 하면 같은화면에서 다른 종목들을 추가하게 되면
        기존에 등록한 종목도 함께 실시간 시세를 받을 수 있음.
        꼭 같은 화면이여야 하고 최초 실시간 등록은 '0'으로 하고 이후부터 '1'로 등록해야함.

        [실시간 시세등록 예시]
            OpenAPI.SetRealReg(_T('0150'), _T('039490'), _T('9001;302;10;11;25;12;13'), '0');  // 039490종목만 실시간 등록
            OpenAPI.SetRealReg(_T('0150'), _T('000660'), _T('9001;302;10;11;25;12;13'), '1');  // 000660 종목을 실시간 추가등록

        반환값
            통신결과
        '''
        return self.dynamicCall('SetRealReg(str, str, str, str)', [sScreenNo, sCodeList, sFidList, sOptType])

    def SetRealRemove(self, sScreenNo: str, sDelCode: str) -> None:
        '''
        void SetRealRemove(LPCTSTR strScrNo, LPCTSTR strDelCode)

            sScreenNo : 화면번호 또는 ALL
            sDelCode  : 종목코드 또는 ALL

        실시간 시세해지 함수이며 화면번호와 종목코드를 이용해서 상세하게 설정할 수 있습니다.

        SetRealReg() 함수로 실시간 등록한 종목만 실시간 해제 할 수 있다.

        [실시간 시세해지 예시]
            OpenAPI.SetRealRemove('0150', '039490');  // '0150'화면에서 '039490'종목해지
            OpenAPI.SetRealRemove('ALL', 'ALL');  // 모든 화면에서 실시간 해지
            OpenAPI.SetRealRemove('0150', 'ALL');  // '0150' 화면에서 실시간 해지
            OpenAPI.SetRealRemove('ALL', '039490');  // 모든 화면에서 '039490'종목해지
        '''
        self.dynamicCall('SetRealRemove(str, str)', [sScreenNo, sDelCode])

    # @ 이벤트 함수

    def _OnReceiveConditionVer(self, lRet: int, sMsg: str) -> None:
        '''
        void OnReceiveConditionVer(long lRet, LPCTSTR sMsg)

            lRet : 호출 성공여부, 1: 성공, 나머지 실패
            sMsg : 호출결과 메시지

        사용자 조건식요청에 대한 응답을 서버에서 수신하면 호출되는 이벤트입니다.

        로컬에 사용자 조건식 저장 성공 여부를 확인하는 시점

        [사용자 조건식 호출결과 수신예시]
            OnReceiveConditionVer(long lRet, LPCTSTR sMsg)
            {
                if(lRet != 0) return;

                CString     strCondList(m_KOA.GetConditionNameList());
                CString     strOneCond, strItemID, strCondName;
                while(AfxExtractSubString(strOneCond, strCondList, nIndex++, _T(';')))  // 조건식을 하나씩 분리한다.
                {
                    if(strOneCond.IsEmpty())    continue;
                    AfxExtractSubString(strItemID   , strOneCond, 0, _T('^'));  // 조건명 인덱스를 분리한다.
                    AfxExtractSubString(strCondName , strOneCond, 1, _T('^'));  // 조건식 이름을 분리한다.
                }
            }
        '''

    def _OnReceiveTrCondition(self, sScreenNo: str, sCodeList: str, sConditionName: str, nIndex: int,
                              nNext: int) -> None:
        '''
        void OnReceiveTrCondition(LPCTSTR sScreenNo, LPCTSTR sCodeList, LPCTSTR sConditionName, int nIndex, int nNext)

            sScreenNo      : 화면번호
            sCodeList      : 종목코드 리스트(';'로 구분)
            sConditionName : 조건식 이름
            nIndex         : 조건명 인덱스
            nNext          : 연속조회 여부(2:연속조회, 0:연속조회없음)

        조건검색 요청으로 검색된 종목코드 리스트를 전달하는 이벤트입니다.
        종목코드 리스트는 각 종목코드가 ';'로 구분되서 전달됩니다.

        조건검색 조회응답으로 종목리스트를 구분자(';')로 붙어서 받는 시점.

        [조건검색 결과 수신예시]
            OnReceiveTrCondition(LPCTSTR sScrNo,LPCTSTR strCodeList, LPCTSTR strConditionName, int nIndex, int nNext)
            {
                if(strCodeList == '') return;
                CString strCode, strCodeName;
                int   nIdx = 0;
                while(AfxExtractSubString(strCode, strCodeList, nIdx++, _T(';')))// 하나씩 종목코드를 분리
                {
                    if(strCode == _T('')) continue;
                    strCodeName = OpenAPI.GetMasterCodeName(strCode); // 종목명을 가져온다.
                }
            }
        '''

    def _OnReceiveRealCondition(self, sCode: str, sType: str, sConditionName: str, sConditionIndex: str) -> None:
        '''
        void OnReceiveRealCondition(LPCTSTR sCode, LPCTSTR sType, LPCTSTR sConditionName, LPCTSTR sConditionIndex)

            sCode           : 종목코드
            strType         : 이벤트 종류, 'I':종목편입, 'D', 종목이탈
            sConditionName  : 조건식 이름
            sConditionIndex : 조건명 인덱스

        실시간 조건검색 요청으로 신규종목이 편입되거나 기존 종목이 이탈될때 마다 호출됩니다.

        [실시간 조건검색 수신예시]
            OnReceiveRealCondition(LPCTSTR sCode, LPCTSTR sType, LPCTSTR strConditionName, LPCTSTR strConditionIndex)
            {
                CString strCode(sCode), strCodeName;
                int   nIdx = 0;
                CString strType(sType);
                if(strType == _T('I'))// 종목편입
                {
                    strCodeName = OpenAPI.GetMasterCodeName(strCode); // 종목명을 가져온다.
                    long lRet = OpenAPI.SetRealReg(strSavedScreenNo, strCode, _T('9001;302;10;11;25;12;13'), '1');// 실시간 시세등록
                }
                else if(strType == _T('D')) // 종목이탈
                {
                    OpenAPI.SetRealRemove(strSavedScreenNo, strCode);// 실시간 시세해지
                }
            }
        '''

    # 기타함수 : 종목정보관련 함수

    def GetCodeListByMarket(self, sMarket: str) -> str:
        '''
        BSTR GetCodeListByMarket(LPCTSTR sMarket)

            sMarket : 시장구분값

        국내 주식 시장별 종목코드를 ';'로 구분해서 전달합니다.
        만일 시장구분값이 NULL이면 전체 시장코드를 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        [시장구분값]
             0 : 장내
            10 : 코스닥
             3 : ELW
             8 : ETF
            50 : KONEX
             4 :  뮤추얼펀드
             5 : 신주인수권
             6 : 리츠
             9 : 하이얼펀드
            30 : K-OTC

        반환값
            종목코드 리스트, 종목간 구분은 ';'이다.
        '''
        return self.dynamicCall('GetCodeListByMarket(str)', [sMarket]).strip()

    def GetMasterCodeName(self, sCode: str) -> str:
        '''
        BSTR GetMarsterCodeName(LPCTSTR strCode)

            sCode : 종목코드

        종목코드에 해당하는 종목명을 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        장내외, 지수선옵, 주식선옵 검색 가능.

        반환값
            종목한글명
        '''
        return self.dynamicCall('GetMasterCodeName(str)', [sCode]).strip()

    def GetMasterListedStockCnt(self, sCode: str) -> int:
        '''
        LONG GetMasterListedStockCnt(LPCTSTR sCode)

            sCode : 종목코드

        입력한 종목코드에 해당하는 종목 상장주식수를 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        반환값
            상장주식수
        '''
        return self.dynamicCall('GetMasterListedStockCnt(str)', [sCode])

    def GetMasterConstruction(self, sCode: str) -> str:
        '''
        BSTR GetMasterConstruction(LPCTSTR strCode)

        sCode : 종목코드

        입력한 종목코드에 해당하는 종목의
        감리구분(정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목)을 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        반환값
            감리구분

            감리구분 – 정상, 투자주의, 투자경고, 투자위험, 투자주의환기종목
        '''
        return self.dynamicCall('GetMasterConstruction(str)', [sCode]).strip()

    def GetMasterListedStockDate(self, sCode: str) -> str:
        '''
        BSTR GetMasterListedStockDate(LPCTSTR strCode)

            sCode : 종목코드

        입력한 종목의 상장일을 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        반환값
            상장일

            상장일 포멧 – xxxxxxxx[8]
        '''
        return self.dynamicCall('GetMasterListedStockDate(str)', [sCode]).strip()

    def GetMasterLastPrice(self, sCode: str) -> str:
        '''
        BSTR GetMasterLastPrice(LPCTSTR strCode)

            sCode : 종목코드

        입력한 종목의 전일가를 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        반환값
            전일가
        '''
        return self.dynamicCall('GetMasterLastPrice(str)', [sCode]).strip()

    def GetMasterStockState(self, sCode: str) -> str:
        '''
        BSTR GetMasterStockState(LPCTSTR strCode)

            sCode : 종목코드

        입력한 종목의 증거금 비율, 거래정지, 관리종목, 감리종목, 투자융의종목, 담보대출
        , 액면분할, 신용가능 여부를 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        반환값
            종목상태

            종목상태 – 정상, 증거금100%, 거래정지, 관리종목, 감리종목, 투자유의종목, 담보대출, 액면분할, 신용가능
        '''
        return self.dynamicCall('GetMasterStockState(str)', [sCode]).strip()

    def GetFutureList(self) -> str:
        '''
        BSTR GetFutrueList()

        지수선물 종목코드 리스트를 ';'로 구분해서 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        반환값
            종목코드 리스트

            반환값의 종목코드간 구분은 ';'
            Ex) 101J9000;101JC000
        '''
        return self.dynamicCall('GetFutureList()').strip()

    def GetActPriceList(self) -> str:
        '''
        BSTR GetActPriceList()

        지수옵션 행사가에 100을 곱해서 소수점이 없는 값을 ';'로 구분해서 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        [지수옵션 행사가 사용예시]
            CString strActPriceList(OpenAPI.GetActPriceList());
            '19000;19250;19500;19750;20000;20250;20500;20750;21000;21250;21500;21750;...'

        반환값
            행사가

            반환값의 행사가간 구분은 ';'
            Ex) 265.00;262.50;260.00
        '''
        return self.dynamicCall('GetActPriceList()').strip()

    def GetMonthList(self) -> str:
        '''
        BSTR GetMonthList()

        지수옵션 월물정보를 ';'로 구분해서 전달하는데
        순서는 콜 11월물 ~ 콜 최근월물 풋 최근월물 ~ 풋 최근월물가 됩니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        [지수옵션 월물조회 사용예시]
        CString strMonthList(OpenAPI.GetMonthList());
        '201812;201806;201712;201706;201703;201612;201611;201610;201609;201608;201607;...'

        반환값
            월물

            반환값의 월물간 구분은 ';'
            Ex) 201412;201409;201408;201407;201407;201408;201409;201412
        '''
        return self.dynamicCall('GetMonthList()').strip()

    def GetOptionCode(self, sActPrice, nCp, sMonth) -> str:
        '''
        BSTR GetOptionCode(LPCTSTR sActPrice, int nCp, LPCTSTR sMonth)

            sActPrice : 소수점을 포함한 행사가
            nCp       : 콜풋구분값, 콜:2, 풋:3
            sMonth    : 6자리 월물

        인자로 지정한 지수옵션 코드를 전달합니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        행사가와 월물 콜풋으로 종목코드를 구한다.

        [지수옵션 코드 사용예시]

            CString strOptCode = OpenAPI.GetOptionCode(_T('247.50'), 2, _T('201607'));

        반환값
            종목코드

            Ex) openApi.GetOptionCode('260.00', 2, '201407');
        '''
        return self.dynamicCall('GetOptionCode(str, int, str)', [sActPrice, nCp, sMonth]).strip()

    def GetOptionATM(self) -> str:
        '''
        BSTR GetOptionATM()

        지수옵션 소수점을 제거한 ATM값을 전달합니다.
        예를들어 ATM값이 247.50 인 경우 24750이 전달됩니다.
        로그인 한 후에 사용할 수 있는 함수입니다.

        지수옵션 ATM을 반환한다.

        반환값
            ATM
        '''
        return self.dynamicCall('GetOptionATM()').strip()

    def GetSFutureList(self, strBaseAssetGb: str) -> str:
        '''
        BSTR GetSFutureList(BSTR strBaseAssetGb)

        기초자산 구분값

        기초자산 구분값을 인자로 받아서 주식선물 종목코드, 종목명, 기초자산이름을 구할수 있습니다.
        주식선물 전체 종목코드를 얻으려면 인자값이 공백처리 하면 됩니다.
        전달되는 데이터 형식은 다음과 같습니다.

            '종목코드1^종목명1^기초자산이름1;종목코드2^종목명2^기초자산이름2;...;종목코드n^종목명n^기초자산이름n;'

        로그인 한 후에 사용할 수 있는 함수입니다.
        '''
        return self.dynamicCall('GetSFutureList(str)', [strBaseAssetGb]).strip()

    # 기타함수 : 특수함수

    def KOA_Functions(self, sFunctionName: str, sParam: str) -> str:
        '''
        BSTR KOA_Functions(BSTR sFunctionName, BSTR sParam)

            sFunctionName : 함수이름 혹은 기능이름
            sParam        : 함수 매개변수

        KOA_Function() 함수는 OpenAPI 기본 기능외에 기능을 사용하기 쉽도록 만든 함수이며
        두 개 인자값을 사용합니다.
        이 함수가 제공하는 기능과 필요한 인자값은 공지를 통해 제공할 예정입니다.

        [KOA_Functions() 함수 사용예]
            1. ShowAccountWindow      : 계좌비밀번호 설정을 출력한다.
            2. GetServerGubun         : 접속서버 구분을 알려준다.
            3. SetConditionSearchFlag : 검색종목 현재가 제공
            4. GetMasterStockInfo     : 주식종목 시장구분, 종목분류등 정보를 얻습니다.
            5. GetUpjongCode          : 업종코드 가져옵니다.
            6. IsOrderWarningETF      : 투자유의종목인지 확인합니다.
            7. IsOrderWarningStock    : 투자유의종목인지 확인합니다.

            ※ 상세는 아래 KOA_Functions 래퍼함수 참고
        '''
        return self.dynamicCall('KOA_Functions(str, str)', [sFunctionName, sParam]).strip()

    # @ KOA_Functions 래퍼함수

    def GetServerGubun(self) -> str:
        '''
        접속서버 구분을 알려준다.

        반환값
            1 : 모의투자 접속, 나머지 : 실서버 접속
        '''
        return self.KOA_Functions('GetServerGubun', '')

    def SetConditionSearchFlag(self, sFlag: str) -> None:
        '''
        검색종목에 현재가를 추가해 줍니다.

        sFlag : 설정 플래그
            'AddPrice' : 현재가 종목코드와 함께 전달하도록 설정
            'DelPrice' : 현재가 포함 해지

        비교적 간단한 설정으로 조건검색 결과로 종목코드와 그 종목의 현재가를 얻을 수 있습니다.
        이 방법은 실시간 조건검색에서는 사용할 수 없고 오직 조건검색에만 가능한 방법입니다.

        'Addprice'로 플래그를 지정하면

            OpenAPI.SetConditionSearchFlag('AddPrice')

        OnReceiveTrCondition()이벤트에는 검색 종목과 현재가가

            '종목코드^현재가;종목코드^현재가;...종목코드^현재가'

        형식으로 전달됩니다. 기존에는

            '종목코드^종목코드...종목코드'

        형식으로 검색결과를 전달하는것과 차이가 있으니 수신 데이터를 처리하실때 주의하셔야 합니다.

        다시 원래대로 조검검색결과를 종목코드만 수신하려면 'Delprice' 플래그를 사용하면 됩니다.

            OpenAPI.SetConditionSearchFlag('DelPrice')

        지금까지 설명을 간단하게 정리하면 다음과 같습니다.

        1. 현재가 종목코드와 함께 전달하도록 설정
            OpenAPI.SetConditionSearchFlag('AddPrice')

        2. 조건검색 요청
            OpenAPI.SendCondition(sScreenNo, sConditionName, nIndex, 0)

        3. 조건검색결과 수신
            앞서 설정으로 종목코드와 현재가가 OnReceiveTRCondition()로 함께 전달되므로
            수신데이터 처리를 다르게 해야 합니다.
            만일 4개 종목이 검색되었다면 다음과 같이 전달됩니다.

                종목코드^현재가;종목코드^현재가;종목코드^현재가;종목코드^현재가;

        4. 현재가 포함 해지 - 이후 조건검색 결과에는 종목코드만 있습니다.

            OpenAPI.SetConditionSearchFlag('DelPrice')

        이 방법은 실시간 조건검색에서는 사용할 수 없고 수신데이터에 현재가가 포함되므로
        데이터 처리 방법을 달리해야 합니다.
        '''
        self.KOA_Functions('SetConditionSearchFlag', sFlag)

    def GetMasterStockInfo(self, sCode: str) -> str:
        '''
        주식종목 시장구분, 종목분류등 정보를 가져온다.

        sCode : 업종명을 얻으려는 종목코드

        반환값
            입력한 종목에 대한 대분류, 중분류, 업종구분값을 구분자로 연결한 문자열이며
            여기서 구분자는 '|'와 ';'입니다.

            예를들어 OpenAPI.KOA_Functions('GetMasterStockInfo', '039490')을 호출하면

                시장구분0|거래소;시장구분1|중형주;업종구분|금융업;

            이렇게 결과를 얻을 수 있습니다.
        '''
        return self.KOA_Functions('GetMasterStockInfo', sCode)

    def GetUpjongCode(self, sMarketGubun: str) -> str:
        '''
        업종코드를 가져온다.

        sMarketGubun : 시장구분값, 0:장내, 1: 코스닥, 2:KOSPI200, 4:KOSPI100(KOSPI50), 7:KRX100

        반환값

            '시장구분값,업종코드,업종명|시장구분값,업종코드,업종명|...|시장구분값,업종코드,업종명'

        즉 하나의 업종코드는 입력한 시장구분값과 업종코드 그리고 그 업종명이 쉼표(,)로 구분되며
        각 업종코드는 '|'로 구분됩니다.

        GetUpjongCode('0')로 조회시 결과는 다음과 같습니다.

            0,001,종합(KOSPI)|0,002,대형주|...|0,605,코스피배당성정50
        '''
        return self.KOA_Function('GetUpjongCode', sMarketGubun)

    def ShowAccountWindow(self) -> None:
        '''
        계좌비밀번호는 별도의 계좌비밀번호 입력창을 통해서만 입력이 가능합니다.
        입력창을 출력하는 방법은 2가지로 제공됩니다.

        1. 메뉴이용
            로그인후 윈도우의 작업표시줄상에 깜박이는 트레이아이콘의 마우스우측 메뉴(모니터 오른쪽 하단)에서 '계좌비밀번호 저장' 선택

        2. 함수이용
            로그인후 OpenAPI.KOA_Functions(_T('ShowAccountWindow'), _T('')) 호출

        입력창에 계좌비밀번호 (모의투자는 '0000')를 입력하시고 등록버튼을 눌러주셔야 이후 주문을 포함하여 계좌관련 조회가 가능합니다.
        '''
        self.KOA_Functions('ShowAccountWindow', '')

    def IsOrderWarningETF(self, sCode: str) -> str:
        '''
        sCode : 확인할 종목코드

        거래소 제도개선으로 ETF/ETN 종목 중 투자유의 종목을 매수주문하는 경우
        경고 메세지 창이 출력되도록 기능이 추가 되었습니다.
        경고 창 출력 시 주문을 중지/전송 선택 가능합니다.

        Open API를 통해 ETF종목을 매매하시는 고객께서는 주문 함수를 호출하기 전에
        특정 종목이 투자유의종목인지 확인할 수 있습니다.
        방법은 아래와 같습니다.

            KOA_Functions("IsOrderWarningETF", "종목코드(6자리)")

        투자유의 종목인 경우 "1" 값이 리턴되며, 그렇지 않은 경우 "0" 값이 리턴됩니다.
        (ETF가 아닌 종목을 입력시 "0" 값이 리턴됩니다.)
        '''
        return self.KOA_Functions('IsOrderWarningETF', sCode)

    def IsOrderWarningStock(self, sCode: str) -> str:
        '''
        sCode : 확인할 종목코드

        거래소 제도개선으로 단기과열종목/투자경고종목/투자위험종목/정리매매종목을 매수주문하는 경우
        경고 메세지 창이 출력되도록 기능이 추가 되었습니다.
        경고 창 출력 시 주문을 중지/전송 선택 가능합니다.

        Open API를 통해 주식종목을 매매하시는 고객께서는 주문 함수를 호출하기 전에
        특정 종목이 투자유의종목인지 확인할 수 있습니다.
        방법은 아래와 같습니다.

            KOA_Functions("IsOrderWarningStock", "종목코드(6자리)")

        리턴값은 다음과 같습니다.

            '0':해당없음, '2':정리매매, '3':단기과열, '4':투자위험, '5':투자경고
        '''
        return self.KOA_Functions('IsOrderWarningStock', sCode)

    # 개발가이드(KOA Studio)에 없는 함수

    def GetAPIModulePath(self) -> str:
        '''
        BSTR GetAPIModulePath()

        OpenAPI모듈의 경로를 반환한다.

        반환값
            경로
        '''
        return self.dynamicCall('GetAPIModulePath()').strip()

    def GetDataCount(self, sRecordName: str) -> int:
        '''
        LONG GetDataCount(LPCTSTR sRecordName)

            sRecordName : 레코드명

        레코드의 반복개수를 반환한다.

        Ex) openApi.GetDataCount('주식기본정보');

        반환값
            레코드 반복개수
        '''
        return self.dynamicCall('GetDataCount(str)', [sRecordName])

    def GetOutputValue(self, sRecordName: str, nRepeatIdx: int, nItemIdx: int) -> str:
        '''
        BSTR GetOutputValue(LPCTSTR sRecordName, long nRepeatIdx, long nItemIdx)

            nRepeatIdx : 반복순서
            nItemIdx   : 아이템 순서

        레코드의 반복순서와 아이템의 출력순서에 따라 수신데이터를 반환한다.

        반환값
            수신 데이터

            Ex) 현재가출력 - openApi.GetOutputValue('주식기본정보', 0, 36);

        '''
        return self.dynamicCall('GetOutputValue(str, int, int)', [sRecordName, nRepeatIdx, nItemIdx]).strip()

    def GetThemeGroupList(self, nType: int) -> str:
        '''
        BSTR GetThemeGroupList(long nType)

            nType : 정렬순서 (0:코드순, 1:테마순)

        테마코드와 테마명을 반환한다.

        반환값
            코드와 코드명 리스트

            반환값의 코드와 코드명 구분은 '|' 코드의 구분은 ';'
            Ex) 100|태양광_폴리실리콘;152|합성섬유
        '''
        return self.dynamicCall('GetThemeGroupList(int)', nType).strip()

    def GetThemeGroupCode(self, sThemeCode: str) -> str:
        '''
        BSTR GetThemeGroupCode(LPCTSTR sThemeCode)

            strThemeCode : 테마코드 반환값

        테마코드에 소속된 종목코드를 반환한다.

        반환값
            종목코드 리스트

            반환값의 종목코드간 구분은 ';'
            Ex) A000660;A005930
        '''
        return self.dynamicCall('GetThemeGroupCode(str)', [sThemeCode]).strip()

    def GetFutreCodeByIndex(self, nIndex: int) -> str:
        '''
        BSTR GetFutreCodeByIndex(int nIndex)

            nIndex : 0~3 지수선물코드, 4~7 지수스프레드

        지수선물 코드를 반환한다.

        반환값
            종목코드

            Ex) 최근월선물 - openApi.GetFutureCodeByInex(0);
            최근월스프레드 - openApi.GetFutureCodeByInex(4);
        '''
        return self.dynamicCall('GetFutreCodeByIndex(int)', [nIndex]).strip()

    def GetOptionCodeByMonth(self, sCode: str, nCp: int, sMonth: str) -> str:
        '''
        BSTR GetOptionCodeByMonth(LPCTSTR sCode, int nCp, LPCTSTR sMonth)

            strCode : 종목코드
            nCp     : 콜풋구분 2:콜, 3:풋
            sMonth  : 월물(6자리)

        입력된 종목코드와 동일한 행사가의 코드중 입력한 월물의 코드를 구한다.

        반환값
            종목코드

            Ex) openApi.GetOptionCodeByMonth('201J7260', 2, '201412');
            결과값 = 201JC260
        '''
        return self.dynamicCall('GetOptionCodeByMonth(str, int, str)', [sCode, nCp, sMonth]).strip()

    def GetOptionCodeByActPrice(self, sCode: str, nCp: int, nTick: int) -> str:
        '''
        BSTR GetOptionCodeByActPrice(LPCTSTR sCode, int nCp, int nTick)

            sCode : 종목코드
            nCp   : 콜풋구분 2:콜, 3:풋
            nTick : 행사가 틱

        입력된 종목코드와 동일한 월물의 코드중 입력한 틱만큼 벌어진 코드를 구한다.

        반환값
            종목코드

            Ex) openApi.GetOptionCodeByActPrice('201J7260', 2, -1);
            결과값 = 201J7262
        '''
        return self.dynamicCall('GetOptionCodeByActPrice(str, int, int)', [sCode, nCp, nTick]).strip()

    def GetSFutureList(self, sBaseAssetCode: str) -> str:
        '''
        BSTR GetSFutureList(LPCTSTR sBaseAssetCode)

            sBaseAssetCode : 기초자산코드

        주식선물 코드 리스트를 반환한다.

        반환값
            종목코드 리스트

            출력값의 코드간 구분은 ';'이다.
        '''
        return self.dynamicCall('GetSFutureList(str)', [sBaseAssetCode]).strip()

    def GetSFutureCodeByIndex(self, sBaseAssetCode: str, nIndex: int) -> str:
        '''
        BSTR GetSFutureCodeByIndex(LPCTSTR sBaseAssetCode, int nIndex)

            sBaseAssetCode : 기초자산코드
            nIndex         : 0~3 지수선물코드, 4~7 지수스프레드, 8~11 스타 선물, 12~ 스타 스프레드

        주식선물 코드를 반환한다.

        반환값
            종목코드
            Ex) openApi.GetSFutureCodeByIndex('11', 0);
        '''
        return self.dynamicCall('GetSFutureCodeByIndex(str, int)', [sBaseAssetCode, nIndex]).strip()

    def GetSActPriceList(self, sBaseAssetGb: str) -> str:
        '''
        BSTR GetSActPriceList(LPCTSTR sBaseAssetGb)

            sBaseAssetGb : 기초자산코드구분

        주식옵션 행사가 리스트를 반환한다.

        반환값
            행사가 리스트, 행사가간 구분은 ';' 비고
            Ex) openApi.GetSActPriceList('11');
        '''
        return self.dynamicCall('GetSActPriceList(str)', [sBaseAssetGb]).strip()

    def GetSMonthList(self, sBaseAssetGb: str) -> str:
        '''
        BSTR GetSMonthList(LPCTSTR sBaseAssetGb)

            strBaseAssetGb : 기초자산코드구분

        주식옵션 월물 리스트를 반환한다.

        반환값
            월물 리스트, 월물간 구분은 ';'

            Ex) openApi.GetSActPriceList('11');
        '''
        return self.dynamicCall('GetSMonthList(str)', [sBaseAssetGb]).strip()

    def GetSOptionCode(self, sBaseAssetGb: str, sActPrice: str, nCp: int, sMonth: str) -> str:
        '''
        BSTR GetSOptionCode(LPCTSTR sBaseAssetGb, LPCTSTR sActPrice, int nCp, LPCTSTR sMonth)

            sBaseAssetGb : 기초자산코드구분
            sActPrice    : 행사가
            nCp          : 콜풋구분
            sMonth       : 월물

        주식옵션 코드를 반환한다.

        반환값
            주식옵션 코드

            Ex) openApi.GetSOptionCode('11', '1300000', 2, '1412');
        '''
        return self.dynamicCall('GetSOptionCode(str, str, int, str)', [sBaseAssetGb, sActPrice, nCp, sMonth]).strip()

    def GetSOptionCodeByMonth(self, sBaseAssetGb: str, sCode: str, nCp: int, sMonth: str) -> str:
        '''
        BSTR GetSOptionCodeByMonth(LPCTSTR sBaseAssetGb, LPCTSTR sCode, int nCp, LPCTSTR sMonth)

            sBaseAssetGb : 기초자산코드구분
            sCode        : 종목코드
            nCp          : 콜풋구분
            sMonth       : 월물

        입력한 주식옵션 코드에서 월물만 변경하여 반환한다.

        반환값
            주식옵션 코드

            Ex) openApi.GetSOptionCodeByMonth('11', '211J8045', 2, '1412');
        '''
        return self.dynamicCall('GetSOptionCodeByMonth(str, str, int, str)', [sBaseAssetGb, sCode, nCp, sMonth]).strip()

    def GetSOptionCodeByActPrice(self, sBaseAssetGb: str, sCode: str, nCp: int, nTick: int) -> str:
        '''
        BSTR GetSOptionCodeByActPrice(LPCTSTR sBaseAssetGb, LPCTSTR sCode, int nCp, int nTick)

            sBaseAssetGb : 기초자산코드구분
            sCode        : 종목코드
            nCp          : 콜풋구분
            nTick        : 월물

        입력한 주식옵션 코드에서 행사가만 변경하여 반환한다. 입력값

        반환값
            주식옵션 코드

            Ex) openApi.GetSOptionCodeByActPrice('11', '211J8045', 2, 4);
        '''
        return self.dynamicCall('GetSOptionCodeByActPrice(str, str, int, int)',
                                [sBaseAssetGb, sCode, nCp, nTick]).strip()

    def GetSFOBasisAssetList(self) -> str:
        '''
        BSTR GetSFOBasisAssetList()

        주식선옵 기초자산코드/종목명을 반환한다.

        반환값
            기초자산코드/종목명, 코드와 종목명 구분은 '|' 코드간 구분은';'

            Ex) 211J8045|삼성전자 C 201408;212J8009|SK텔레콤 C 201408 비고
            Ex) openApi.GetSFOBasisAssetList();
        '''
        return self.dynamicCall('GetSFOBasisAssetList()').strip()

    def GetSOptionATM(self, sBaseAssetGb: str) -> str:
        '''
        BSTR GetSOptionATM(LPCTSTR sBaseAssetGb)

            sBaseAssetGb : 기초자산코드구분

        주식옵션 ATM을 반환한다.

        반환값
            ATM

            Ex) openApi.GetSOptionATM('11');
        '''
        return self.dynamicCall('GetSOptionATM(str)', [sBaseAssetGb]).strip()

    def GetBranchCodeName(self) -> str:
        '''
        BSTR GetBranchCodeName()

        회원사 코드와 이름을 반환합니다.

        반환값
            회원사코드|회원사명;회원사코드|회원사명;…

            Ex) openApi.GetBranchCodeName();
        '''
        return self.dynamicCall('GetBranchCodeName()').strip()

    def SetInfoData(self, sInfoData: str) -> int:
        '''
        LONG SetInfoData(LPCTSTR sInfoData)

            sInfoData : 아이디

        다수의 아이디로 자동로그인이 필요할 때 사용한다.

        반환값
            통신결과

            Ex) openApi.SetInfoData('UserID');
        '''
        return self.dynamicCall('SetInfoData(str)', [sInfoData])
