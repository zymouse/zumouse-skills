# Ansible Runner 完整代码示例

本文档包含详细的代码示例，供需要具体实现时参考。

## 示例 1: 实时监控 Playbook 执行并生成报告

```python
import ansible_runner
import json
from datetime import datetime

class PlaybookMonitor:
    def __init__(self):
        self.task_results = []
        self.failed_tasks = []
        self.start_time = None
    
    def event_handler(self, event_data):
        event = event_data.get('event', '')
        
        if event == 'playbook_on_start':
            self.start_time = datetime.now()
            print(f"[{self.start_time}] Playbook 开始执行")
            
        elif event == 'runner_on_ok':
            host = event_data['event_data'].get('host')
            task = event_data['event_data'].get('task')
            duration = event_data['event_data'].get('duration', 0)
            self.task_results.append({
                'host': host,
                'task': task,
                'status': 'ok',
                'duration': duration
            })
            print(f"  ✓ {host}: {task} ({duration:.2f}s)")
            
        elif event == 'runner_on_failed':
            host = event_data['event_data'].get('host')
            task = event_data['event_data'].get('task')
            self.failed_tasks.append({'host': host, 'task': task})
            print(f"  ✗ {host}: {task} FAILED")
            
        elif event == 'playbook_on_stats':
            print("\n执行统计:")
            stats = event_data['event_data']
            for status, hosts in stats.items():
                if hosts and status in ['ok', 'changed', 'failures', 'unreachable']:
                    print(f"  {status}: {hosts}")
        
        return True
    
    def generate_report(self, result):
        duration = (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        
        report = {
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'duration': duration,
            'status': result.status,
            'rc': result.rc,
            'total_tasks': len(self.task_results),
            'failed_tasks': len(self.failed_tasks),
            'task_details': self.task_results
        }
        
        return report

def main():
    monitor = PlaybookMonitor()
    
    result = ansible_runner.run(
        private_data_dir='/tmp/demo',
        playbook='site.yml',
        event_handler=monitor.event_handler
    )
    
    report = monitor.generate_report(result)
    
    print(f"\n{'='*50}")
    print(f"执行报告")
    print(f"{'='*50}")
    print(f"状态: {report['status']}")
    print(f"返回码: {report['rc']}")
    print(f"耗时: {report['duration']:.2f}s")
    print(f"任务总数: {report['total_tasks']}")
    print(f"失败任务: {report['failed_tasks']}")
    
    # 保存报告
    with open('/tmp/demo/execution_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return result.rc == 0

if __name__ == '__main__':
    exit(0 if main() else 1)
```

## 示例 2: 动态创建执行环境并运行

```python
import ansible_runner
import os
import tempfile
import json

def create_demo_environment(tmpdir):
    """创建临时 Ansible 执行环境"""
    dirs = ['env', 'inventory', 'project']
    for d in dirs:
        os.makedirs(os.path.join(tmpdir, d), exist_ok=True)
    
    # 环境变量
    with open(os.path.join(tmpdir, 'env', 'envvars'), 'w') as f:
        json.dump({'ANSIBLE_STDOUT_CALLBACK': 'json'}, f)
    
    # 额外变量
    extravars = {
        'app_name': 'myapp',
        'app_version': '1.2.3',
        'deploy_env': 'staging'
    }
    with open(os.path.join(tmpdir, 'env', 'extravars'), 'w') as f:
        json.dump(extravars, f)
    
    # 清单文件
    inventory = """[webservers]
web1.example.com ansible_host=192.168.1.10
web2.example.com ansible_host=192.168.1.11

[dbservers]
db1.example.com ansible_host=192.168.1.20

[all:vars]
ansible_user=deploy
ansible_ssh_private_key_file=/home/deploy/.ssh/id_rsa
"""
    with open(os.path.join(tmpdir, 'inventory', 'hosts'), 'w') as f:
        f.write(inventory)
    
    # Playbook
    playbook = """---
- name: Deploy Application
  hosts: webservers
  gather_facts: no
  
  tasks:
    - name: Show deployment info
      debug:
        msg: "Deploying {{ app_name }} v{{ app_version }} to {{ deploy_env }}"
    
    - name: Check connectivity
      ping:
"""
    with open(os.path.join(tmpdir, 'project', 'deploy.yml'), 'w') as f:
        f.write(playbook)

def run_with_dynamic_env():
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            create_demo_environment(tmpdir)
            
            result = ansible_runner.run(
                private_data_dir=tmpdir,
                playbook='deploy.yml',
                verbosity=1
            )
            
            print(f"执行状态: {result.status}")
            print(f"返回码: {result.rc}")
            
            if result.stats:
                print(f"统计: {json.dumps(result.stats, indent=2)}")
            
            return result.rc == 0
            
        except Exception as e:
            print(f"执行失败: {e}")
            return False

if __name__ == '__main__':
    success = run_with_dynamic_env()
    exit(0 if success else 1)
```

