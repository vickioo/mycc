import requests
import time
import datetime
import os
import json

# ==============================================================================
# AtomGit / GitCode AI - 2M Token 自动续期脚本
# 运行方式: pm2 start atomgit_renew.py --name atomgit-renew --interpreter python3
# ==============================================================================

# 请在浏览器中登录 atomgit.com/ai 后按 F12，在 Network 找到请求并复制完整 Cookie
# 或者通过环境变量传入
COOKIE = os.environ.get("ATOMGIT_COOKIE", "你的完整Cookie内容写在这里")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Referer": "https://atomgit.com/ai/models",
    "Accept": "application/json, text/plain, */*"
}

# 根据社区抓包的常见领取接口（可能随平台更新变化）
CLAIM_URL = "https://atomgit.com/api/v1/ai/models/claim"
# 或者使用签到接口
CHECKIN_URL = "https://atomgit.com/api/v1/ai/user/checkin"

def renew_token():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] 正在尝试自动续期 AtomGit 2M Token...")
    
    if "你的完整Cookie内容" in COOKIE:
        print(f"[{now}] 错误: 请先在脚本或环境变量中配置你的真实 Cookie！")
        return False

    try:
        # 尝试调用领取接口
        response = requests.post(CLAIM_URL, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            print(f"[{now}] 续领接口返回: {json.dumps(res_json, ensure_ascii=False)}")
        elif response.status_code == 404:
            # Fallback 尝试签到接口
            res2 = requests.post(CHECKIN_URL, headers=HEADERS, timeout=10)
            print(f"[{now}] 签到接口返回: {res2.status_code} - {res2.text}")
        else:
            print(f"[{now}] 续领失败，状态码: {response.status_code}, 返回: {response.text}")
            
    except Exception as e:
        print(f"[{now}] 请求异常: {str(e)}")

if __name__ == "__main__":
    print("===================================================")
    print("🚀 AtomGit AI Token 自动续领守护进程已启动")
    print("检查间隔: 每 6 小时触发一次 (确保度过 12 小时冷却期)")
    print("===================================================")
    
    while True:
        renew_token()
        # 每 6 小时 (21600 秒) 检查并尝试续领一次
        time.sleep(21600)
