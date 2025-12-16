<script setup>
import Header from "@/components/Header.vue";
import { ref, onMounted } from 'vue';

const isLoaded = ref(false);

onMounted(() => {
  setTimeout(() => {
    isLoaded.value = true;
  }, 100);
});
</script>

<template>
  <div class="back-ground">
    <Header class="header"></Header>
    <div class="bg-decorations">
      <div class="decoration-circle decoration-1"></div>
      <div class="decoration-circle decoration-2"></div>
      <div class="decoration-circle decoration-3"></div>
      <div class="floating-elements">
        <div class="floating-element element-1"></div>
        <div class="floating-element element-2"></div>
        <div class="floating-element element-3"></div>
      </div>
    </div>

    <section class="main-section">
      <div class="container">
        <el-row :gutter="40">
          <el-col :xs="24" :lg="14">
            <div class="hero-content" :class="{ 'loaded': isLoaded }">
              <div class="hero-badge">
                <span class="badge-icon">🔬</span>
                <span>AI-Powered TCM Diagnosis</span>
              </div>

              <h1 class="gradient-title">
                <span class="title-line">Intelligent</span>
                <span class="title-line highlight">Tongue Diagnosis</span>
                <span class="title-line">Revolution</span>
              </h1>

              <p class="subtitle">
                Experience the future of Traditional Chinese Medicine with our cutting-edge AI technology.
                Get instant, accurate tongue diagnosis and personalized health insights powered by deep learning.
              </p>

              <div class="feature-tags">
                <span class="tag">✨ AI-Powered</span>
                <span class="tag">📱 Instant Results</span>
                <span class="tag">🏥 TCM Integration</span>
              </div>

              <div class="cta-section">
                <router-link to="/check" class="cta-button primary">
                  <span class="button-text">Start Diagnosis</span>
                  <div class="button-icon">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="currentColor" stroke-width="2"/>
                    </svg>
                  </div>
                </router-link>
              </div>
            </div>
          </el-col>

          <el-col :xs="24" :lg="10">
            <div class="card-group" :class="{ 'loaded': isLoaded }">
              <div class="featured-card">
                <div class="card-header">
                  <div class="card-icon featured">
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                      <path d="M12 2L15.09 8.26L22 9L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9L8.91 8.26L12 2Z"
                            fill="currentColor"/>
                    </svg>
                  </div>
                  <div class="card-badge">Featured</div>
                </div>
                <h3>AI Tongue Analysis</h3>
                <p>Advanced deep learning algorithms analyze tongue characteristics with 95%+ accuracy,
                  providing comprehensive TCM diagnosis in seconds.</p>
                <div class="card-stats">
                  <div class="stat">
                    <span class="stat-value">80%+</span>
                    <span class="stat-label">Accuracy</span>
                  </div>
                  <div class="stat">
                    <span class="stat-value">&lt;40s</span>
                    <span class="stat-label">Analysis Time</span>
                  </div>
                </div>
              </div>

              <el-card class="feature-card">
                <div class="card-content">
                  <div class="card-icon">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
                      <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z"
                            stroke="currentColor" stroke-width="2"/>
                    </svg>
                  </div>
                  <h3>Health Tracking</h3>
                  <p>Monitor your health journey with detailed reports, historical comparisons, and personalized recommendations.</p>
                  <div class="card-features">
                    <span class="feature-item">📊 Visual Reports</span>
                    <span class="feature-item">📈 Progress Tracking</span>
                  </div>
                </div>
              </el-card>

              <el-card class="feature-card">
                <div class="card-content">
                  <div class="card-icon">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
                      <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88M13 7C13 9.20914 11.2091 11 9 11C6.79086 11 5 9.20914 5 7C5 4.79086 6.79086 3 9 3C11.2091 3 13 4.79086 13 7Z"
                            stroke="currentColor" stroke-width="2"/>
                    </svg>
                  </div>
                  <h3>Expert Consultation</h3>
                  <p>Connect with certified TCM practitioners for detailed consultations and treatment recommendations.</p>
                  <div class="card-features">
                    <span class="feature-item">👨‍⚕️ Certified Experts</span>
                    <span class="feature-item">💬 Real-time Chat</span>
                  </div>
                </div>
              </el-card>
            </div>
          </el-col>
        </el-row>
      </div>
    </section>
  </div>
</template>

<style scoped>
.back-ground {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  position: relative;
  overflow: hidden;
}

