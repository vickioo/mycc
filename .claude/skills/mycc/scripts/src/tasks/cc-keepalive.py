#!/usr/bin/env python3
"""
cc 守护进程 - 高可用保障
• 监控：cc2wechat-daemon / free-claude-code / mihomo
• 每30秒检查一次，连续2次失败触发重启
• 最多重启5次，超过停止并报警
• 稳定运行10分钟后重置计数器
• 通过微信 cc2wechat 推送报警
"""
import subprocess, json, time, os, signal, sys, socket
from datetime import datetime

# ── 配置 ──────────────────────────────────────────────────
SERVICES = [
    {
        'name': 'cc2wechat-daemon',
        'port': None,
        'cmd': 'node /home/vicki/.npm-global/bin/cc2wechat start',
        'pattern': 'cc2wechat',
    },
    {
        'name': 'free-claude-code',
        'port': 8082,
        'cmd': 'cd /home/vicki/aihub/free-claude-code && /home/vicki/aihub/free-claude-code/.venv/bin/python3 -m uvicorn server:app --host 0.0.0.0 --port 8082',
        'pattern': 'free-claude-code',
    },
    {
        'name': 'clash-meta',
        'port': 9090,
        'cmd': '/home/vicki/aihub/free-claude-code/mihomo -d /home/vicki/aihub/free-claude-code/config.yaml',
        'pattern': 'mihomo',
    },
]

PID_FILE = '/tmp/cc-keepalive.pid'
LOG_FILE = '/tmp/cc-keepalive.log'
COUNT_FILE = '/tmp/cc-keepalive-count.txt'
MAX_RESTARTS = 5
CHECK_INTERVAL = 30
PM2 = '/home/vicki/.npm-global/bin/pm2'
REPLY = 'node /home/vicki/.npm-global/lib/node_modules/@aster110/cc2wechat/dist/reply-cli.js --text'
WECHAT_ON = True  # False to disable WeChat alerts


# ── 工具函数 ──────────────────────────────────────────────
def log(msg, level='INFO'):
    ts = datetime.now().strftime('%m-%d %H:%M:%S')
    line = f'[{ts}] [{level}] {msg}'
    print(line)
    with open(LOG_FILE, 'a') as f:
        f.write(line + '\n')


def send_wechat(msg):
    if not WECHAT_ON:
        return
    try:
        subprocess.run(
            f'{REPLY} "{msg.replace(chr(34), chr(92)+chr(34))}"',
            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10
        )
    except Exception as e:
        log(f'WeChat发送失败: {e}', 'WARN')


def get_restart_count():
    try:
        return int(open(COUNT_FILE).read().strip())
    except:
        return 0


def set_restart_count(n):
    with open(COUNT_FILE, 'w') as f:
        f.write(str(n))


