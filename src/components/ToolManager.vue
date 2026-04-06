<template>
  <div class="tool-manager">
    <h3>工具管理</h3>
    <div class="tool-actions">
      <button @click="loadTools" class="btn">加载工具</button>
    </div>
    <div class="tools-list">
      <div v-for="tool in tools" :key="tool.name" class="tool-item">
        <div class="tool-info">
          <h4>{{ tool.name }}</h4>
          <p>{{ tool.path }}</p>
        </div>
        <div class="tool-actions">
          <button @click="executeTool(tool.name)" class="btn">执行</button>
        </div>
      </div>
    </div>
    <div v-if="tools.length === 0" class="empty-state">
      暂无工具，请点击"加载工具"按钮
    </div>
    
    <!-- 工具执行对话框 -->
    <div v-if="showExecuteDialog" class="dialog-overlay">
      <div class="dialog">
        <h4>执行工具</h4>
        <div class="form-group">
          <label>命令:</label>
          <input v-model="toolCommand" placeholder="输入命令..." />
        </div>
        <div class="form-group">
          <label>参数:</label>
          <input v-model="toolArguments" placeholder="输入参数，用空格分隔..." />
        </div>
        <div class="dialog-actions">
          <button @click="showExecuteDialog = false" class="btn">取消</button>
          <button @click="confirmExecuteTool" class="btn">执行</button>
        </div>
      </div>
    </div>
    
    <!-- 执行结果对话框 -->
    <div v-if="showResultDialog" class="dialog-overlay">
      <div class="dialog">
        <h4>执行结果</h4>
        <div class="result-content">
          <div class="result-section">
            <h5>标准输出:</h5>
            <pre>{{ toolResult.stdout }}</pre>
          </div>
          <div class="result-section">
            <h5>错误输出:</h5>
            <pre>{{ toolResult.stderr }}</pre>
          </div>
          <div class="result-section">
            <h5>返回代码:</h5>
            <p>{{ toolResult.returncode }}</p>
          </div>
        </div>
        <div class="dialog-actions">
          <button @click="showResultDialog = false" class="btn">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Tool {
  name: string
  path: string
}

interface ToolResult {
  stdout: string
  stderr: string
  returncode: number
}

const tools = ref<Tool[]>([])
const showExecuteDialog = ref(false)
const showResultDialog = ref(false)
const currentTool = ref('')
const toolCommand = ref('')
const toolArguments = ref('')
const toolResult = ref<ToolResult>({ stdout: '', stderr: '', returncode: 0 })

async function loadTools() {
  try {
    const response = await fetch('http://localhost:5000/api/tools')
    if (response.ok) {
      tools.value = await response.json()
    } else {
      console.error('Failed to load tools:', response.statusText)
    }
  } catch (error) {
    console.error('Error loading tools:', error)
  }
}

function executeTool(toolName: string) {
  currentTool.value = toolName
  toolCommand.value = ''
  toolArguments.value = ''
  showExecuteDialog.value = true
}

async function confirmExecuteTool() {
  if (!currentTool.value || !toolCommand.value) return
  
  const argumentsArray = toolArguments.value.split(' ').filter(arg => arg.trim() !== '')
  
  try {
    const response = await fetch(`http://localhost:5000/api/tools/${currentTool.value}/execute`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 
        command: toolCommand.value, 
        arguments: argumentsArray 
      })
    })
    
    if (response.ok) {
      toolResult.value = await response.json()
      showExecuteDialog.value = false
      showResultDialog.value = true
    } else {
      const error = await response.json()
      alert('工具执行失败: ' + error.error)
    }
  } catch (error) {
    console.error('Error executing tool:', error)
    alert('工具执行失败')
  }
}
</script>

<style scoped>
.tool-manager {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.tool-actions {
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

.tools-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.tool-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.tool-info {
  flex: 1;
}

.tool-info h4 {
  margin: 0 0 5px 0;
  color: #333;
}

.tool-info p {
  margin: 0;
  color: #666;
  font-size: 14px;
  word-break: break-all;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #999;
  font-style: italic;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.result-content {
  margin-top: 15px;
}

.result-section {
  margin-bottom: 15px;
}

.result-section h5 {
  margin: 0 0 5px 0;
  color: #333;
}

.result-section pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  max-height: 200px;
}
</style>