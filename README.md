# 도그푸터 실행 사양

## 도그푸터 지원 OS
|  | Windows 7 | Windows 10 |
| :-------- | :--------: | :--------: |
| 이미지 인식 | O | O |
| 마우스 이벤트 | O | O |
| 비활성 모드 | X | O |
| 창 숨김 | X | O |

## 도그푸터 지원 앱플레이어
|  | LDPlayer | NoxPlayer | Memu | BlueStack |
| :-------- | :--------: | :--------: | :--------: | :--------: |
| 이미지 인식 | O | O | O | X |
| 마우스 이벤트 | O | O | O | X |
| 비활성 모드 | O | O | X | X |
| 창 숨김 | O | O | X | X |

# 도그푸터 매크로 설치 방법

## Git for Windows 설치

오픈 소스 깃허브(github.com)를 사용하기 위해서는 컴퓨터에 git 이라는 프로그램을 설치해야 합니다.
도그푸터 매크로는 윈도우즈에서만 실행할 수 있기 때문에 윈도우즈용 Git을 설치하도록 합니다.
아래 링크를 클랙해서 "Download"버튼을 누르면 됩니다.

[Git for Windows 공식 홈페이지 바로가기 링크](https://gitforwindows.org/)

## Python 3.6x 버전 설치

윈도우즈 OS 버전에 따라 설치하는 Python 버전이 다릅니다. 보통 윈도우7 은 32비트를 설치하고 윈도우10 은 64비트를 설치합니다. 파이썬 설치는 여기서 다루지 않습니다. 구글이나 네이버에서 검색해서 설치해주세요

[Python 3.6.8 버전 윈도우 32비트(Windows 7/10) 다운로드 링크](https://www.python.org/ftp/python/3.6.8/python-3.6.8-webinstall.exe)

[Python 3.6.8 버전 윈도우 64비트(Windows 10) 다운로드 링크](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64-webinstall.exe)

## Git Bash 실행하기

"Git for Windows" 를 제대로 설치했다면 "Git Bash"라는 프로그램이 있어햐 합니다. 해당 프로그램이 없다면 구글링을 통해서 제대로 설치해주세요.
Git Bash를 실행합니다. 이 프로그램은 윈도우즈 CMD 창과 비슷하게 생겼습니다.

## 도그푸터 깃허브 오픈 소스 다운로드 받기

도그푸터 소스를 내려받을 디렉토리를 만듭니다. 
디렉토리로 이동 후 마우스를 우클릭하며 메뉴에 "Git Bash Here" 가 있어야 합니다.
"Git Bash Here"가 없으면 Git for Windows가 제대로 설치가 되지 않은 것입니다. 설치를 제대로 해주세요.
"Git Bash Here"가 보인다면 클릭해주세요. 해당 디렉토리에서 Git Bash가 실행됩니다.



## PIP 라이브러리 설치하기

도그푸터는 Python 으로 작성되었습니다. 또한 Python 에서 제공하는 기본 라이브러리 외에 외부 라이브러리를 사용합니다.
아래 명령어를 Git Bash에서 순서대로 실행해주시길 바랍니다.


```
$ python -m pip install --upgrade pip
```

```
$ pip install flask-restful
```

```
$ pip install pyautogui
```

```
$ pip install numpy
```

```
$ pip install opencv-python
```

```
$ pip install matplotlib
```



