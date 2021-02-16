# 사용법
```
python3 crawling.py
>>> Enter the date (ex 2021-01-01) or just hit the enter key : 
```
엔터키를 치면 time_stamp.json에 저장된 최신일자를 불러서 크롤링하고 특정날짜 (ex 2021-01-01)를 입력하면 특정날짜 ~ 실행 일자 까지 크롤링한다.
# 라이브러리
```
import requests
from bs4 import Beatifulsoup
import dateutil
```

# 설명
1. time_stamp.json 에는 뉴스별로 가장 최신일자 뉴스의 일자가 저장되어 있다. crwaling.py를 실행하고 enter를 치면 실핼일자 부터 이 파일에 저장된 최신자까지 크롤링한다. 
2. text의 길이가 20 미만인 데이터는 data/error_data 에 meta_data와 함께 저장한다.


# 문제
1. ~~hellodd, bizwatch 두 사이트는 현재 작업환경(집, 20210106)에서 ip가 막혀서 크롤링이 불가능함~~  
-> ip 우회(roa api)로 해결함  

2. ~~bikorea, klnews 두 사이트는 aiohttp 에서 ClientSession() 의 session 의 session.get() 의 response 의 디코딩 문제로 동기화 방식으로 크롤링을 한다.
즉, 에서 `utf-8` 이 안먹힌다.~~  
-> aiohttp를 쓰지 않고 동기 코드를 비동기 코드화시켜서 사용함
    ```
    async with session.get(url, timeout=20) as response:
        text = await response.read()
        soup = bs(text.decode('utf-8'), 'html.parser')
    ```

3. 코드가 더욱 복잡해졌다.
4. Error 처리가 안되어 있다.
5. ~~mobiinside 사이트는 post 방식으로 동작한다. 그래서 request data를 사용해야 하는데~~  
    ```
     "td_block_id": "td_uid_28_5ff5396b7a816",
     "td_magic_token": "8f0b3053b5"
    ```  
    ~~값이 매일 바뀐다.~~  
    -> 해당 값 또한 소스 페이지에 있음을 발견하고 코드 수정함.
6. log 처리가 안되어 있다.