## 示例 3: 批量执行多个 Playbook

```python
import ansible_runner
import concurrent.futures
import time

def run_playbook(playbook_name, private_data_dir='/tmp/demo'):
    """执行单个 Playbook"""
    print(f"[开始] {playbook_name}")
    start = time.time()
    
    result = ansible_runner.run(
        private_data_dir=private_data_dir,
        playbook=playbook_name,
        ident=f"batch-{playbook_name.replace('.yml', '')}"
    )
    
    duration = time.time() - start
    print(f"[完成] {playbook_name} - {result.status} ({duration:.2f}s)")
    
    return {
        'playbook': playbook_name,
        'status': result.status,
        'rc': result.rc,
        'duration': duration,
        'stats': result.stats
    }

def run_batch(playbooks, max_workers=3):
    """并行执行多个 Playbook"""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(run_playbook, pb): pb 
            for pb in playbooks
        }
        
        for future in concurrent.futures.as_completed(futures):
            playbook = futures[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"[错误] {playbook}: {e}")
                results.append({
                    'playbook': playbook,
                    'status': 'error',
                    'error': str(e)
                })
    
    return results

def main():
    playbooks = ['setup.yml', 'configure.yml', 'deploy.yml', 'verify.yml']
    
    print(f"批量执行 {len(playbooks)} 个 Playbook...\n")
    
    results = run_batch(playbooks, max_workers=2)
    
    print(f"\n{'='*50}")
    print("批量执行结果:")
    all_success = all(r.get('rc') == 0 for r in results)
    
    for r in results:
        status_icon = "✓" if r.get('rc') == 0 else "✗"
        print(f"{status_icon} {r['playbook']}: {r['status']}")
    
    return all_success

if __name__ == '__main__':
    exit(0 if main() else 1)
```

## 示例 4: 容器执行环境

```python
import ansible_runner

# 基本容器执行
result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    playbook='site.yml',
    process_isolation=True,
    container_image='quay.io/ansible/ansible-runner:latest',
    process_isolation_executable='podman'
)

# 带卷挂载的容器执行
result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    playbook='site.yml',
    process_isolation=True,
    container_image='my-ee:latest',
    container_volume_mounts=[
        '/host/data:/container/data:Z',
        '/home/user/.ssh:/root/.ssh:ro',
    ]
)

# 容器内执行命令
out, err, rc = ansible_runner.run_command(
    executable_cmd='ansible-playbook',
    cmdline_args=['site.yml', '-i', 'inventory'],
    process_isolation=True,
    container_image='network-ee:latest',
    container_volume_mounts=['/home/user/.ssh:/root/.ssh:ro']
)
```

## 示例 5: 远程作业执行（Receptor）

```python
import ansible_runner
import subprocess

# 在本地打包作业
transmit_result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    playbook='test.yml',
    streamer='transmit'
)

# transmit_result.stdout 包含二进制流，可以传输到远程

# 在远程主机执行（worker 阶段）
# ansible-runner worker < transmit.stream

# 处理返回的结果（process 阶段）
process_result = ansible_runner.run(
    private_data_dir='/tmp/demo',
    streamer='process',
    ident='remote-job-001'
)
```

## 示例 6: 错误处理最佳实践

```python
import ansible_runner

def safe_run_playbook(private_data_dir, playbook):
    try:
        result = ansible_runner.run(
            private_data_dir=private_data_dir,
            playbook=playbook
        )
        
        if result.rc != 0:
            print(f"Playbook 执行失败，返回码: {result.rc}")
            
            # 获取错误输出
            with result.stderr as f:
                stderr = f.read()
                if stderr:
                    print(f"错误输出: {stderr}")
            
            # 检查特定主机失败
            if result.stats and result.stats.get('failures'):
                print(f"失败主机: {result.stats['failures']}")
            
            return False
        
        return True
        
    except Exception as e:
        print(f"执行异常: {e}")
        return False
```

## 示例 7: 资源清理

```python
import shutil
import os

def cleanup_old_artifacts(private_data_dir, keep_last=10):
    """保留最近 N 次执行的 artifacts"""
    artifacts_dir = os.path.join(private_data_dir, 'artifacts')
    
    if not os.path.exists(artifacts_dir):
        return
    
    runs = sorted(os.listdir(artifacts_dir))
    for old_run in runs[:-keep_last]:
        old_path = os.path.join(artifacts_dir, old_run)
        print(f"清理旧目录: {old_path}")
        shutil.rmtree(old_path)
```