def is_port_open(port, timeout=2):
    """检测端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False


def check_pm2(name):
    """通过 PM2 检查进程状态"""
    try:
        out = subprocess.check_output(f'{PM2} jlist', shell=True, text=True, timeout=5)
        for p in json.loads(out):
            if p['name'] == name:
                return p['pm2_env']['status'] == 'online', p['pm2_env'].get('restart_time', 0)
    except:
        pass
    return False, 0


def check_service(svc):
    """综合检查：PM2状态 + 端口开放"""
    online, restarts = check_pm2(svc['name'])
    if svc['port'] is None:
        port_ok = True
    else:
        port_ok = is_port_open(svc['port'])
    return online and port_ok


def restart_service(svc):
    """通过 PM2 重启服务"""
    log(f'重启 {svc["name"]}...')
    try:
        subprocess.run(f'{PM2} restart {svc["name"]}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=10)
        time.sleep(5)
        if check_service(svc):
            log(f'{svc["name"]} 重启成功', 'OK')
            return True
        else:
            log(f'{svc["name"]} 重启后仍异常', 'ERROR')
            return False
    except Exception as e:
        log(f'重启 {svc["name"]} 失败: {e}', 'ERROR')
        return False


def stop():
    """停止守护进程"""
    if os.path.exists(PID_FILE):
        pid = int(open(PID_FILE).read().strip())
        try:
            os.kill(pid, signal.SIGTERM)
            log('守护进程已停止')
        except:
            pass
        try:
            os.remove(PID_FILE)
        except:
            pass
    else:
        log('守护进程未运行')


def health_check():
    """一次完整健康检查，返回 (全部健康, 失败列表)"""
    failed = []
    for svc in SERVICES:
        ok = check_service(svc)
        if not ok:
            failed.append(svc)
            port_str = f"port {svc['port']}" if svc['port'] else "进程"
            log(f'{svc["name"]} 异常 ({port_str} {"离线" if svc["port"] and not is_port_open(svc["port"]) else "PM2异常或进程不在"})', 'WARN')
    return len(failed) == 0, failed


def status():
    """打印状态摘要"""
    results = []
    for svc in SERVICES:
        ok = check_service(svc)
        port_str = f"port {svc['port']}" if svc['port'] else "no port"
        results.append(f'  {"✅" if ok else "❌"} {svc["name"]:22s} {port_str}')
    return '\n'.join(results)


# ── 主循环 ──────────────────────────────────────────────
def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'start'

    if cmd == 'stop':
        stop()
        sys.exit(0)

    if cmd == 'status':
        log(f'=== cc 守护状态 ===\n{status()}', 'INFO')
        sys.exit(0)

    if cmd == 'check':
        ok, failed = health_check()
        if ok:
            log('健康检查通过', 'OK')
        else:
            log(f'异常: {[s["name"] for s in failed]}', 'WARN')
        sys.exit(0 if ok else 1)

    # start / restart
    if cmd not in ('start', 'restart'):
        print(f'用法: {sys.argv[0]} start|stop|status|check')
        sys.exit(1)

    if cmd == 'restart':
        stop()
        time.sleep(2)

    # 检查是否已在运行
    if os.path.exists(PID_FILE):
        old_pid = int(open(PID_FILE).read().strip())
        try:
            os.kill(old_pid, 0)
            log(f'守护进程已在运行 (PID {old_pid})', 'WARN')
            sys.exit(1)
        except:
            pass

    # 写 PID
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    log('━━━━━━━━━━━━━━━━━━━━')
    log('cc 守护进程启动')
    log(f'监控服务: {", ".join(s["name"] for s in SERVICES)}')
    log(f'检查间隔: {CHECK_INTERVAL}秒')
    log(f'最大重启: {MAX_RESTARTS}次')
    log('━━━━━━━━━━━━━━━━━━━━')

    consecutive_failures = 0
    stable_since = time.time()

    # 优雅退出
    def handler(signum, frame):
        stop()
        sys.exit(0)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    while True:
        ok, failed = health_check()

        if ok:
            log('健康检查通过', 'OK')
            consecutive_failures = 0
            # 稳定运行10分钟 → 重置计数
            if time.time() - stable_since >= 600:
                count = get_restart_count()
                if count > 0:
                    set_restart_count(0)
                    log('计数器已重置（稳定运行10分钟）', 'INFO')
                stable_since = time.time()
        else:
            consecutive_failures += 1
            log(f'健康检查失败 (连续 {consecutive_failures} 次)', 'WARN')

            if consecutive_failures >= 2:
                count = get_restart_count()
                if count >= MAX_RESTARTS:
                    msg = f'🚨 cc守护：达到最大重启次数({MAX_RESTARTS})，停止自动恢复，请人工检查！'
                    log(msg, 'CRITICAL')
                    send_wechat(msg)
                    stop()
                    sys.exit(1)

                # 重启失败的服务
                for svc in failed:
                    ok2 = restart_service(svc)
                    if not ok2:
                        send_wechat(f'⚠️ cc守护：{svc["name"]} 重启失败，请检查')
                        set_restart_count(count + 1)
                consecutive_failures = 0
                stable_since = time.time()

        time.sleep(CHECK_INTERVAL)


if __name__ == '__main__':
    main()
