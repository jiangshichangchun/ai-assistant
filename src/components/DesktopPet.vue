<template>
  <div class="desktop-pet">
    <h3>桌面宠物</h3>
    <div class="pet-controls">
      <button @click="togglePet" class="btn">{{ isPetActive ? '隐藏宠物' : '显示宠物' }}</button>
      <button @click="changeModel" class="btn">切换模型</button>
      <button @click="changeAnimation" class="btn">切换动画</button>
    </div>
    <div v-if="isPetActive" class="pet-container">
      <div ref="petCanvas" class="pet-canvas"></div>
      <div class="pet-stats">
        <p>状态: {{ petState }}</p>
        <p>动画: {{ currentAnimation }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'

const isPetActive = ref(false)
const petCanvas = ref<HTMLElement | null>(null)
const petState = ref('idle')
const currentAnimation = ref('idle')

let scene: THREE.Scene
let camera: THREE.PerspectiveCamera
let renderer: THREE.WebGLRenderer
let petModel: THREE.Object3D | null = null
let animationMixer: THREE.AnimationMixer | null = null
let animations: THREE.AnimationClip[] = []
let clock: THREE.Clock

// 可用的模型和动画
const models = [
  { name: 'cat', url: 'https://threejs.org/examples/models/gltf/CesiumMan/CesiumMan.gltf' },
  { name: 'dog', url: 'https://threejs.org/examples/models/gltf/FlightHelmet/FlightHelmet.gltf' },
  { name: 'robot', url: 'https://threejs.org/examples/models/gltf/RobotExpressive/RobotExpressive.gltf' }
]

const animationsList = ['idle', 'walk', 'run', 'celebrate']
let currentModelIndex = 0
let currentAnimationIndex = 0

function togglePet() {
  isPetActive.value = !isPetActive.value
  if (isPetActive.value) {
    initPet()
  } else {
    disposePet()
  }
}

function changeModel() {
  currentModelIndex = (currentModelIndex + 1) % models.length
  if (isPetActive.value) {
    disposePet()
    initPet()
  }
}

function changeAnimation() {
  currentAnimationIndex = (currentAnimationIndex + 1) % animationsList.length
  currentAnimation.value = animationsList[currentAnimationIndex]
  playAnimation(currentAnimation.value)
}

function initPet() {
  if (!petCanvas.value) return

  // 创建场景
  scene = new THREE.Scene()
  scene.background = null

  // 创建相机
  camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000)
  camera.position.z = 5

  // 创建渲染器
  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
  renderer.setSize(200, 200)
  petCanvas.value.appendChild(renderer.domElement)

  // 添加灯光
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
  scene.add(ambientLight)

  const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
  directionalLight.position.set(1, 1, 1)
  scene.add(directionalLight)

  // 加载模型
  const loader = new GLTFLoader()
  const model = models[currentModelIndex]
  
  loader.load(
    model.url,
    (gltf) => {
      petModel = gltf.scene
      scene.add(petModel)

      // 处理动画
      animationMixer = new THREE.AnimationMixer(petModel)
      animations = gltf.animations
      
      // 播放默认动画
      playAnimation('idle')

      // 调整模型大小和位置
      if (petModel) {
        petModel.scale.set(1, 1, 1)
        petModel.position.set(0, -1, 0)
      }
    },
    undefined,
    (error) => {
      console.error('Error loading model:', error)
    }
  )

  // 创建时钟
  clock = new THREE.Clock()

  // 开始动画循环
  animate()
}

function animate() {
  if (!isPetActive.value) return

  requestAnimationFrame(animate)

  const delta = clock.getDelta()
  if (animationMixer) {
    animationMixer.update(delta)
  }

  // 只有在可见时才渲染
  if (petCanvas.value && petCanvas.value.offsetParent !== null) {
    renderer.render(scene, camera)
  }
}

function playAnimation(animationName: string) {
  if (!animationMixer || animations.length === 0) return

  // 停止所有动画
  animationMixer.stopAllAction()

  // 找到并播放指定动画
  const animation = animations.find(clip => clip.name === animationName)
  if (animation) {
    const action = animationMixer.clipAction(animation)
    action.play()
  } else {
    // 如果指定动画不存在，播放第一个动画
    const action = animationMixer.clipAction(animations[0])
    action.play()
  }
}

function disposePet() {
  if (renderer && petCanvas.value) {
    petCanvas.value.removeChild(renderer.domElement)
    renderer.dispose()
  }

  if (scene) {
    scene.clear()
  }

  petModel = null
  animationMixer = null
  animations = []
}

// 监听鼠标移动，让宠物跟随鼠标
function onMouseMove(event: MouseEvent) {
  if (!petModel) return

  const mouseX = (event.clientX / window.innerWidth) * 2 - 1
  const mouseY = -(event.clientY / window.innerHeight) * 2 + 1

  // 让宠物头部跟随鼠标
  if (petModel.children[0]) {
    petModel.children[0].rotation.y = mouseX * 0.5
    petModel.children[0].rotation.x = mouseY * 0.3
  }
}

onMounted(() => {
  window.addEventListener('mousemove', onMouseMove)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  disposePet()
})
</script>

<style scoped>
.desktop-pet {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.pet-controls {
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

.pet-container {
  display: flex;
  gap: 20px;
  align-items: center;
}

.pet-canvas {
  width: 200px;
  height: 200px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.1);
}

.pet-stats {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

.pet-stats p {
  margin: 5px 0;
  color: #333;
}
</style>