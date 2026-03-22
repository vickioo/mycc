#!/usr/bin/env python3
"""
模型切换工具
支持在不同AI模型之间快速切换，包括主要模型和备用模型
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from urllib.parse import urlencode

# 模型配置
MODELS = {
    "primary": {
        "glm47": {
            "name": "GLM4.7",
            "model": "z-ai/glm4.7",
            "endpoint": "https://integrate.api.nvidia.com/v1",
            "description": "智谱AI的GLM4.7模型，支持多轮对话和复杂推理",
            "stability": "稳定",
            "estimated_uptime": "1+ months",
            "apiKey": "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",
            "platform": "nvidia"
        },
        "antigravity": {
            "name": "Antigravity Manager",
            "model": "antigravity/manager",
            "endpoint": "http://192.168.100.228:8045/v1",
            "description": "Antigravity Manager的API代理服务，支持多种模型",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "antigravity-admin-2026",
            "platform": "custom"
        },
        # 联通云 - Plan-Lite 套餐 (优先)
        "unicom-glm5": {
            "name": "GLM5 (联通云)",
            "model": "glm-5",
            "endpoint": "https://aigw-gzgy2.cucloud.cn:8443/v1",
            "description": "联通云 - 智谱 GLM5，Plan-Lite 套餐优先",
            "stability": "稳定",
            "estimated_uptime": "至2026-04-04",
            "apiKey": "sk-1pC3T7x9LvHmZrFNgE8K6QwPqDSj2BdYuW5ZoX4AyC0ZlV7k",
            "platform": "unicom"
        },
        "unicom-qwen3-397b": {
            "name": "Qwen3.5 397B (联通云)",
            "model": "Qwen3.5-397B-A17B",
            "endpoint": "https://aigw-gzgy2.cucloud.cn:8443/v1",
            "description": "联通云 - 阿里 Qwen3.5 397B MoE",
            "stability": "稳定",
            "estimated_uptime": "至2026-04-04",
            "apiKey": "sk-1pC3T7x9LvHmZrFNgE8K6QwPqDSj2BdYuW5ZoX4AyC0ZlV7k",
            "platform": "unicom"
        },
        "unicom-minimax": {
            "name": "MiniMax M2.5 (联通云)",
            "model": "MiniMax-M2.5",
            "endpoint": "https://aigw-gzgy2.cucloud.cn:8443/v1",
            "description": "联通云 - MiniMax M2.5 Pro",
            "stability": "稳定",
            "estimated_uptime": "至2026-04-04",
            "apiKey": "sk-1pC3T7x9LvHmZrFNgE8K6QwPqDSj2BdYuW5ZoX4AyC0ZlV7k",
            "platform": "unicom"
        },
        # 联通云 - 免费额度 (备用)
        "unicom-free-glm5": {
            "name": "GLM5 (联通云免费)",
            "model": "glm-5",
            "endpoint": "https://aigw-gzgy2.cucloud.cn:8443/v1",
            "description": "联通云 - 免费额度备用",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-rPgmo2UrLU6DmUp16AhhbTGlgWjgAbBA",
            "platform": "unicom-free"
        },
        "minimax": {
            "name": "Minimax M2.1",
            "model": "minimaxai/minimax-m2.1",
            "endpoint": "https://integrate.api.nvidia.com/v1",
            "description": "Minimax的M2.1模型，擅长中文理解和生成",
            "stability": "稳定",
            "estimated_uptime": "1+ months",
            "apiKey": "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",
            "platform": "nvidia"
        },
        "kimi": {
            "name": "KIMI",
            "model": "moonshotai/kimi-k2.5",
            "endpoint": "https://integrate.api.nvidia.com/v1",
            "description": "月之暗面的KIMI K2.5模型，知识覆盖广泛",
            "stability": "稳定",
            "estimated_uptime": "1+ months",
            "apiKey": "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",
            "platform": "nvidia"
        },
        "oneapi-glm5": {
            "name": "GLM5 (OneAPI)",
            "model": "z-ai/glm5",
            "endpoint": "http://localhost:3000/v1",
            "description": "本地 OneAPI - 智谱 GLM5",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f",
            "platform": "oneapi"
        },
        "oneapi-ds-v3.2": {
            "name": "DeepSeek V3.2 (OneAPI)",
            "model": "Pro/deepseek-ai/DeepSeek-V3.2",
            "endpoint": "http://localhost:3000/v1",
            "description": "本地 OneAPI - DeepSeek V3.2 Pro",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f",
            "platform": "oneapi"
        },
        "oneapi-kimi-think": {
            "name": "KIMI K2 Thinking (OneAPI)",
            "model": "moonshotai/kimi-k2-thinking",
            "endpoint": "http://localhost:3000/v1",
            "description": "本地 OneAPI - KIMI K2 推理模型",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f",
            "platform": "oneapi"
        },
        "oneapi-qwen3.5": {
            "name": "Qwen3.5 397B (OneAPI)",
            "model": "qwen/qwen3.5-397b-a17b",
            "endpoint": "http://localhost:3000/v1",
            "description": "本地 OneAPI - 通义千问3.5 397B MoE",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f",
            "platform": "oneapi"
        },
        "oneapi-minimax": {
            "name": "Minimax M2.5 (OneAPI)",
            "model": "Pro/MiniMaxAI/MiniMax-M2.5",
            "endpoint": "http://localhost:3000/v1",
            "description": "本地 OneAPI - Minimax M2.5 Pro",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f",
            "platform": "oneapi"
        },
        "oneapi-step": {
            "name": "Step 3.5 Flash (OneAPI)",
            "model": "stepfun-ai/Step-3.5-Flash",
            "endpoint": "http://localhost:3000/v1",
            "description": "本地 OneAPI - 阶跃星辰 Step 3.5 Flash",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-WuYeAKrS317KiCSUB549A3Cb62B24f05A31a207b8bB1Ed4f",
            "platform": "oneapi"
        }
    },
    "alternatives": {
        "deepseek-v3": {
            "name": "DeepSeek V3",
            "model": "deepseek-ai/DeepSeek-V3",
            "endpoint": "https://api.siliconflow.cn/v1",
            "description": "硅基流动 - DeepSeek V3，高性能开源模型",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-tvsikylgqyqawlcyxwhtpnavgjedrsgnwshfgggtahpcriln",
            "platform": "siliconflow"
        },
        "deepseek-r1": {
            "name": "DeepSeek R1",
            "model": "deepseek-ai/DeepSeek-R1",
            "endpoint": "https://api.siliconflow.cn/v1",
            "description": "硅基流动 - DeepSeek R1，推理能力强",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-tvsikylgqyqawlcyxwhtpnavgjedrsgnwshfgggtahpcriln",
            "platform": "siliconflow"
        },
        "qwen2.5-7b": {
            "name": "Qwen2.5 7B",
            "model": "Qwen/Qwen2.5-7B-Instruct",
            "endpoint": "https://api.siliconflow.cn/v1",
            "description": "硅基流动 - 通义千问2.5 7B，轻量高效",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-tvsikylgqyqawlcyxwhtpnavgjedrsgnwshfgggtahpcriln",
            "platform": "siliconflow"
        },
        "qwen2.5-72b": {
            "name": "Qwen2.5 72B",
            "model": "Qwen/Qwen2.5-72B-Instruct",
            "endpoint": "https://api.siliconflow.cn/v1",
            "description": "硅基流动 - 通义千问2.5 72B，能力更强",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-tvsikylgqyqawlcyxwhtpnavgjedrsgnwshfgggtahpcriln",
            "platform": "siliconflow"
        },
        "llama3.1-8b": {
            "name": "Llama 3.1 8B",
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
            "endpoint": "https://api.siliconflow.cn/v1",
            "description": "硅基流动 - Meta Llama 3.1 8B，开源标杆",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-tvsikylgqyqawlcyxwhtpnavgjedrsgnwshfgggtahpcriln",
            "platform": "siliconflow"
        },
        "glm-4-9b": {
            "name": "GLM-4 9B",
            "model": "THUDM/glm-4-9b-chat",
            "endpoint": "https://api.siliconflow.cn/v1",
            "description": "硅基流动 - 清华 GLM-4 9B，中文友好",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "sk-tvsikylgqyqawlcyxwhtpnavgjedrsgnwshfgggtahpcriln",
            "platform": "siliconflow"
        },
        "llama3": {
            "name": "Llama 3",
            "model": "meta/llama3-70b",
            "endpoint": "https://integrate.api.nvidia.com/v1",
            "description": "Meta的Llama 3 70B模型，通用能力强",
            "stability": "稳定",
            "estimated_uptime": "1+ months",
            "apiKey": "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",
            "platform": "nvidia"
        },
        "gemini": {
            "name": "Gemini Pro",
            "model": "google/gemini-pro",
            "endpoint": "https://integrate.api.nvidia.com/v1",
            "description": "Google的Gemini Pro模型，多模态能力强",
            "stability": "稳定",
            "estimated_uptime": "1+ months",
            "apiKey": "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",
            "platform": "nvidia"
        },
        "google-ai-studio-1.5-pro": {
            "name": "Gemini 1.5 Pro",
            "model": "gemini-1.5-pro",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
            "description": "Google Gemini 1.5 Pro - 最强大的多模态模型，2M token上下文",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "AIzaSyChYNDikBt20m9grkOAWhNXzD6eY7Je06g",
            "platform": "google"
        },
        "google-ai-studio-flash": {
            "name": "Gemini 1.5 Flash",
            "model": "gemini-1.5-flash",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
            "description": "Google Gemini 1.5 Flash - 更快更高效的模型",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "AIzaSyChYNDikBt20m9grkOAWhNXzD6eY7Je06g",
            "platform": "google"
        },
        "google-ai-studio-pro-002": {
            "name": "Gemini 1.5 Pro 002",
            "model": "gemini-1.5-pro-002",
            "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
            "description": "Google Gemini 1.5 Pro 002 - Pro的新版本",
            "stability": "稳定",
            "estimated_uptime": "长期",
            "apiKey": "AIzaSyChYNDikBt20m9grkOAWhNXzD6eY7Je06g",
            "platform": "google"
        },
        "claude": {
            "name": "Claude 3 Haiku",
            "model": "anthropic/claude-3-haiku-20240307",
            "endpoint": "https://integrate.api.nvidia.com/v1",
            "description": "Anthropic的Claude 3 Haiku模型，响应速度快",
            "stability": "稳定",
            "estimated_uptime": "1+ months",
            "apiKey": "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",
            "platform": "nvidia"
        }
    }
}

# Claude Code 配置文件路径
SETTINGS_FILE = os.path.expanduser("~/.claude/settings.json")

class ModelSwitcher:
    """模型切换器"""

    def __init__(self):
        self.config = self._load_config()
        self.current_model = self._detect_current_model()

    def _load_config(self):
        """加载 Claude Code 配置"""
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载配置文件失败: {e}")
        return {"env": {}, "includeCoAuthoredBy": False}

    def _detect_current_model(self):
        """从配置中检测当前使用的模型"""
        env = self.config.get("env", {})
        base_url = env.get("ANTHROPIC_BASE_URL", "")

        # 根据 endpoint 查找匹配的模型
        for category in MODELS.values():
            for model_id, model_info in category.items():
                if model_info["endpoint"] in base_url:
                    return model_id
        return None

    def _save_config(self):
        """保存配置到 Claude Code"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
            # 备份当前配置
            if os.path.exists(SETTINGS_FILE):
                backup_file = f"{SETTINGS_FILE}.bak"
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    with open(backup_file, "w", encoding="utf-8") as bf:
                        bf.write(f.read())
            # 保存新配置
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False

    def list_models(self):
        """列出可用模型"""
        print("=== 可用模型列表 ===")
        print()

        print("1. 主要模型:")
        for model_id, model_info in MODELS["primary"].items():
            status = "✅ 当前" if self.current_model == model_id else ""
            print(f"   - {model_id}: {model_info['name']} ({model_info['model']}) {status}")
            print(f"     描述: {model_info['description']}")
            print(f"     稳定性: {model_info['stability']}")
            print(f"     预计可用时间: {model_info['estimated_uptime']}")
        print()

        print("2. 备用模型:")
        for model_id, model_info in MODELS["alternatives"].items():
            status = "✅ 当前" if self.current_model == model_id else ""
            print(f"   - {model_id}: {model_info['name']} ({model_info['model']}) {status}")
            print(f"     描述: {model_info['description']}")
            print(f"     稳定性: {model_info['stability']}")
            print(f"     预计可用时间: {model_info['estimated_uptime']}")
        print()

        if self.current_model:
            current_model_info = self.get_model_info(self.current_model)
            if current_model_info:
                print(f"当前使用的模型: {current_model_info['name']} ({self.current_model})")
        else:
            print("当前使用: 智谱 GLM (通过 open.bigmodel.cn)")

    def get_model_info(self, model_id):
        """获取模型信息"""
        if model_id in MODELS["primary"]:
            return MODELS["primary"][model_id]
        elif model_id in MODELS["alternatives"]:
            return MODELS["alternatives"][model_id]
        return None

    def switch_model(self, model_id):
        """切换到指定模型"""
        model_info = self.get_model_info(model_id)
        if not model_info:
            print(f"❌ 未找到模型: {model_id}")
            return False

        print(f"切换到模型: {model_info['name']} ({model_id})")
        print(f"模型ID: {model_info['model']}")
        print(f"端点: {model_info['endpoint']}")
        print(f"稳定性: {model_info['stability']}")
        print(f"预计可用时间: {model_info['estimated_uptime']}")

        # 测试模型可用性
        if self.test_model(model_id):
            # 更新配置
            self.config.setdefault("env", {})
            self.config["env"]["ANTHROPIC_BASE_URL"] = model_info["endpoint"]
            self.config["env"]["ANTHROPIC_AUTH_TOKEN"] = model_info["apiKey"]
            self.config["env"]["ANTHROPIC_MODEL"] = model_info["model"]
            self.config["env"]["ANTHROPIC_DEFAULT_SONNET_MODEL"] = model_info["model"]
            self.config["env"]["ANTHROPIC_DEFAULT_OPUS_MODEL"] = model_info["model"]
            self.config["env"]["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = model_info["model"]

            if self._save_config():
                self.current_model = model_id
                print(f"✅ 模型切换成功！当前模型: {model_info['name']}")
                print(f"⚠️  请重启 Claude Code 以使更改生效")
                return True
            else:
                print("❌ 保存配置失败")
                return False
        else:
            print(f"❌ 模型 {model_id} 测试失败，切换被取消")
            return False

    def test_model(self, model_id):
        """测试模型可用性"""
        model_info = self.get_model_info(model_id)
        if not model_info:
            print(f"❌ 未找到模型: {model_id}")
            return False

        print(f"测试模型: {model_info['name']}...")

        platform = model_info.get("platform", "openai")

        if platform == "google":
            return self._test_gemini_studio(model_info)
        elif platform == "custom":
            # 自定义端点跳过测试
            print(f"✅ {model_info['name']} (自定义端点，跳过测试)")
            return True
        elif platform == "oneapi":
            return self._test_openai_format(model_info)
        else:
            return self._test_openai_format(model_info)

    def _test_openai_format(self, model_info):
        """测试 OpenAI 兼容格式的 API"""
        endpoint = model_info["endpoint"]
        model = model_info["model"]
        api_key = model_info.get("apiKey")

        if not api_key:
            print(f"⚠️  {model_info['name']} 没有 API Key，跳过测试")
            return False

        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 10
            }

            # 确保完整的 endpoint 路径
            if not endpoint.endswith("/chat/completions"):
                endpoint = f"{endpoint.rstrip('/')}/chat/completions"

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=data,
                headers=headers,
                method="POST"
            )

            timeout = 30 if model_info.get("platform") == "oneapi" else 10
            with urllib.request.urlopen(req, timeout=timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                print(f"✅ 模型 {model_info['name']} 测试成功")
                return True

        except urllib.error.HTTPError as e:
            error_data = e.read().decode("utf-8")
            print(f"❌ 模型 {model_info['name']} 测试失败: HTTP {e.code}")
            if error_data:
                try:
                    error_json = json.loads(error_data)
                    if "error" in error_json:
                        print(f"   错误: {error_json['error'].get('message', error_json['error'])}")
                except:
                    pass
            return False
        except Exception as e:
            print(f"❌ 模型 {model_info['name']} 测试失败: {e}")
            return False

    def _test_gemini_studio(self, model_info):
        """测试 Google AI Studio API"""
        endpoint = model_info["endpoint"]
        api_key = model_info.get("apiKey")
        model = model_info["model"]

        if not api_key:
            print(f"⚠️  {model_info['name']} 没有 API Key，跳过测试")
            return False

        try:
            # Google AI Studio 测试端点
            test_endpoint = f"{endpoint}/{model}:generateContent?key={api_key}"

            payload = {
                "contents": [{"parts": [{"text": "test"}]}]
            }

            headers = {"Content-Type": "application/json"}
            data = json.dumps(payload).encode("utf-8")

            req = urllib.request.Request(
                test_endpoint,
                data=data,
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
                print(f"✅ 模型 {model_info['name']} 测试成功")
                return True

        except urllib.error.HTTPError as e:
            error_data = e.read().decode("utf-8")
            print(f"❌ 模型 {model_info['name']} 测试失败: HTTP {e.code}")
            if error_data:
                try:
                    error_json = json.loads(error_data)
                    if "error" in error_json:
                        print(f"   错误: {error_json['error'].get('message', error_json['error'])}")
                except:
                    print(f"   详情: {error_data[:200]}")
            return False
        except Exception as e:
            print(f"❌ 模型 {model_info['name']} 测试失败: {e}")
            return False

    def check_balance(self):
        """检查各平台余额"""
        print("=== 余额查询 ===")
        print()

        # 硅基流动
        print("1. 硅基流动:")
        sf_models = ["deepseek-v3", "deepseek-r1", "qwen2.5-7b", "qwen2.5-72b",
                     "llama3.1-8b", "glm-4-9b"]
        api_key = None
        for model_id in sf_models:
            model_info = self.get_model_info(model_id)
            if model_info:
                api_key = model_info.get("apiKey")
                break
        if api_key:
            self._check_siliconflow_balance(api_key)
        else:
            print("   ⚠️  未配置 API Key")
        print()

        # NVIDIA
        print("2. NVIDIA API:")
        nv_models = ["glm47", "minimax", "kimi", "llama3", "gemini", "claude"]
        api_keys = {}
        for model_id in nv_models:
            model_info = self.get_model_info(model_id)
            if model_info:
                key = model_info.get("apiKey")
                if key:
                    api_keys[key] = api_keys.get(key, 0) + 1
        print("   ⚠️  NVIDIA 余额需登录 https://build.nvidia.com 查看控制台")
        print(f"   已配置 {len(api_keys)} 个不同的 API Key")
        print()

        # Google AI Studio
        print("3. Google AI Studio:")
        google_models = ["google-ai-studio-1.5-pro", "google-ai-studio-flash", "google-ai-studio-pro-002"]
        api_key = None
        for model_id in google_models:
            model_info = self.get_model_info(model_id)
            if model_info:
                api_key = model_info.get("apiKey")
                break
        if api_key:
            self._check_google_studio_balance(api_key)
        else:
            print("   ⚠️  未配置 API Key")
        print()

    def _check_siliconflow_balance(self, api_key):
        """查询硅基流动余额"""
        try:
            endpoint = "https://api.siliconflow.cn/v1/user/info"
            headers = {"Authorization": f"Bearer {api_key}"}
            req = urllib.request.Request(endpoint, headers=headers, method="GET")

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
                # 打印原始响应用于调试
                # print(f"   调试: {result}")
                if "data" in result:
                    data = result["data"]
                    # 尝试多种可能的余额字段
                    balance = "N/A"
                    total_charge = "N/A"

                    # 方式1: data.balance.total_balance
                    if "balance" in data and isinstance(data["balance"], dict):
                        balance = data["balance"].get("total_balance",
                                  data["balance"].get("balance",
                                  data["balance"].get("remain_balance", "N/A")))

                    # 方式2: data.total_balance 或 data.balance
                    if balance == "N/A":
                        balance = data.get("total_balance",
                                  data.get("balance", "N/A"))

                    # 累计消费
                    total_charge = data.get("total_charge", data.get("total_amount", "N/A"))

                    print(f"   余额: {balance}")
                    print(f"   累计消费: {total_charge}")
                else:
                    print("   ⚠️  无法获取余额信息")

        except urllib.error.HTTPError as e:
            error_data = e.read().decode("utf-8")
            print(f"   ❌ 查询失败: HTTP {e.code}")
            if error_data:
                try:
                    error_json = json.loads(error_data)
                    if "error" in error_json:
                        print(f"   错误: {error_json['error'].get('message', error_json['error'])}")
                except:
                    pass
        except Exception as e:
            print(f"   ❌ 查询失败: {e}")

    def _check_google_studio_balance(self, api_key):
        """查询 Google AI Studio 余额"""
        print("   ⚠️  Google AI Studio 余额需登录 https://aistudio.google.com 查看控制台")

    def auto_select_model(self):
        """自动选择可用模型"""
        print("自动选择可用模型...")

        # 按优先级测试模型
        test_order = [
            "glm47",
            "antigravity",
            "minimax",
            "kimi",
            "deepseek-v3",
            "qwen2.5-72b",
            "llama3",
            "gemini",
        ]

        for model_id in test_order:
            print(f"测试模型: {model_id}...")
            if self.test_model(model_id):
                # 切换到该模型
                model_info = self.get_model_info(model_id)
                self.config.setdefault("env", {})
                self.config["env"]["ANTHROPIC_BASE_URL"] = model_info["endpoint"]
                self.config["env"]["ANTHROPIC_AUTH_TOKEN"] = model_info["apiKey"]
                self.config["env"]["ANTHROPIC_MODEL"] = model_info["model"]
                self.config["env"]["ANTHROPIC_DEFAULT_SONNET_MODEL"] = model_info["model"]
                self.config["env"]["ANTHROPIC_DEFAULT_OPUS_MODEL"] = model_info["model"]
                self.config["env"]["ANTHROPIC_DEFAULT_HAIKU_MODEL"] = model_info["model"]

                if self._save_config():
                    self.current_model = model_id
                    print(f"✅ 自动选择成功！当前模型: {model_info['name']} ({model_id})")
                    print(f"模型描述: {model_info['description']}")
                    print(f"稳定性: {model_info['stability']}")
                    print(f"预计可用时间: {model_info['estimated_uptime']}")
                    print(f"⚠️  请重启 Claude Code 以使更改生效")
                    return True
                else:
                    print("❌ 保存配置失败")
                    return False

        print("❌ 所有模型测试失败，无法自动选择模型")
        return False

    def get_current_model(self):
        """获取当前模型"""
        if self.current_model:
            model_info = self.get_model_info(self.current_model)
            if model_info:
                print(f"当前模型: {model_info['name']} ({self.current_model})")
                print(f"模型ID: {model_info['model']}")
                print(f"端点: {model_info['endpoint']}")
                print(f"描述: {model_info['description']}")
                print(f"稳定性: {model_info['stability']}")
                print(f"预计可用时间: {model_info['estimated_uptime']}")
                return model_info
        else:
            print("当前使用: 智谱 GLM (通过 open.bigmodel.cn)")
            print("提示: 使用 cc-switch 切换到其他模型")
        return None

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="模型切换工具")
    parser.add_argument("--list", action="store_true", help="列出可用模型")
    parser.add_argument("--model", type=str, help="切换到指定模型")
    parser.add_argument("--test", type=str, help="测试模型可用性")
    parser.add_argument("--auto", action="store_true", help="自动选择可用模型")
    parser.add_argument("--current", action="store_true", help="显示当前模型")
    parser.add_argument("--balance", action="store_true", help="查询余额")

    args = parser.parse_args()
    switcher = ModelSwitcher()

    if args.list:
        switcher.list_models()
    elif args.model:
        switcher.switch_model(args.model)
    elif args.test:
        switcher.test_model(args.test)
    elif args.auto:
        switcher.auto_select_model()
    elif args.current:
        switcher.get_current_model()
    elif args.balance:
        switcher.check_balance()
    else:
        # 默认列出模型
        switcher.list_models()

if __name__ == "__main__":
    main()
