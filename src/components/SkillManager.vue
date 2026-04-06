<template>
  <div class="skill-manager">
    <h3>技能管理</h3>
    <div class="skill-actions">
      <button @click="loadSkills" class="btn">加载技能</button>
      <button @click="registerSkill" class="btn">注册技能</button>
    </div>
    <div class="skills-list">
      <div v-for="skill in skills" :key="skill.id" class="skill-item">
        <div class="skill-info">
          <h4>{{ skill.name }}</h4>
          <p>{{ skill.description }}</p>
        </div>
        <div class="skill-actions">
          <button @click="executeSkill(skill.id)" class="btn">执行</button>
          <button @click="unregisterSkill(skill.id)" class="btn btn-danger">注销</button>
        </div>
      </div>
    </div>
    <div v-if="skills.length === 0" class="empty-state">
      暂无技能，请点击"加载技能"按钮
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Skill {
  id: string
  name: string
  description: string
  parameters: any[]
}

const skills = ref<Skill[]>([])

async function loadSkills() {
  try {
    const response = await fetch('http://localhost:5000/api/skills')
    if (response.ok) {
      skills.value = await response.json()
    } else {
      console.error('Failed to load skills:', response.statusText)
    }
  } catch (error) {
    console.error('Error loading skills:', error)
  }
}

async function registerSkill() {
  const skillPath = prompt('请输入技能路径:')
  if (skillPath) {
    try {
      const response = await fetch('http://localhost:5000/api/skills/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ skill_path: skillPath })
      })
      if (response.ok) {
        const skill = await response.json()
        skills.value.push(skill)
        alert('技能注册成功')
      } else {
        const error = await response.json()
        alert('技能注册失败: ' + error.error)
      }
    } catch (error) {
      console.error('Error registering skill:', error)
      alert('技能注册失败')
    }
  }
}

async function executeSkill(skillId: string) {
  try {
    const response = await fetch(`http://localhost:5000/api/skills/${skillId}/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ parameters: {} })
    })
    if (response.ok) {
      const result = await response.json()
      alert('技能执行结果: ' + JSON.stringify(result.result))
    } else {
      const error = await response.json()
      alert('技能执行失败: ' + error.error)
    }
  } catch (error) {
    console.error('Error executing skill:', error)
    alert('技能执行失败')
  }
}

async function unregisterSkill(skillId: string) {
  if (confirm('确定要注销这个技能吗？')) {
    try {
      const response = await fetch(`http://localhost:5000/api/skills/${skillId}/unregister`, {
        method: 'DELETE'
      })
      if (response.ok) {
        skills.value = skills.value.filter(skill => skill.id !== skillId)
        alert('技能注销成功')
      } else {
        const error = await response.json()
        alert('技能注销失败: ' + error.error)
      }
    } catch (error) {
      console.error('Error unregistering skill:', error)
      alert('技能注销失败')
    }
  }
}
</script>

<style scoped>
.skill-manager {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.skill-actions {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.btn {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn:hover {
  background-color: #45a049;
}

.btn-danger {
  background-color: #f44336;
}

.btn-danger:hover {
  background-color: #da190b;
}

.skills-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.skill-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.skill-info {
  flex: 1;
}

.skill-info h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.skill-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
  font-style: italic;
}
</style>