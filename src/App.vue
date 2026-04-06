<template>
  <div id="app">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-brand">
        <h1>AI Assistant</h1>
      </div>
      <div class="navbar-menu">
        <button @click="activeTab = 'chat'" :class="['nav-btn', activeTab === 'chat' ? 'active' : '']">聊天</button>
        <button @click="activeTab = 'modules'" :class="['nav-btn', activeTab === 'modules' ? 'active' : '']">模块</button>
        <button @click="activeTab = 'skills'" :class="['nav-btn', activeTab === 'skills' ? 'active' : '']">技能</button>
        <button @click="activeTab = 'tools'" :class="['nav-btn', activeTab === 'tools' ? 'active' : '']">工具</button>
        <button @click="activeTab = 'pet'" :class="['nav-btn', activeTab === 'pet' ? 'active' : '']">宠物</button>
        <button @click="activeTab = 'system'" :class="['nav-btn', activeTab === 'system' ? 'active' : '']">系统</button>
        <button @click="activeTab = 'settings'" :class="['nav-btn', activeTab === 'settings' ? 'active' : '']">设置</button>
      </div>
    </nav>

    <!-- 主内容区 -->
    <div class="main-content">
      <!-- 聊天界面 -->
      <div v-if="activeTab === 'chat'" class="card">
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

      <!-- 模块管理 -->
      <div v-if="activeTab === 'modules'" class="card">
        <h2>模块管理</h2>
        <div class="modules-list">
          <div v-for="module in modules" :key="module.id" class="module-item">
            <span>{{ module.name }}</span>
            <span :class="['status-badge', module.status]">{{ module.status === 'active' ? '启用' : '停用' }}</span>
            <button @click="toggleModule(module.id)" :class="['toggle-btn', module.status]">{{ module.status === 'active' ? '停用' : '启用' }}</button>
          </div>
        </div>
      </div>

      <!-- 技能管理 -->
      <div v-if="activeTab === 'skills'" class="card">
        <SkillManager />
      </div>

      <!-- 工具管理 -->
      <div v-if="activeTab === 'tools'" class="card">
        <ToolManager />
      </div>

      <!-- 桌面宠物 -->
      <div v-if="activeTab === 'pet'" class="card">
        <DesktopPet />
      </div>

      <!-- 系统集成 -->
      <div v-if="activeTab === 'system'" class="card">
        <SystemIntegration />
      </div>

      <!-- 设置界面 -->
      <div v-if="activeTab === 'settings'" class="card">
        <h2>设置</h2>
        <div class="settings-container">
          <div class="settings-section">
            <h3>外观设置</h3>
            <div class="setting-item">
              <label>主题</label>
              <select v-model="settings.theme">
                <option value="light">浅色</option>
                <option value="dark">深色</option>
                <option value="system">跟随系统</option>
              </select>
            </div>
            <div class="setting-item">
              <label>字体大小</label>
              <input type="range" v-model="settings.fontSize" min="12" max="20" />
              <span>{{ settings.fontSize }}px</span>
            </div>
          </div>

          <div class="settings-section">
            <h3>AI设置</h3>
            <div class="setting-item">
              <label>模型</label>
              <select v-model="settings.model">
                <option value="gpt-4">GPT-4</option>
                <option value="gpt-3.5-turbo">GPT-3.5 Turbo</option>
                <option value="claude-3">Claude 3</option>
              </select>
            </div>
            <div class="setting-item">
              <label>API密钥</label>
              <input type="password" v-model="settings.apiKey" placeholder="输入API密钥" />
            </div>
          </div>

          <div class="settings-section">
            <h3>系统设置</h3>
            <div class="setting-item">
              <label>开机自启</label>
              <input type="checkbox" v-model="settings.startup" />
            </div>
            <div class="setting-item">
              <label>托盘图标</label>
              <input type="checkbox" v-model="settings.trayIcon" />
            </div>
          </div>

          <button @click="saveSettings" class="save-btn">保存设置</button>
        </div>
      </div>
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

