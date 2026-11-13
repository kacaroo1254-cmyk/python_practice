import os                               # 폴더·파일 이름을 다루는 도구 상자(os)를 가져온다
import sys                              # 지금 돌고 있는 파이썬에 대한 정보 도구 상자(sys)를 가져온다

# 이 파일은 읽지 않고 실행만 합니다. 실행하면 내 자리를 알려 줍니다.

HERE = os.path.dirname(os.path.abspath(__file__))   # 이 파일이 들어 있는 폴더의 전체 주소 (예: B 작업 폴더/d32_photo)
TOP = os.path.dirname(HERE)                         # 그 폴더의 바로 위 폴더 (B 작업 폴더 의 맨 위여야 한다)
VENV = os.path.join(TOP, ".venv")                   # 바로 위 폴더 안의 .venv 주소 (B 작업 폴더 의 .venv)
PY = os.path.abspath(sys.executable)                # 지금 이 파일을 실행하고 있는 파이썬의 전체 주소

print("이 파일이 있는 폴더 :", HERE)                 # 첫째 줄 : 이 파일이 있는 폴더
print("파이썬 :", PY)                               # 둘째 줄 : 지금 쓰는 파이썬

PY_SMALL = PY.lower()                               # 대문자·소문자를 구분하지 않도록 모두 소문자로 바꾼다 (윈도우 대비)
VENV_SMALL = VENV.lower() + os.sep                  # .venv 주소 끝에 폴더 구분 글자(\ 또는 /)를 붙여 소문자로 만든다

if PY_SMALL.startswith(VENV_SMALL):                 # 파이썬 주소가 B 의 맨 위 .venv 주소로 시작하면
    print("프로젝트 맨 위 .venv(B 의 .venv)를 쓰고 있다 -> 좋습니다")      # 제대로 된 자리
else:                                               # 아니면
    print("다른 .venv 를 쓰고 있다 -> 설정에서 바꾸세요")        # 설정(Python Interpreter)을 바꿔야 한다
    print("프로젝트 맨 위 .venv(B 의 .venv) 는 :", VENV)          # 이것이 있어야 할 자리

if sys.flags.utf8_mode == 1:                        # 파이썬의 UTF-8 모드가 켜져 있으면 (1 = 켜짐)
    print("파이썬 UTF-8 모드 : 켜짐")                 # 켜짐
else:                                               # 아니면
    print("파이썬 UTF-8 모드 : 꺼짐")                 # 꺼짐

TOP_GIT = os.path.exists(os.path.join(TOP, ".git"))  # 바로 위 폴더(B 의 맨 위)에 .git (내 깃 폴더 표시)이 있는지
if TOP_GIT:                                         # 있으면
    print("내 깃 폴더(B) : 맞다 -> 좋습니다")             # B 가 내 깃으로 연결된 폴더
else:                                               # 없으면
    print("내 깃 폴더(B) : 아니다 -> 바로 위 폴더가 B 의 맨 위 폴더가 맞는지 보세요")   # 폴더를 잘못 열었을 수 있다

from ultralytics import settings                    # ultralytics 가 기억해 둔 설정을 꺼낸다
RUNS = os.path.abspath(settings["runs_dir"])        # YOLO 가 기억한 결과 폴더(runs)의 전체 주소
print("YOLO 가 기억한 결과 자리 :", RUNS)              # 결과 자리를 보여 준다

if RUNS.lower().startswith(TOP.lower() + os.sep):   # 기억한 자리가 B 의 맨 위 아래이면
    print("결과 자리 : 내 폴더(B) 안 -> 좋습니다")        # 제대로 된 자리
else:                                               # 아니면 (예전에 A 에서 돌릴 때 기억한 자리)
    print("결과 자리 : 내 폴더(B) 밖 -> y0_reset.py 를 한 번 실행하세요")   # 초기화 파일을 안내
