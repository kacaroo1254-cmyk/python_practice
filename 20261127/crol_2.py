import os
import time
import base64
import shutil
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# 1. 수집 설정값 (실습 시 원하는 검색어와 목표 수량으로 변경)
query = "아이오닉 3"
target_count = 200
output_dir = f"dataset/{query}_thumb"
os.makedirs(output_dir, exist_ok=True)

# 2. 자동화 탐지 우회 크롬 브라우저 실행
options = uc.ChromeOptions()
options.add_argument("--window-size=1400,900")
driver = uc.Chrome(options=options)

# 3. 구글 이미지 검색 페이지 접속 (udm=2: 이미지 검색 탭)
search_url = f"https://www.google.com/search?q={query}&udm=2"
driver.get(search_url)
time.sleep(2)

# 4. 보안 인증(reCAPTCHA) 발생 시 수동 해결 대기
if "sorry/index" in driver.current_url or "로봇이 아닙니다" in driver.page_source:
    print("\n[알림] 구글 보안 인증이 감지되었습니다. 크롬 창에서 인증을 완료한 뒤")
    input("터미널 창을 클릭하고 [Enter] 키를 눌러주세요... ")
    time.sleep(2)

# 5. 스크롤을 내려 목표 수량 이상의 썸네일이 DOM에 로드되도록 유도
print("크롬에서 스크롤을 내리며 썸네일을 로딩하는 중...")
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1.5)

    # 검색 결과 그리드 내의 모든 이미지 태그 탐색
    img_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-id] img")
    print(f"현재 로드된 썸네일 후보 수: {len(img_elements)}개")

    if len(img_elements) >= target_count + 30:
        break

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        # 페이지 끝에 도달했을 때 '결과 더보기' 버튼이 있다면 클릭
        try:
            more_btn = driver.find_element(By.CSS_SELECTOR, "input[type='button'], div[role='button']")
            more_btn.click()
            time.sleep(2)
        except Exception:
            break
    last_height = new_height

# 6. 썸네일 이미지 추출 및 저장 (Base64 인코딩 + 외부 URL 모두 처리)
downloaded = 0
saved_sources = set()

for img in img_elements:
    if downloaded >= target_count:
        break

    try:
        # 지연 로딩(Lazy Loading) 해제를 위해 해당 이미지 위치로 화면 스크롤
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", img)
        src = img.get_attribute("src")

        if not src or src in saved_sources:
            continue

        # 검색창 아이콘 등 너무 작은 UI 이미지(80px 미만) 필터링
        width = int(img.get_attribute("naturalWidth") or 0)
        height = int(img.get_attribute("naturalHeight") or 0)
        if width < 80 or height < 80:
            continue

        # 케이스 A: HTML 내부에 Base64 문자열로 포함된 이미지 디코딩 저장
        if src.startswith("data:image/"):
            header, encoded = src.split(",", 1)
            ext = "png" if "png" in header else ("webp" if "webp" in header else "jpg")

            img_bytes = base64.b64decode(encoded)
            file_path = os.path.join(output_dir, f"{query}_thumb_{downloaded + 1:03d}.{ext}")
            with open(file_path, "wb") as f:
                f.write(img_bytes)

            saved_sources.add(src)
            downloaded += 1
            print(f"[{downloaded}/{target_count}] Base64 저장: {file_path} ({width}x{height})")

        # 케이스 B: 구글 썸네일 서버 URL(https://encrypted-tbn0...) 요청 저장
        elif src.startswith("http"):
            resp = requests.get(src, timeout=5)
            if resp.status_code == 200 and len(resp.content) > 2048:
                file_path = os.path.join(output_dir, f"{query}_thumb_{downloaded + 1:03d}.jpg")
                with open(file_path, "wb") as f:
                    f.write(resp.content)

                saved_sources.add(src)
                downloaded += 1
                print(f"[{downloaded}/{target_count}] URL 저장: {file_path} ({width}x{height})")

    except Exception:
        continue

# 7. 브라우저 안전 종료 (Windows 핸들 중복 종료 예외 방지)
try:
    driver.quit()
except Exception:
    pass
finally:
    driver.quit = lambda: None

print(f"\n썸네일 수집 완료! 총 {downloaded}장 저장됨.")

# 8. 수집된 폴더를 zip 압축 파일로 생성
zip_filename = f"{query}_thumbs_{downloaded}"
shutil.make_archive(zip_filename, 'zip', output_dir)
print(f"압축 완료: {zip_filename}.zip")