<template>
  <div class="system-integration">
    <h3>系统集成</h3>
    <div class="integration-features">
      <div class="feature">
        <h4>全局划词</h4>
        <p>选中任意文本后，使用快捷键 <code>Ctrl+Shift+A</code> 打开AI分析</p>
        <button @click="testClipboard" class="btn">测试剪贴板</button>
        <div v-if="clipboardContent" class="clipboard-content">
          <p>剪贴板内容: {{ clipboardContent }}</p>
        </div>
      </div>
      <div class="feature">
        <h4>系统托盘</h4>
        <p>应用已添加到系统托盘，可通过托盘图标快速访问</p>
        <button @click="toggleTray" class="btn">测试托盘</button>
      </div>
      <div class="feature">
        <h4>全局快捷键</h4>
        <ul class="shortcut-list">
          <li><code>Ctrl+Shift+A</code> - 分析选中文本</li>
          <li><code>Ctrl+Shift+O</code> - 打开应用</li>
          <li><code>Ctrl+Shift+X</code> - 隐藏应用</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const clipboardContent = ref('')

async function testClipboard() {
  try {
    // 暂时注释掉，等待修复
    // const result = await tauri.invoke('get_clipboard_content')
    // clipboardContent.value = result.text
    clipboardContent.value = '测试剪贴板内容'
  } catch (error) {
    console.error('Error getting clipboard content:', error)
  }
}

async function toggleTray() {
  // 测试系统托盘功能
  console.log('Tray toggle clicked')
}

// 注册全局快捷键
function registerGlobalShortcuts() {
  // 这里可以使用Tauri的globalShortcut API注册全局快捷键
  // 由于需要在主进程中注册，这里只是示例
  console.log('Global shortcuts registered')
}

// 监听系统级别的划词事件
function listenForSelection() {
  document.addEventListener('mouseup', async () => {
    const selection = window.getSelection()
    if (selection && selection.toString().trim()) {
      const selectedText = selection.toString().trim()
      console.log('Selected text:', selectedText)
      // 可以在这里触发AI分析
    }
  })
}

// 初始化
registerGlobalShortcuts()
listenForSelection()
</script>

<style scoped>
.system-integration {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.integration-features {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 15px;
}

.feature {
  padding: 15px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.feature h4 {
  margin: 0 0 10px 0;
  color: #333;
}

.feature p {
  margin: 0 0 15px 0;
  color: #666;
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

.clipboard-content {
  margin-top: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f5f5f5;
}

.shortcut-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.shortcut-list li {
  margin: 5px 0;
  padding: 5px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

code {
  background-color: #f0f0f0;
  padding: 2px 4px;
  border-radius: 3px;
  font-family: monospace;
}
</style>