.bg-decorations {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

.decoration-1 {
  width: 300px;
  height: 300px;
  top: -150px;
  right: -150px;
  animation: float 8s ease-in-out infinite;
}

.decoration-2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: -100px;
  animation: float 6s ease-in-out infinite reverse;
}

.decoration-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  right: 10%;
  animation: float 10s ease-in-out infinite;
}

.floating-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.floating-element {
  position: absolute;
  width: 4px;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  animation: twinkle 3s ease-in-out infinite;
}

.element-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.element-2 {
  top: 60%;
  right: 20%;
  animation-delay: 1s;
}

.element-3 {
  bottom: 30%;
  left: 70%;
  animation-delay: 2s;
}

.header {
  position: relative;
  z-index: 10;
}

.main-section {
  position: relative;
  z-index: 2;
  padding: 60px 0 100px;
  min-height: calc(100vh - 91px);
}

.container {
  max-width: 1400px;
  padding: 0 24px;
  margin: 0 auto;
}

.hero-content {
  padding-right: 20px;
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.hero-content.loaded {
  opacity: 1;
  transform: translateY(0);
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 50px;
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.badge-icon {
  font-size: 1rem;
}

.gradient-title {
  font-size: 4rem;
  line-height: 1.1;
  margin-bottom: 24px;
  font-weight: 800;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.title-line {
  display: block;
}

.title-line.highlight {
  background: linear-gradient(45deg, #ffd89b 0%, #19547b 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  position: relative;
}

.subtitle {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.25rem;
  line-height: 1.7;
  margin-bottom: 32px;
  max-width: 580px;
  font-weight: 400;
}

.feature-tags {
  display: flex;
  gap: 12px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.tag {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 25px;
  color: white;
  font-size: 0.875rem;
  font-weight: 500;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.cta-section {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 32px;
  border-radius: 16px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  border: none;
  cursor: pointer;
}

.cta-button.primary {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
}

.cta-button.secondary {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.cta-button:hover {
  transform: translateY(-3px);
}

.cta-button.primary:hover {
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.5);
}

.cta-button.secondary:hover {
  background: rgba(255, 255, 255, 0.2);
}

.button-icon {
  transition: transform 0.3s ease;
}

.cta-button:hover .button-icon {
  transform: translateX(4px);
}

.card-group {
  display: grid;
  gap: 24px;
  opacity: 0;
  transform: translateX(30px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.2s;
}

.card-group.loaded {
  opacity: 1;
  transform: translateX(0);
}

.featured-card {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.8) 100%);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 32px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  overflow: hidden;
}

.featured-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.15);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.card-icon.featured {
  width: 60px;
  height: 60px;
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.card-badge {
  padding: 4px 12px;
  background: linear-gradient(45deg, #ffd89b 0%, #19547b 100%);
  color: white;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.featured-card h3 {
  color: #2c3e50;
  font-size: 1.75rem;
  margin-bottom: 16px;
  font-weight: 700;
}

.featured-card p {
  color: #5a6c7d;
  line-height: 1.6;
  font-size: 1rem;
  margin-bottom: 24px;
}

.card-stats {
  display: flex;
  gap: 32px;
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.875rem;
  color: #8b95a1;
}

.feature-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12);
}

.card-content {
  padding: 28px;
}

.card-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(45deg, #667eea20 0%, #764ba220 100%);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
  color: #667eea;
}

.feature-card h3 {
  color: #2c3e50;
  font-size: 1.5rem;
  margin-bottom: 12px;
  font-weight: 600;
}

.feature-card p {
  color: #5a6c7d;
  line-height: 1.6;
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.card-features {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.feature-item {
  padding: 6px 12px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

@keyframes twinkle {
  0%, 100% {
    opacity: 0.3;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

@media (max-width: 1024px) {
  .gradient-title {
    font-size: 3rem;
  }

  .hero-content {
    padding-right: 0;
    margin-bottom: 60px;
  }

  .container {
    padding: 0 20px;
  }
}

@media (max-width: 768px) {
  .gradient-title {
    font-size: 2.5rem;
  }

  .main-section {
    padding: 40px 0 60px;
  }

  .cta-section {
    flex-direction: column;
    align-items: stretch;
  }

  .cta-button {
    justify-content: center;
  }

  .feature-tags {
    justify-content: center;
  }

  .card-stats {
    justify-content: space-around;
  }
}

@media (max-width: 480px) {
  .gradient-title {
    font-size: 2rem;
  }

  .subtitle {
    font-size: 1.125rem;
  }

  .container {
    padding: 0 16px;
  }

  .featured-card,
  .card-content {
    padding: 24px;
  }
}
</style>
