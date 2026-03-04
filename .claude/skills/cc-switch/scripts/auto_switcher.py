#!/usr/bin/env python3
"""
智能自动轮替框架
实现模型故障检测、健康检查和自动切换机制
"""

import argparse
import json
import os
import sys
import time
import threading
import signal
from datetime import datetime, timedelta
from collections import defaultdict, deque
import urllib.request
import urllib.error

# 导入现有的模型配置
sys.path.append('/data/mycc/.claude/skills/cc-switch/scripts')
from switcher import MODELS, CONFIG_FILE, ModelSwitcher

class HealthChecker:
    """健康检查器"""
    
    def __init__(self):
        self.health_status = defaultdict(lambda: {
            'last_check': None,
            'status': 'unknown',  # unknown, healthy, unhealthy
            'failures': 0,
            'success_rate': 1.0,
            'response_times': deque(maxlen=10),
            'last_error': None
        })
        self.check_interval = 300  # 5分钟检查一次
        
    def check_model_health(self, model_id, model_info):
        """检查单个模型健康状态"""
        start_time = time.time()
        
        try:
            # 根据模型类型选择测试方法
            if 'google-ai-studio' in model_id:
                success = self._test_gemini_studio(model_info)
            else:
                success = self._test_openai_format(model_info)
                
            response_time = time.time() - start_time
            
            # 更新健康状态
            status = self.health_status[model_id]
            status['last_check'] = datetime.now()
            
            if success:
                status['status'] = 'healthy'
                status['failures'] = 0
                status['response_times'].append(response_time)
                status['last_error'] = None
            else:
                status['status'] = 'unhealthy'
                status['failures'] += 1
                status['response_times'].append(float('inf'))
                
            # 计算成功率
            recent_checks = list(status['response_times'])
            if recent_checks:
                successful_checks = len([t for t in recent_checks if t != float('inf')])
                status['success_rate'] = successful_checks / len(recent_checks)
                
            return success, response_time
            
        except Exception as e:
            status = self.health_status[model_id]
            status['last_check'] = datetime.now()
            status['status'] = 'unhealthy'
            status['failures'] += 1
            status['last_error'] = str(e)
            return False, float('inf')
    
    def _test_openai_format(self, model_info):
        """测试OpenAI兼容格式的API"""
        endpoint = model_info["endpoint"]
        model = model_info["model"]
        api_key = model_info.get("apiKey")
        
        if not api_key:
            return False
            
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": "health check"}],
                "max_tokens": 10
            }
            
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                endpoint,
                data=data,
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
                return True
                
        except Exception:
            return False
    
    def _test_gemini_studio(self, model_info):
        """测试Google AI Studio API"""
        endpoint = model_info["endpoint"]
        api_key = model_info.get("apiKey")
        
        if not api_key:
            return False
            
        try:
            url = f"{endpoint}?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": "health check"}]}]
            }
            
            headers = {"Content-Type": "application/json"}
            data = json.dumps(payload).encode("utf-8")
            
            req = urllib.request.Request(
                url,
                data=data,
                headers=headers,
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode("utf-8"))
                return True
                
        except Exception:
            return False
    
    def get_healthy_models(self):
        """获取健康的模型列表"""
        healthy_models = []
        for model_id in MODELS["primary"]:
            status = self.health_status[model_id]
            if (status['status'] == 'healthy' and 
                status['success_rate'] >= 0.8 and
                status['failures'] < 3):
                healthy_models.append(model_id)
        return healthy_models

