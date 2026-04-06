<template>
  <div id="app">
    <h1>AI Assistant</h1>
    <div class="card">
      <h2>聊天界面</h2>
      <div class="chat-container">
        <div class="chat-messages" ref="messagesContainer">
          <div v-for="(message, index) in visibleMessages" :key="index" :class="['message', message.type]">
            <div v-if="message.type === 'image'" class="message-image">
              <img :src="message.content" alt="Image" />
            </div>
            <div v-else-if="message.type === 'file'" class="message-file">
              <a :href="message.content" target="_blank">{{ message.filename }}</a>
            </div>
            <div v-else>
              {{ message.content }}
            </div>
          </div>
        </div>
        <div class="chat-input">
          <div class="input-tools">
            <button @click="selectImage" class="tool-btn">
              🖼️
            </button>
            <button @click="startVoiceInput" class="tool-btn">
              🎤
            </button>
            <button @click="selectFile" class="tool-btn">
              📁
            </button>
          </div>
          <input v-model="inputMessage" @keyup.enter="sendMessage" placeholder="输入消息..." />
          <button @click="sendMessage" class="send-btn">发送</button>
          <input type="file" ref="fileInput" style="display: none" @change="handleFileSelect" />
          <input type="file" ref="imageInput" accept="image/*" style="display: none" @change="handleImageSelect" />
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
    <div class="card">
      <SkillManager />
    </div>
    <div class="card">
      <ToolManager />
    </div>
    <div class="card">
      <DesktopPet />
    </div>
    <div class="card">
      <SystemIntegration />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, defineAsyncComponent, computed } from 'vue'

// 懒加载组件
const SkillManager = defineAsyncComponent(() => import('./components/SkillManager.vue'))
const ToolManager = defineAsyncComponent(() => import('./components/ToolManager.vue'))
const DesktopPet = defineAsyncComponent(() => import('./components/DesktopPet.vue'))
const SystemIntegration = defineAsyncComponent(() => import('./components/SystemIntegration.vue'))

interface Message {
  type: 'user' | 'ai' | 'image' | 'file'
  content: string
  filename?: string
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
const fileInput = ref<HTMLInputElement | null>(null)
const imageInput = ref<HTMLInputElement | null>(null)
const messagesContainer = ref<HTMLElement | null>(null)

// 虚拟滚动：只显示最近的50条消息
const visibleMessages = computed(() => {
  if (messages.value.length <= 50) {
    return messages.value
  }
  return messages.value.slice(-50)
})

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
    // 滚动到底部
    scrollToBottom()
  }, 1000)
  
  // 清空输入
  inputMessage.value = ''
  
  // 滚动到底部
  scrollToBottom()
}

// 滚动到聊天底部
function scrollToBottom() {
  setTimeout(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  }, 100)
}

function toggleModule(moduleId: string) {
  const module = modules.value.find(m => m.id === moduleId)
  if (module) {
    module.status = module.status === 'active' ? 'inactive' : 'active'
  }
}

// 多模态交互函数
function selectImage() {
  if (imageInput.value) {
    imageInput.value.click()
  }
}

function selectFile() {
  if (fileInput.value) {
    fileInput.value.click()
  }
}

function startVoiceInput() {
  // 检查浏览器是否支持语音识别
  if ('webkitSpeechRecognition' in window) {
    const recognition = new (window as any).webkitSpeechRecognition()
    recognition.lang = 'zh-CN'
    recognition.continuous = false
    recognition.interimResults = false
    
    recognition.onstart = () => {
      alert('语音输入已开始，请说话...')
    }
    
    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript
      inputMessage.value = transcript
    }
    
    recognition.onerror = (event: any) => {
      console.error('语音识别错误:', event.error)
      alert('语音识别失败，请重试')
    }
    
    recognition.onend = () => {
      alert('语音输入已结束')
    }
    
    recognition.start()
  } else {
    alert('您的浏览器不支持语音识别功能')
  }
}

function handleImageSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    const reader = new FileReader()
    
    reader.onload = (e) => {
      const result = e.target?.result as string
      messages.value.push({ type: 'image', content: result })
      
      // 模拟AI回复
      setTimeout(() => {
        messages.value.push({ type: 'ai', content: '我收到了你的图片，看起来不错！' })
      }, 1000)
    }
    
    reader.readAsDataURL(file)
  }
}

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files[0]) {
    const file = target.files[0]
    const reader = new FileReader()
    
    reader.onload = (e) => {
      const result = e.target?.result as string
      messages.value.push({ 
        type: 'file', 
        content: result, 
        filename: file.name 
      })
      
      // 模拟AI回复
      setTimeout(() => {
        messages.value.push({ type: 'ai', content: `我收到了你的文件：${file.name}` })
      }, 1000)
    }
    
    reader.readAsDataURL(file)
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
  align-items: center;
  padding: 10px;
  background-color: #fff;
  border-top: 1px solid #ccc;
  gap: 10px;
}

.input-tools {
  display: flex;
  gap: 5px;
}

.tool-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 4px;
  background-color: #f0f0f0;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-btn:hover {
  background-color: #e0e0e0;
}

.chat-input input {
  flex: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.send-btn {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.send-btn:hover {
  background-color: #45a049;
}

.message-image img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
}

.message-file a {
  color: #4CAF50;
  text-decoration: none;
  font-weight: 500;
}

.message-file a:hover {
  text-decoration: underline;
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