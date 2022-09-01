import time
from collections import deque
from PyQt5 import QtCore


class Task:
    '''
    TR 요청을 위한 파라미터 저장용 클래스
    '''
    __slots__ = ['id', 'count', 'trcode', 'rqname',
                 'stockcode', 'paramtr', 'paramrq']

    id_count = 0  # id를 클래스 변수로 지정하여 객체별로 유일성을 부여한다.

    def __init__(self):
        self.__class__.id_count += 1  # 객체가 생성될 때 갱신

        # Task구분용 ID, 키움은 request id가 문자열이므로 str로 변환
        self.id = str(self.__class__.id_count)
        self.count = 0  # 카운팅용
        self.trcode = ''
        self.rqname = ''
        self.stockcode = ''
        self.paramtr = {}  # SetInputValue 설정용

        # CommRqData 파라미터 설정용. [sRqName, sTrCode, nPrevNext, sScreenNo] 순으로 설정한다.
        self.paramrq = []


class TRReqManager(QtCore.QThread):
    '''
    TR요청을 일정 시간 간격으로 호출하게 하는 클래스
    TR요청 정보를 Task 형식으로 큐에 push하고 일정 시간 간격 경과시 Task 데이터를 pop해 준다.
    pop할 때 poptr 이벤트를 호출하며 외부에서 poptr이벤트를 connect하고 Task 데이터를 이용해 TR을 요청해준다.

    참고: http://blog.quantylab.com/systrading.html
    '''
    poptr = QtCore.pyqtSignal(Task)  # TR Task 데이터가 pop되었을 때 알려주는 이벤트

    taskQueue = deque()

    def __init__(self) -> None:
        super().__init__()

        self.mutex = QtCore.QMutex()

        self.TimeInterval = 0.33  # TR 요청 간격
        self.flagLoop = True

    def __del__(self) -> None:
        self.flagLoop = False
        self.wait()

    def setTimeInterval(self, fValue: float) -> None:
        '''
        시간 간격을 재설정한다.
        '''
        self.TimeInterval = fValue

    def stop(self) -> None:
        '''
        큐 루프를 멈춘다.
        '''
        self.flagLoop = False

    def push(self, task: Task) -> None:
        '''
        Task 데이터를 큐에 넣는다.
        '''
        self.mutex.lock()
        self.taskQueue.append(task)
        self.mutex.unlock()

    def pushfirst(self, task: Task) -> None:
        '''
        Task 데이터를 큐 제일 처음에 넣는다.
        '''
        self.mutex.lock()
        self.taskQueue.insert(0, task)
        self.mutex.unlock()

    def run(self) -> None:
        while self.flagLoop:
            while len(self.taskQueue) > 0:
                try:
                    self.mutex.lock()
                    task = self.taskQueue.popleft()
                    self.mutex.unlock()
                    self.poptr.emit(task)
                    time.sleep(self.TimeInterval)
                except:
                    print("taskQueue 예외 발생")
            time.sleep(self.TimeInterval)

        self.flagLoop = True
