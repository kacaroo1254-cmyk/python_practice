# 한 번만 실행하는 파일입니다. YOLO 가 예전에 기억한 결과 자리를 지우고, 지금 내 폴더(B)로 다시 기억하게 합니다.
# 실행한 뒤 y0_where.py 를 다시 실행해서 '결과 자리 : 내 폴더(B) 안' 이 나오는지 보세요.

from ultralytics import settings                    # ultralytics 가 기억해 둔 설정을 꺼낸다

print("지우기 전 결과 자리 :", settings["runs_dir"])   # 지우기 전에 기억하던 자리
settings.reset()                                    # 기억을 지우고 지금 파이썬이 있는 폴더(B) 기준으로 다시 정한다
print("지운 뒤 결과 자리 :", settings["runs_dir"])     # 새로 기억한 자리
