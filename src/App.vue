<template>
  <div id="app">
    <h1>AI Assistant</h1>
    <div class="card">
      <h2>聊天界面</h2>
      <div class="chat-container">
        <div class="chat-messages">
          <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
            {{ message.content }}
          </div>
        </div>
        <div class="chat-input">
          <input v-model="inputMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
          <button @click="sendMessage">发送</button>
        </div>
      </div>
    </div>
    <div class="card">
      <h2>模块管理</h2>
      <div class="modules-list">
        <div v-for="module in modules" :key="module.id" class="module-item">
          {{ module.name }} - {{ module.status }}
          <button @click="toggleModule(module.id)">{{ module.status === 'active' ? '停用' : '启用' }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Message {
  type: 'user' | 'ai'
  content: string
}

interface Module {
  id: string
  name: string
  status: 'active' | 'inactive'
}

const messages = ref<Message[]>([
  { type: 'ai', content: '你好！我是你的AI助手，有什么可以帮助你的吗？' }
])

const inputMessage = ref('')

const modules = ref<Module[]>([
  { id: 'chat', name: '聊天模块', status: 'active' },
  { id: 'desktop-pet', name: '桌面宠物', status: 'inactive' },
  { id: 'file-processing', name: '文件处理', status: 'inactive' },
  { id: 'web-processing', name: '网页处理', status: 'inactive' },
  { id: 'image-processing', name: '图片处理', status: 'inactive' }
])

function sendMessage() {
  if (inputMessage.value.trim() === '') return
  
  // 添加用户消息
  messages.value.push({ type: 'user', content: inputMessage.value })
  
  // 模拟AI回复
  setTimeout(() => {
    messages.value.push({ type: 'ai', content: `你刚才说：${inputMessage.value}` })
  }, 1000)
  
  // 清空输入
  inputMessage.value = ''
}

function toggleModule(moduleId: string) {
  const module = modules.value.find(m => m.id === moduleId)
  if (module) {
    module.status = module.status === 'active' ? 'inactive' : 'active'
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 300px;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  padding: 10px;
  overflow-y: auto;
  background-color: #f5f5f5;
}

.message {
  margin: 5px 0;
  padding: 10px;
  border-radius: 8px;
  max-width: 80%;
}

.message.user {
  background-color: #e3f2fd;
  align-self: flex-end;
  margin-left: auto;
}

.message.ai {
  background-color: #f1f1f1;
  align-self: flex-start;
}

.chat-input {
  display: flex;
  padding: 10px;
  background-color: #fff;
  border-top: 1px solid #ccc;
}

.chat-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
}

.modules-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.module-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>