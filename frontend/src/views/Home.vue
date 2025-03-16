<script setup>
import Header from "@/components/Header.vue";
</script>

<template>
  <div class="back-ground">
    <Header class="header"></Header>
    <section class="main-section">
      <div class="container">
        <el-row :gutter="30">
          <!-- 主内容区 -->
          <el-col :xs="24" :md="14">
            <div class="hero-content">
              <h1 class="gradient-title">
                舌诊宝：中医AI智能舌诊系统
              </h1>
              <p class="subtitle">
                基于深度学习的舌象识别应用，推动中医与人工智能的现代化结合
              </p>
              <router-link to="/check" class="cta-button">
                <span>立即检测</span>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                  <path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="currentColor" stroke-width="2"/>
                </svg>
              </router-link>
            </div>
          </el-col>

          <!-- 功能卡片区 -->
          <el-col :xs="24" :md="10">
            <div class="card-group">
              <el-card class="feature-card">
                <div class="card-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                    <path d="M4 17L12 9L20 17" stroke="#2F80ED" stroke-width="2"/>
                    <path d="M12 4V20" stroke="#2F80ED" stroke-width="2"/>
                  </svg>
                </div>
                <h3>舌象智能诊断</h3>
                <p>上传舌像获取AI诊断报告，结合中医理论提供个性化健康建议</p>
              </el-card>

              <el-card class="feature-card">
                <div class="card-icon">
                  <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                    <path
                        d="M3 10H21M7 3V5M17 3V5M6.2 21H17.8C18.9201 21 19.4802 21 19.908 20.782C20.2843 20.5903 20.5903 20.2843 20.782 19.908C21 19.4802 21 18.9201 21 17.8V8.2C21 7.07989 21 6.51984 20.782 6.09202C20.5903 5.71569 20.2843 5.40973 19.908 5.21799C19.4802 5 18.9201 5 17.8 5H6.2C5.0799 5 4.51984 5 4.09202 5.21799C3.71569 5.40973 3.40973 5.71569 3.21799 6.09202C3 6.51984 3 7.07989 3 8.2V17.8C3 18.9201 3 19.4802 3.21799 19.908C3.40973 20.2843 3.71569 20.5903 4.09202 20.782C4.51984 21 5.07989 21 6.2 21Z"
                        stroke="#27AE60" stroke-width="2"/>
                  </svg>
                </div>
                <h3>健康记录管理</h3>
                <p>按记录查看历史诊断报告，随时追踪健康状况变化</p>
              </el-card>
            </div>
          </el-col>
        </el-row>
      </div>
    </section>
  </div>
</template>

<style scoped>
.header {
  position: relative;

}

.main-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  min-height: calc(100vh - 91px);
  padding: 80px 0;
}

.container {
  max-width: 1200px;
  padding: 0 20px;
  margin: 5vh auto 0;
}

.hero-content {
  padding-right: 40px;
}

.gradient-title {
  background: linear-gradient(45deg, #2F80ED, #27AE60);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-size: 3.5rem;
  line-height: 1.2;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.subtitle {
  color: #4F4F4F;
  font-size: 1.25rem;
  line-height: 1.6;
  margin-bottom: 2.5rem;
  max-width: 500px;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  padding: 1rem 2rem;
  background: #2F80ED;
  color: white;
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(47, 128, 237, 0.2);
}

.cta-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(47, 128, 237, 0.3);
  background: #256fcc;
}

.cta-button svg {
  margin-left: 12px;
  transition: transform 0.3s ease;
}

.cta-button:hover svg {
  transform: translateX(4px);
}

.card-group {
  display: grid;
  gap: 24px;
}

.feature-card {
  border: none;
  border-radius: 16px;
  padding: 32px;
  transition: transform 0.3s ease;
  background: white;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.06);
}

.feature-card:hover {
  transform: translateY(-5px);
}

.card-icon {
  margin-bottom: 20px;
}

.feature-card h3 {
  color: #2D3436;
  font-size: 1.5rem;
  margin-bottom: 12px;
}

.feature-card p {
  color: #636E72;
  line-height: 1.6;
  font-size: 1rem;
}

@media (max-width: 768px) {
  .gradient-title {
    font-size: 2.5rem;
  }

  .hero-content {
    padding-right: 0;
    margin-bottom: 40px;
  }
}

.back-ground {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  overflow: hidden;
  height: 100vh;

}
</style>