class AutoSwitcher:
    """自动切换器"""
    
    def __init__(self):
        self.switcher = ModelSwitcher()
        self.health_checker = HealthChecker()
        self.running = False
        self.switch_history = deque(maxlen=50)  # 保存最近50次切换记录
        self.preferred_models = ['glm47', 'antigravity', 'minimax', 'kimi']  # 优先级顺序
        
    def start_monitoring(self):
        """开始监控"""
        self.running = True
        print("🚀 启动智能自动轮替监控...")
        print(f"📅 开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 监控间隔: {self.health_checker.check_interval}秒")
        print(f"🔄 优先模型: {', '.join(self.preferred_models)}")
        
        # 注册信号处理器
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            while self.running:
                self._monitor_cycle()
                time.sleep(self.health_checker.check_interval)
        except KeyboardInterrupt:
            print("\n🛑 收到停止信号...")
        finally:
            self.stop_monitoring()
    
    def _monitor_cycle(self):
        """监控周期"""
        print(f"\n🔍 执行健康检查周期 [{datetime.now().strftime('%H:%M:%S')}]")
        
        # 检查所有主要模型
        available_models = []
        
        for model_id in self.preferred_models:
            if model_id in MODELS["primary"]:
                model_info = MODELS["primary"][model_id]
                success, response_time = self.health_checker.check_model_health(model_id, model_info)
                
                status_icon = "✅" if success else "❌"
                avg_time = self._get_avg_response_time(model_id)
                print(f"   {status_icon} {model_id}: {response_time:.2f}s (平均: {avg_time:.2f}s)")
                
                if success:
                    available_models.append(model_id)
        
        # 如果当前模型不健康，自动切换
        current_model = self.switcher.current_model
        current_status = self.health_checker.health_status[current_model]
        
        if current_model and current_status['status'] != 'healthy':
            print(f"⚠️  当前模型 {current_model} 不健康，寻找替代模型...")
            self._switch_to_best_available(available_models, current_model)
        elif not available_models:
            print("🚨 所有优先模型都不可用，检查备用模型...")
            self._check_alternative_models()
        else:
            print(f"✅ 当前模型 {current_model} 健康，无需切换")
    
    def _get_avg_response_time(self, model_id):
        """获取平均响应时间"""
        times = list(self.health_checker.health_status[model_id]['response_times'])
        valid_times = [t for t in times if t != float('inf')]
        return sum(valid_times) / len(valid_times) if valid_times else 0
    
    def _switch_to_best_available(self, available_models, failed_model):
        """切换到最佳可用模型"""
        if not available_models:
            print("❌ 没有可用的替代模型")
            return False
        
        # 选择响应最快的健康模型
        best_model = min(available_models, 
                        key=lambda m: self._get_avg_response_time(m))
        
        if self.switcher.switch_model(best_model):
            # 记录切换历史
            self.switch_history.append({
                'timestamp': datetime.now(),
                'from_model': failed_model,
                'to_model': best_model,
                'reason': 'health_failure'
            })
            print(f"🔄 已切换到 {best_model} (响应时间: {self._get_avg_response_time(best_model):.2f}s)")
            return True
        return False
    
    def _check_alternative_models(self):
        """检查备用模型"""
        print("🔍 检查备用模型...")
        backup_models = ['google-ai-studio-1.5-pro', 'google-ai-studio-flash']
        
        for model_id in backup_models:
            if model_id in MODELS["alternatives"]:
                model_info = MODELS["alternatives"][model_id]
                success, response_time = self.health_checker.check_model_health(model_id, model_info)
                if success:
                    print(f"✅ 发现可用备用模型: {model_id}")
                    if self.switcher.switch_model(model_id):
                        self.switch_history.append({
                            'timestamp': datetime.now(),
                            'from_model': self.switcher.current_model,
                            'to_model': model_id,
                            'reason': 'backup_activation'
                        })
                        return True
        return False
    
    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print(f"\n📡 收到信号 {signum}，准备停止...")
        self.running = False
    
    def stop_monitoring(self):
        """停止监控"""
        self.running = False
        print("🛑 监控已停止")
        self._print_summary()
    
    def _print_summary(self):
        """打印监控摘要"""
        print("\n📊 监控摘要:")
        print(f"   总运行时间: {datetime.now()}")
        print(f"   切换次数: {len(self.switch_history)}")
        
        if self.switch_history:
            print("   切换历史:")
            for record in list(self.switch_history)[-5:]:  # 显示最近5次
                print(f"     {record['timestamp'].strftime('%H:%M:%S')} "
                      f"{record['from_model']} → {record['to_model']} "
                      f"({record['reason']})")

class ModelAnalyzer:
    """模型分析器"""
    
    @staticmethod
    def analyze_models():
        """分析所有模型配置"""
        print("📊 模型配置分析报告")
        print("=" * 50)
        
        total_models = len(MODELS["primary"]) + len(MODELS["alternatives"])
        print(f"总计模型数量: {total_models}")
        print(f"主要模型: {len(MODELS['primary'])}")
        print(f"备用模型: {len(MODELS['alternatives'])}")
        
        # 分析API提供商分布
        providers = defaultdict(int)
        for model_dict in [MODELS["primary"], MODELS["alternatives"]]:
            for model_info in model_dict.values():
                endpoint = model_info["endpoint"]
                if "nvidia.com" in endpoint:
                    providers["NVIDIA"] += 1
                elif "siliconflow.cn" in endpoint:
                    providers["SiliconFlow"] += 1
                elif "googleapis.com" in endpoint:
                    providers["Google AI"] += 1
                elif "192.168.100.228" in endpoint:
                    providers["Antigravity"] += 1
                else:
                    providers["Other"] += 1
        
        print("\nAPI提供商分布:")
        for provider, count in providers.items():
            print(f"   {provider}: {count} 个模型")
        
        # 显示推荐的优先级列表
        print("\n🎯 推荐优先级顺序:")
        priority_list = ['glm47', 'antigravity', 'minimax', 'kimi', 
                        'google-ai-studio-1.5-pro', 'google-ai-studio-flash']
        for i, model in enumerate(priority_list, 1):
            status = "✅" if model in MODELS["primary"] or model in MODELS["alternatives"] else "❌"
            print(f"   {i}. {model} {status}")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="智能自动轮替框架")
    parser.add_argument("--monitor", action="store_true", help="启动持续监控")
    parser.add_argument("--analyze", action="store_true", help="分析模型配置")
    parser.add_argument("--once", action="store_true", help="执行一次健康检查")
    parser.add_argument("--interval", type=int, default=300, help="监控间隔(秒)")
    
    args = parser.parse_args()
    
    if args.analyze:
        ModelAnalyzer.analyze_models()
    elif args.once:
        auto_switcher = AutoSwitcher()
        auto_switcher._monitor_cycle()
    elif args.monitor:
        auto_switcher = AutoSwitcher()
        auto_switcher.health_checker.check_interval = args.interval
        auto_switcher.start_monitoring()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()