// 导航栏状态
const activeTab = ref('chat')

// 设置选项
const settings = ref({
  theme: 'light',
  fontSize: 16,
  model: 'gpt-4',
  apiKey: '',
  startup: false,
  trayIcon: true
})

// 保存设置
function saveSettings() {
  // 这里可以添加保存设置的逻辑，例如存储到localStorage
  localStorage.setItem('ai-assistant-settings', JSON.stringify(settings.value))
  alert('设置已保存')
}

// 加载设置
function loadSettings() {
  const savedSettings = localStorage.getItem('ai-assistant-settings')
  if (savedSettings) {
    settings.value = JSON.parse(savedSettings)
  }
}

// 初始化加载设置
loadSettings()

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
/* 全局样式 */
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* 导航栏 */
.navbar {
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.navbar-menu {
  display: flex;
  gap: 1rem;
}

.nav-btn {
  background: none;
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.nav-btn.active {
  background-color: #3498db;
  font-weight: 500;
}

/* 主内容区 */
.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* 卡片样式 */
.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.card h2 {
  margin-top: 0;
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

/* 聊天界面 */
.chat-container {
  display: flex;
  flex-direction: column;
  height: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background-color: #fafafa;
}

.chat-messages {
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.message {
  margin: 0.5rem 0;
  padding: 0.75rem 1rem;
  border-radius: 18px;
  max-width: 80%;
  line-height: 1.4;
}

.message.user {
  background-color: #3498db;
  color: white;
  align-self: flex-end;
  margin-left: auto;
  border-bottom-right-radius: 4px;
}

.message.ai {
  background-color: #f1f1f1;
  color: #333;
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.chat-input {
  display: flex;
  align-items: center;
  padding: 1rem;
  background-color: white;
  border-top: 1px solid #e0e0e0;
  gap: 0.75rem;
}

.input-tools {
  display: flex;
  gap: 0.5rem;
}

.tool-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #e0e0e0;
  border-radius: 50%;
  background-color: white;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.tool-btn:hover {
  background-color: #f0f0f0;
  border-color: #3498db;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-input input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 20px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.chat-input input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.send-btn {
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.send-btn:hover {
  background-color: #2980b9;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
}

.send-btn:active {
  transform: translateY(0);
}

.message-image img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message-file a {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.message-file a:hover {
  color: #2980b9;
  text-decoration: underline;
}

/* 模块管理 */
.modules-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-top: 1rem;
}

.module-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fafafa;
  transition: all 0.3s ease;
}

.module-item:hover {
  border-color: #3498db;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.toggle-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.toggle-btn.active {
  background-color: #dc3545;
  color: white;
  border-color: #dc3545;
}

.toggle-btn.inactive {
  background-color: #28a745;
  color: white;
  border-color: #28a745;
}

.toggle-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 设置界面 */
.settings-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.settings-section {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.25rem;
  background-color: #fafafa;
}

.settings-section h3 {
  margin-top: 0;
  color: #2c3e50;
  font-size: 1.125rem;
  margin-bottom: 1rem;
}

.setting-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e0e0e0;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-item label {
  font-weight: 500;
  color: #333;
}

.setting-item select,
.setting-item input[type="password"] {
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 1rem;
  min-width: 200px;
}

.setting-item input[type="range"] {
  flex: 1;
  margin: 0 1rem;
}

.setting-item input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.save-btn {
  align-self: flex-start;
  padding: 0.75rem 1.5rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.save-btn:hover {
  background-color: #218838;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(40, 167, 69, 0.3);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }

  .navbar-menu {
    flex-wrap: wrap;
    justify-content: center;
  }

  .main-content {
    padding: 1rem;
  }

  .chat-container {
    height: 300px;
  }

  .module-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .module-item button {
    align-self: flex-end;
  }

  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .setting-item select,
  .setting-item input[type="password"] {
    width: 100%;
  }
}
</style>