# OurHour
Kakaotalk conversation analyzer


## 대화 파일 준비하기
대화방 > 설정 > 대화 내용 내보내기
현재 한국어 아이폰에서 내보내기한 대화 파일만 작동함

2016. 7. 10. 오후 7:37, 이름 : 대화 내용

위와 같은 형식으로 나와야 함.

## 실행 방법
프로젝트 압축 해제

src/ 폴더에 카카오톡 대화 파일 옮겨두기

터미널에서 프로젝트 폴더로 이동
 * Windows : 탐색기에서 프로젝트 폴더로 이동한 후 경로창에 cmd 라고 쳐서 명령 프롬프트 키기

**python이 설치 및 PATH에 등록되어 있어야 합니다!**

터미널에서 아래 명령어 실행
```
pip install -r src/requirements.txt
python src/cli.py
```