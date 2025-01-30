<template>
  <div class="back-ground">
    <Header class="Header"></Header>

    <div class="content">
      <!-- 侧边栏 -->
      <div class="sidebar-container">
        <div class="sidebar-header">
          <el-input v-model="newItemLabel" placeholder="输入记录名称" size="large"/>
          <el-button type="primary" size="large" @click="addItem">添加</el-button>
        </div>

        <div class="sidebar-list">
          <div
              v-for="item in items"
              :key="item.id"
              :class="['sidebar-item', { active: activeItem === item.id }]"
              @click="handleItemClick(item.id)"
          >
            {{ item.label }}
            <el-icon @click.stop="removeItem(item.id)" class="delete-icon">
              <el-icon-delete/>
            </el-icon>
          </div>

        </div>
      </div>

      <!-- 主内容区域 -->
      <div class="main-container">
        <Main/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {ref, watch} from 'vue';
import Header from "@/components/Header.vue";
import Main from "@/components/mainPage/mainContainer.vue";
import {Delete as ElIconDelete} from '@element-plus/icons-vue';

// 选中的项
const activeItem = ref<string | null>(null);

// 列表项
const items = ref([
  {id: '1', label: '记录一'},
  {id: '2', label: '记录二'},
  {id: '3', label: '记录三'},
  {id: '4', label: '记录四'}
]);

// 新增项名称
const newItemLabel = ref('');
let itemIdCounter = items.value.length + 1;

/**
 * 处理点击侧边栏项
 * @param id 选中项的 ID
 */
const handleItemClick = (id: string) => {
  activeItem.value = id;

  // 你可以在这里添加额外的处理逻辑，例如：
  console.log(`选中项: ${id}`);

  // 触发数据加载或页面跳转（如果有路由的话）
  // router.push(`/page/${id}`); // 需要 Vue Router
};

// 监听 activeItem 变化，执行其他响应逻辑
watch(activeItem, (newVal) => {
  if (newVal) {
    console.log(`已切换到: ${newVal}`);
    // 可以在这里请求数据或更新组件内容
  }
});

// 添加新项
const addItem = () => {
  if (newItemLabel.value.trim()) {
    const newItemId = `${itemIdCounter++}`;
    items.value.push({
      id: newItemId,
      label: newItemLabel.value.trim()
    });
    handleItemClick(newItemId); // 自动选中新添加的项
    newItemLabel.value = '';
  }
};

// 删除项
const removeItem = (targetId: string) => {
  items.value = items.value.filter(item => item.id !== targetId);
  if (activeItem.value === targetId) {
    activeItem.value = items.value.length ? items.value[0].id : null;
  }
};
</script>


<style scoped>
/* 整体布局 */
.back-ground {
  background: linear-gradient(200deg, #f3e7e9, #cddffa);
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 顶部 Header */
.Header {
  height: 60px;
  width: 100%;
}

/* 主体部分 */
.content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 侧边栏 */
.sidebar-container {
  width: 250px;
  height: 100%;
  background-color: #f8f9fa;
  border-right: 1px solid #ddd;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

/* 侧边栏头部 */
.sidebar-header {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
}

/* 列表项 */
.sidebar-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}

/* 每一项 */
.sidebar-item {
  background: #ffffff;
  padding: 10px 15px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all 0.3s ease;
  box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
  margin-right: 5px;
}

/* 选中项 */
.sidebar-item.active {
  background: #409eff;
  color: white;
}

/* 删除按钮 */
.delete-icon {
  font-size: 18px;
  cursor: pointer;
  transition: 0.2s;
}

.delete-icon:hover {
  color: red;
}
.main-container {
  flex: 1;
  padding: 0;
}
</style>
