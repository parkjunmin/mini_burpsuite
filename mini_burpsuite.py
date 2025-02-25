import requests
import json
import random
import signal

# 랜덤 User-Agent 목록
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

# 세션 객체 생성
session = requests.Session()
session.headers.update({'User-Agent': random.choice(USER_AGENTS)})

# Ctrl + C 시 종료 메시지 출력
def signal_handler(sig, frame):
    print("\n[⚠ 종료] 사용자가 키보드를 통해 취소하였습니다.")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

# 로그인 URL 입력
login_url = input("로그인할 URL을 입력하세요: ").strip()
request_method = input("로그인 요청 방식을 선택하세요 (1: GET, 2: POST): ").strip()

# 요청 방식 설정
if request_method == "1":
    request_method = "GET"
elif request_method == "2":
    request_method = "POST"
else:
    print("[⚠ 오류] 잘못된 입력입니다. 1 또는 2를 선택하세요.")
    exit(1)

# 로그인 데이터 입력
login_data = input("로그인 데이터를 JSON 형식으로 입력하세요 (예: { \"uid\": \"' or 1=1--\", \"passw\": \"' or 1=1--\", \"btnSubmit\": \"Login\" }): ").strip()

# JSON 변환
try:
    login_payload = json.loads(login_data)
except json.JSONDecodeError:
    print("[⚠ 오류] 잘못된 JSON 형식입니다. 올바른 형식으로 입력하세요.")
    exit(1)

# 로그인 요청
try:
    if request_method == "POST":
        response = session.post(login_url, data=login_payload)
    else:
        response = session.get(login_url, params=login_payload)

    if response.status_code == 200:
        print("[✅ 로그인 성공] 로그인 요청이 정상적으로 처리되었습니다.")
        print(f"🔹 저장된 쿠키: {session.cookies.get_dict()}")
    else:
        print(f"[⚠ 로그인 실패] 상태 코드: {response.status_code}")

except requests.RequestException as e:
    print(f"[⚠ 요청 실패] {login_url} → {e}")
    exit(1)

# 로그인 후 세션 유지 및 사용자 입력 루프
while True:
    print("\n🔹 메뉴 선택")
    print("1: URL 요청")
    print("2: 현재 쿠키 확인 및 변경")
    print("3: 종료")
    
    user_choice = input("메뉴 번호를 입력하세요: ").strip().lower()

    if user_choice == "1":
        target_url = input("로그인 후 접근할 페이지 URL을 입력하세요: ").strip()
        if target_url.lower() == "exit":
            print("[✅ 프로그램 종료]")
            break

        # 요청 방식 선택 (1: GET, 2: POST)
        method_choice = input("요청 방식을 선택하세요 (1: GET, 2: POST): ").strip()
        if method_choice == "1":
            method = "GET"
            request_payload = None
        elif method_choice == "2":
            method = "POST"
            request_data = input("요청 데이터를 JSON 형식으로 입력하세요: ").strip()
            try:
                request_payload = json.loads(request_data)
            except json.JSONDecodeError:
                print("[⚠ 오류] 잘못된 JSON 형식입니다.")
                continue
        else:
            print("[⚠ 오류] 잘못된 입력입니다. 1 또는 2를 선택하세요.")
            continue

        try:
            session.headers.update({'User-Agent': random.choice(USER_AGENTS)})  # 요청마다 User-Agent 변경
            if method == "GET":
                response = session.get(target_url, cookies=session.cookies.get_dict())
            else:
                response = session.post(target_url, data=request_payload, cookies=session.cookies.get_dict())

            print(f"\n[✅ 요청 성공] {target_url} (상태 코드: {response.status_code})")
            print(response.text)  # 응답 본문 출력

        except requests.RequestException as e:
            print(f"[⚠ 요청 실패] {target_url} → {e}")

    elif user_choice == "2":
        print("\n🔹 현재 저장된 쿠키:")
        print(json.dumps(session.cookies.get_dict(), indent=4, ensure_ascii=False))  # 쿠키 출력
        
        new_cookies = input("변경할 쿠키 값을 JSON 형식으로 입력하세요 (변경하지 않으려면 엔터): ").strip()
        if new_cookies:
            try:
                cookie_dict = json.loads(new_cookies)
                session.cookies.update(cookie_dict)  # 쿠키 변경
                print("[✅ 쿠키 업데이트 완료]")
            except json.JSONDecodeError:
                print("[⚠ 오류] 잘못된 JSON 형식입니다.")

    elif user_choice == "3":
        print("[✅ 프로그램 종료]")
        break

    else:
        print("[⚠ 오류] 잘못된 입력입니다. 1, 2, 3 중에서 선택하세요.")
