import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# 添加OpenSpace到Python路径
sys.path.append('E:\\evolving-agent\\OpenSpace-main')

# 添加CLI-Anything到Python路径
sys.path.append('E:\\evolving-agent\\CLI-Anything-main')

from openspace.skill_engine.registry import SkillRegistry
from openspace.skill_engine.store import SkillStore
from openspace.config.loader import load_config

app = Flask(__name__)
CORS(app)

# 加载配置
config = load_config()

# 初始化技能注册表和存储
skill_registry = SkillRegistry()
skill_store = SkillStore()

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """获取所有技能"""
    skills = skill_registry.get_all_skills()
    return jsonify([skill.to_dict() for skill in skills])

@app.route('/api/skills/<skill_id>', methods=['GET'])
def get_skill(skill_id):
    """获取单个技能"""
    skill = skill_registry.get_skill(skill_id)
    if skill:
        return jsonify(skill.to_dict())
    return jsonify({'error': 'Skill not found'}), 404

@app.route('/api/skills/<skill_id>/execute', methods=['POST'])
def execute_skill(skill_id):
    """执行技能"""
    data = request.json
    parameters = data.get('parameters', {})
    
    try:
        result = skill_registry.execute_skill(skill_id, parameters)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills/register', methods=['POST'])
def register_skill():
    """注册新技能"""
    data = request.json
    skill_path = data.get('skill_path')
    
    if not skill_path:
        return jsonify({'error': 'Skill path is required'}), 400
    
    try:
        skill = skill_registry.register_skill(skill_path)
        return jsonify(skill.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills/<skill_id>/unregister', methods=['DELETE'])
def unregister_skill(skill_id):
    """注销技能"""
    try:
        skill_registry.unregister_skill(skill_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tools', methods=['GET'])
def get_tools():
    """获取所有CLI-Anything工具"""
    try:
        # 扫描CLI-Anything目录获取工具列表
        tools_dir = 'E:\\evolving-agent\\CLI-Anything-main'
        tools = []
        
        for item in os.listdir(tools_dir):
            item_path = os.path.join(tools_dir, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, 'setup.py')):
                tools.append({
                    'name': item,
                    'path': item_path
                })
        
        return jsonify(tools)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tools/<tool_name>/execute', methods=['POST'])
def execute_tool(tool_name):
    """执行CLI-Anything工具"""
    data = request.json
    command = data.get('command')
    arguments = data.get('arguments', [])
    
    if not command:
        return jsonify({'error': 'Command is required'}), 400
    
    try:
        tool_path = os.path.join('E:\\evolving-agent\\CLI-Anything-main', tool_name)
        if not os.path.exists(tool_path):
            return jsonify({'error': 'Tool not found'}), 404
        
        # 构建命令
        cmd = [sys.executable, '-m', f'cli_anything.{tool_name}', command] + arguments
        
        # 执行命令
        import subprocess
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=tool_path)
        
        return jsonify({
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)