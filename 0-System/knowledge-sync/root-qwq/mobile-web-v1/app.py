#!/usr/bin/env python3
"""
AI Team Mobile Web Interface
轻量级手机 Web 界面 - 访问 AI 助理团队
"""

import json
import subprocess
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="AI Team Mobile")

# AI 助理配置
AI_AGENTS = {
    "qwq": {"name": "Qwen Code", "desc": "当前会话", "status": "online"},
    "mycc": {"name": "Claude Code", "desc": "CC 服务器", "status": "online"},
    "gemini": {"name": "Gemini CLI", "desc": "Google", "status": "standby"},
}

class ChatMessage(BaseModel):
    agent: str
    message: str

def run_shell_command(cmd: str, timeout: int = 60) -> str:
    """执行 shell 命令并返回输出"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.stdout or result.stderr or "命令执行完成"
    except subprocess.TimeoutExpired:
        return "命令执行超时"
    except Exception as e:
        return f"错误：{str(e)}"

@app.get("/", response_class=HTMLResponse)
async def index():
    """手机主页"""
    return f'''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Team</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 600px; margin: 0 auto; }}
        .header {{ 
            text-align: center; 
            color: white; 
            margin-bottom: 30px;
            padding: 20px;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 8px; }}
        .header p {{ opacity: 0.9; font-size: 14px; }}
        .agents {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); 
            gap: 15px;
            margin-bottom: 30px;
        }}
        .agent-card {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        .agent-card:active {{ transform: scale(0.98); }}
        .agent-card.selected {{ 
            border: 3px solid #667eea;
            box-shadow: 0 6px 20px rgba(102,126,234,0.4);
        }}
        .agent-icon {{ font-size: 36px; margin-bottom: 10px; }}
        .agent-name {{ font-weight: 600; color: #333; margin-bottom: 4px; }}
        .agent-desc {{ font-size: 12px; color: #666; }}
        .agent-status {{ 
            display: inline-block;
            margin-top: 8px;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 500;
        }}
        .status-online {{ background: #d4edda; color: #155724; }}
        .status-standby {{ background: #fff3cd; color: #856404; }}
        .status-offline {{ background: #f8d7da; color: #721c24; }}
        .chat-box {{
            background: white;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}
        .chat-input {{
            width: 100%;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            padding: 15px;
            font-size: 15px;
            resize: none;
            min-height: 100px;
            margin-bottom: 15px;
        }}
        .chat-input:focus {{ outline: none; border-color: #667eea; }}
        .btn {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 15px 30px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            transition: opacity 0.2s;
        }}
        .btn:active {{ opacity: 0.8; }}
        .btn:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        .response-box {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin-top: 20px;
            max-height: 400px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 13px;
            white-space: pre-wrap;
            word-break: break-word;
        }}
        .quick-actions {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 20px;
        }}
        .quick-btn {{
            background: #f0f0f0;
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 13px;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .quick-btn:active {{ background: #e0e0e0; }}
        .loading {{
            text-align: center;
            padding: 20px;
            color: #666;
        }}
        .spinner {{
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Team</h1>
            <p>你的 AI 助理团队</p>
        </div>
        
        <div class="agents">
            <div class="agent-card selected" onclick="selectAgent('qwq')" id="agent-qwq">
                <div class="agent-icon">🦊</div>
                <div class="agent-name">Qwen Code</div>
                <div class="agent-desc">当前会话</div>
                <div class="agent-status status-online">● 在线</div>
            </div>
            <div class="agent-card" onclick="selectAgent('mycc')" id="agent-mycc">
                <div class="agent-icon">🎯</div>
                <div class="agent-name">Claude</div>
                <div class="agent-desc">CC 服务器</div>
                <div class="agent-status status-online">● 在线</div>
            </div>
            <div class="agent-card" onclick="selectAgent('gemini')" id="agent-gemini">
                <div class="agent-icon">✨</div>
                <div class="agent-name">Gemini</div>
                <div class="agent-desc">Google</div>
                <div class="agent-status status-standby">● 待机</div>
            </div>
        </div>
        
        <div class="chat-box">
            <textarea 
                class="chat-input" 
                id="messageInput" 
                placeholder="输入消息或命令..."
                rows="4"
            ></textarea>
            
            <div class="quick-actions">
                <button class="quick-btn" onclick="quickCommand('sv status')">📊 服务状态</button>
                <button class="quick-btn" onclick="quickCommand('查看任务队列')">📋 任务队列</button>
                <button class="quick-btn" onclick="quickCommand('检查代理连接')">🌐 代理状态</button>
                <button class="quick-btn" onclick="quickCommand('查看用量统计')">📈 用量统计</button>
            </div>
            
            <button class="btn" onclick="sendMessage()" id="sendBtn">
                发送
            </button>
            
            <div class="response-box" id="responseBox" style="display: none;"></div>
        </div>
    </div>
    
    <script>
        let selectedAgent = 'qwq';
        
        function selectAgent(agent) {{
            selectedAgent = agent;
            document.querySelectorAll('.agent-card').forEach(c => c.classList.remove('selected'));
            document.getElementById('agent-' + agent).classList.add('selected');
        }}
        
        function quickCommand(cmd) {{
            document.getElementById('messageInput').value = cmd;
        }}
        
        async function sendMessage() {{
            const input = document.getElementById('messageInput');
            const btn = document.getElementById('sendBtn');
            const responseBox = document.getElementById('responseBox');
            const message = input.value.trim();
            
            if (!message) return;
            
            btn.disabled = true;
            btn.innerHTML = '<div class="loading"><div class="spinner"></div>处理中...</div>';
            responseBox.style.display = 'block';
            responseBox.innerHTML = '<div class="loading"><div class="spinner"></div>正在处理...</div>';
            
            try {{
                const response = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        agent: selectedAgent,
                        message: message
                    }})
                }});
                
                const data = await response.json();
                responseBox.textContent = data.response || '无响应';
            }} catch (error) {{
                responseBox.textContent = '错误：' + error.message;
            }} finally {{
                btn.disabled = false;
                btn.textContent = '发送';
                input.value = '';
            }}
        }}
        
        // 支持回车发送
        document.getElementById('messageInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter' && !e.shiftKey) {{
                e.preventDefault();
                sendMessage();
            }}
        }});
    </script>
</body>
</html>
'''

@app.post("/api/chat")
async def chat(msg: ChatMessage):
    """处理聊天消息"""
    agent = msg.agent
    message = msg.message.lower()
    
    # 简单命令路由
    if "状态" in message or "status" in message:
        if "服务" in message:
            cmd = "/root/bin/sv/sv status"
        elif "代理" in message:
            cmd = "ssh -p 8022 localhost 'cat ~/clash-tunnel.log | tail -5'"
        else:
            cmd = "ps aux | grep -E 'claude|gemini|ssh.*gate' | grep -v grep | head -10"
    elif "任务" in message or "queue" in message:
        cmd = "ls -la /root/air/mycc/shared-tasks-qwq/processing/ /root/air/mycc/shared-tasks-qwq/inbox/"
    elif "用量" in message or "token" in message:
        cmd = "python3 /root/air/qwq/.qwen/skills/qwq-usage/scripts/analyzer.py --days 7"
    elif "代理" in message and "检查" in message:
        cmd = "ssh -p 8022 localhost 'curl -s --socks5-hostname localhost:7891 https://api.ip.sb/ip'"
    else:
        # 默认执行 shell 命令
        cmd = f"echo '收到消息：{message}'\\necho '代理：{agent}'\\necho '时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'"
    
    response = run_shell_command(cmd, timeout=30)
    
    return {"agent": agent, "response": response}

@app.get("/api/agents")
async def list_agents():
    """列出所有助理"""
    return {"agents": AI_AGENTS}

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    print("🚀 启动 AI Team Mobile Web Interface...")
    print("📱 访问地址：http://localhost:8765")
    print("🌐 局域网访问：http://<你的 IP>:8765")
    uvicorn.run(app, host="0.0.0.0", port=8765)
