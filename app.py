import subprocess, os, uvicorn, json, asyncio, httpx, re
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import edge_tts

app = FastAPI()

# --- 核心配置 ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AI_TEAM_TOKEN = 'ceecee-super-team-8822'
COOKIE_KEY = "ai_hub_session"
ONE_API_URL = "http://127.0.0.1:8082/v1/messages?beta=true"

# --- Agent 注册表 (遵循顶层架构设计) ---
AGENT_REGISTRY = {
    "gemini": {
        "name": "✨ Gemini-Pro", 
        "url": "https://api.mycc.dev/QSTF2T", # 这里可以根据实际情况切换
        "model": "gemini-1.5-pro",
        "type": "coordinator",
        "status": "online"
    },
    "mycc": {
        "name": "🎯 MyCC-Claude", 
        "url": "https://api.mycc.dev/QSTF2T", 
        "model": "claude-3-5-sonnet-20241022",
        "type": "cloud_sync",
        "status": "online"
    },
    "lobster": {
        "name": "🦞 龙虾-Surface", 
        "url": ONE_API_URL, 
        "model": "claude-3-5-haiku-20241022",
        "type": "heavy_duty",
        "status": "online"
    },
    "qwq": {
        "name": "🦊 千问-Local", 
        "url": ONE_API_URL, 
        "model": "claude-3-5-sonnet-20241022",
        "type": "local_coding",
        "status": "online"
    }
}

# --- 鉴权中间件 (收紧安全性) ---
@app.middleware('http')
async def auth_middleware(request: Request, call_next):
    # 强制公开路径：仅限登录页面和健康检查
    strictly_public = ["/login", "/api/health", "/api/login"]
    
    # 静态资源放行 (允许加载 CSS/JS/Manifest 等，但不放行 HTML)
    is_asset = any(request.url.path.endswith(ext) for ext in [".css", ".js", ".png", ".jpg", ".json", ".webmanifest", ".ico"])
    
    if request.url.path in strictly_public or is_asset:
        return await call_next(request)

    # 验证 Token (Cookie 或 Header)
    cookie_token = request.cookies.get(COOKIE_KEY)
    header_token = request.headers.get('X-AI-Token')
    
    if cookie_token == AI_TEAM_TOKEN or header_token == AI_TEAM_TOKEN:
        return await call_next(request)
    
    # 未授权则重定向至登录 (如果是 API 请求则返回 403)
    if request.url.path.startswith("/api/"):
        return HTMLResponse(status_code=403, content="Access Denied")
    return RedirectResponse(url="/login")

# --- 登录与健康检查 ---
@app.get("/login")
async def login_page():
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Team - 授权验证</title>
        <style>
            body {{ background: #0f172a; color: #f1f5f9; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; font-family: system-ui; }}
            .login-card {{ background: #1e293b; padding: 2.5rem; border-radius: 1.5rem; border: 1px solid #334155; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); width: 100%; max-width: 400px; text-align: center; }}
            input {{ width: 100%; padding: 0.8rem; margin: 1.5rem 0; background: #0f172a; border: 1px solid #334155; border-radius: 0.8rem; color: white; text-align: center; font-size: 1.1rem; }}
            button {{ width: 100%; padding: 0.8rem; background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; border-radius: 0.8rem; color: white; font-weight: 600; cursor: pointer; transition: opacity 0.2s; }}
            button:hover {{ opacity: 0.9; }}
        </style>
    </head>
    <body>
        <div class="login-card">
            <h2 style="margin:0; background: linear-gradient(135deg, #6366f1, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">AI Teamwork</h2>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 0.5rem;">请输入团队授权码以访问系统</p>
            <input type="password" id="token" placeholder="Authorization Token">
            <button onclick="login()">激活进入</button>
        </div>
        <script>
            function login() {{
                const token = document.getElementById('token').value;
                document.cookie = "{COOKIE_KEY}=" + token + "; path=/; max-age=2592000"; // 30天有效期
                location.href = "/";
            }}
        </script>
    </body>
    </html>
    """)

@app.get("/api/health")
async def health(): return {"status": "ok", "timestamp": datetime.now().isoformat()}

# --- 主页面路由 (修正路径) ---
@app.get("/")
async def root(): return FileResponse(os.path.join(BASE_DIR, "intranet-hub.html"))

@app.get("/chat")
async def chat_page(): return FileResponse(os.path.join(BASE_DIR, "chat.html"))

@app.get("/hub-v2")
async def old_hub(): return FileResponse(os.path.join(BASE_DIR, "hub.html"))

# --- 核心 API ---
@app.get("/api/agents")
async def get_agents(): return AGENT_REGISTRY

class ChatMessage(BaseModel):
    agent: str
    message: str

@app.post("/api/chat")
async def chat(msg: ChatMessage):
    at_match = re.match(r'^@(\w+)\s+', msg.message)
    current_agent = msg.agent
    clean_message = msg.message
    
    if at_match:
        target_agent = at_match.group(1)
        if target_agent in AGENT_REGISTRY:
            current_agent = target_agent
            clean_message = msg.message[len(at_match.group(0)):].strip()
            
    agent_info = AGENT_REGISTRY.get(current_agent, AGENT_REGISTRY["mycc"])
    
    async def stream_generator():
        target_model = agent_info.get("model", "claude-3-5-sonnet-20241022")
        api_url = agent_info.get("url")
        
        payload = {
            "model": target_model,
            "messages": [{"role": "user", "content": clean_message}],
            "max_tokens": 4096,
            "stream": True
        }
        
        async with httpx.AsyncClient() as client:
            try:
                async with client.stream("POST", api_url, json=payload, timeout=120.0) as response:
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:].strip()
                            if data_str == "[DONE]": break
                            try:
                                data = json.loads(data_str)
                                if data.get('type') == 'content_block_delta':
                                    content = data['delta'].get('text', '')
                                    if content:
                                        yield f"data: {json.dumps({'content': content})}\n\n"
                            except: continue
            except Exception as e:
                yield f"data: {json.dumps({'content': f'❌ 云端记忆同步失败: {str(e)}'})}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream")

# --- 知识库路由 (修正静态资源路径) ---
@app.get("/knowledge")
@app.get("/kb")
async def knowledge_base():
    return FileResponse(os.path.join(BASE_DIR, "knowledge", "index-docsify.html"))

@app.get("/knowledge/{path:path}")
async def knowledge_file(path: str):
    file_path = os.path.join(BASE_DIR, "knowledge", path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

# --- 辅助 API ---
@app.get("/api/tts")
async def tts(text: str):
    clean_text = re.sub(r'[*#>`\-]', '', text).strip()
    return StreamingResponse(edge_tts.Communicate(clean_text, "zh-CN-XiaoxiaoNeural").stream(), media_type="audio/mpeg")

@app.get("/api/architecture")
async def get_arch(): return FileResponse("/root/AI_TEAMWORK_ARCHITECTURE.md")

# --- 挂载静态资源 (最关键的一步) ---
# 允许加载根目录下的 css/js/png 等文件
app.mount("/static", StaticFiles(directory=BASE_DIR), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8766)
