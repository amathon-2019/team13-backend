#team13-backend

##사용된 기술

Frontend : React / Axios / WebSocket API

Backend : Python3.7 + Django + RestFramewok + Channels + Redis

Lambda + API GateWay (Http / Websocket 혼용)

어려웠던 점.

Lambda Runtime Python3.7 환경에서 자꾸
파이썬 패키지들이 불러오지기 전에 handler 함수가 실행되는 문제 발생.
Pythonn3.7 환경으로 변경. Docker로 AmazonLinux 환경에서 직접 테스트 했는데 이상이 없었는데 Lambd에 업로드하면 문제 발생. Layer 활용해도 동일한 문제 발생.

Python3.7의 코루틴 활용한 코드들이 있었는데 전부 제거. 그리고 Python3.7이 필요한 

