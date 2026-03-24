#!/usr/bin/env python3
"""
Remmina 远程桌面操控脚本
list        → 列出已保存连接
connect <名> → 连接指定桌面
screenshot  → 截图远程桌面窗口
status     → 检查连接状态
"""
import subprocess, glob, configparser, sys, os

REMOTE_DISPLAY = ':0'
REMMINA_BASE = '/home/vicki/.local/share/remmina/'

def cmd(c, timeout=8):
    r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip(), r.returncode

def list_profiles():
    profiles = []
    for f in glob.glob(REMMINA_BASE + '*.remmina'):
        cfg = configparser.ConfigParser()
        try:
            cfg.read(f)
            if 'remmina' in cfg:
                s = cfg['remmina']
                profiles.append({
                    'name': s.get('name', os.path.basename(f)),
                    'protocol': s.get('protocol', '?'),
                    'server': s.get('server', '?'),
                    'file': os.path.basename(f),
                })
        except:
            pass
    return profiles

def find_remmina_window():
    out, _ = cmd('xdotool search --name "Remmina"')
    wids = [w for w in out.strip().split('\n') if w and w.startswith('0x')]
    return wids[0] if wids else None

if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'list'

    if arg == 'list':
        profiles = list_profiles()
        icons = {'RDP': '🖥️', 'SSH': '🐚', 'VNC': '🖥️', 'SFTP': '📁'}
        print(f'📡 Remmina 已保存连接 ({len(profiles)}个)')
        for i, p in enumerate(profiles, 1):
            icon = icons.get(p['protocol'], '🔗')
            print(f'  {i}. {icon} {p["name"]} → {p["server"]} ({p["protocol"]})')

    elif arg == 'connect':
        name = sys.argv[2] if len(sys.argv) > 2 else ''
        profiles = list_profiles()
        matched = [p for p in profiles if name.lower() in p['name'].lower()]
        if not matched:
            print(f'未找到匹配 "{name}" 的连接')
            sys.exit(1)
        p = matched[0]
        print(f'🔗 连接: {p["name"]} → {p["server"]}')
        remmina_file = REMMINA_BASE + p['file']
        subprocess.Popen(f'DISPLAY={REMOTE_DISPLAY} remmina -c {remmina_file}',
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f'Remmina 已启动，请等待连接建立')

    elif arg == 'screenshot':
        wid = find_remmina_window()
        path = '/tmp/remmina_win.png'
        if wid:
            _, rc = cmd(f'DISPLAY={REMOTE_DISPLAY} maim -i {wid} {path}')
            if rc != 0:
                cmd(f'DISPLAY={REMOTE_DISPLAY} maim {path}')
        else:
            cmd(f'DISPLAY={REMOTE_DISPLAY} maim {path}')
        print(f'截图: {path} ({os.path.getsize(path)//1024}KB)')

    elif arg == 'status':
        wid = find_remmina_window()
        if wid:
            out, _ = cmd(f'xdotool getwindowname {wid}')
            print(f'🖥️ 已连接: {out.strip()} (WID={wid})')
        else:
            print('❌ 未发现 Remmina 窗口')

    else:
        print('用法: remmina-ctrl.py list|connect <名称>|screenshot|status')
