<script lang="ts" setup>
import {nextTick, onMounted, ref, watch} from 'vue';
import Main from "@/components/mainPage/mainContainer.vue";
import GuidePage from "@/components/mainPage/guidePage.vue";
import axios from "axios";

const showGuide = ref(true);
const guidePageRef = ref(null);
const activeItem = ref<string | null | number>(null);
const mainPageRef = ref(null);
const items = ref([]);
const newItemLabel = ref('');
let itemIdCounter = 10000000;

const handleItemClick = async (id: string | number) => {
  showGuide.value = false;
  await nextTick();
  console.log(`选中项: ${id}`);
  const tempTip = items.value.find(item => item.id === id).temp
  if (tempTip) {
    console.log("临时页面")
    mainPageRef.value.resetPage();
    activeItem.value = id;
    mainPageRef.value.setTempName(items.value.find(item => item.id === activeItem.value).label)
    return
  }
  axios.get("/model/record/" + id, {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }, timeout: 3000
  }).then(res => {

    console.log("选中页面的数据", res.data.data.records)
    const data = res.data.data.records
    mainPageRef.value.inputData(data.map(item => {
          return {
            text: item.content,
            isUser: item.role == 1,
            loading: false,
            isPicture: false,
            time: new Date(item.create_at).toLocaleString('default', {
              year: 'numeric',
              month: '2-digit',
              day: '2-digit',
              hour: '2-digit',
              minute: '2-digit'
            }),
          }
        }), id
    )
    activeItem.value = id;
  }).catch(error => {
    console.log(error);
  })

};

watch(activeItem, (newVal) => {

});

const addItem = () => {
  if (!newItemLabel.value.trim()) {
    return;
  }
  const newItemId = ++itemIdCounter;
  items.value.push({
    id: newItemId,
    label: newItemLabel.value.trim(),
    temp: true
  });
  handleItemClick(newItemId);
  newItemLabel.value = '';
};

const removeItem = (targetId: string) => {
  items.value = items.value.filter(item => item.id !== targetId);
  if (activeItem.value === targetId) {
    activeItem.value = items.value.length ? items.value[0].id : null;
  }
};

const formatData = (data: any) => {
  return data.map(item => {
    return {
      id: item.session_id,
      label: item.name,
      temp: false
    }
  })
}

onMounted(() => {
  axios.get("/model/session", {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }, timeout: 3000
  }).then(res => {
    console.log("初始化数据", res.data.data)
    items.value = formatData(res.data.data)
    if (items.value.length) {
      guidePageRef.value.changeGuideText("View Details of the Record")
    } else guidePageRef.value.changeGuideText(" Add")
  }).catch(error => {
    console.log(error);
  })
})
;

const handleBackId = (id: string) => {
  items.value[items.value.length - 1].id = id
  activeItem.value = id
  items.value[items.value.length - 1].temp = false
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    addItem();
  }
};
</script>

<template>
  <div class="back-ground">
    <div class="content">
      <div class="sidebar-container">
        <div class="sidebar-header">
          <el-input v-model="newItemLabel" placeholder="Input record name" size="large"/>
          <el-button type="primary" size="large" @click="addItem" @keydown="handleKeyDown">Add</el-button>
        </div>
        <div class="sidebar-list">
          <div
              v-for="item in items"
              :key="item.id"
              :class="['sidebar-item', { active: activeItem === item.id }]"
              @click="handleItemClick(item.id)"
          >
            {{ item.label }}
          </div>
        </div>
      </div>
      <div class="main-container">
        <GuidePage v-if="showGuide" ref="guidePageRef"/>
        <Main ref="mainPageRef" @back-id="handleBackId" v-else/>
      </div>
    </div>
  </div>
</template>

<style scoped>
.back-ground {
  background: linear-gradient(200deg, #f3e7e9, #cddffa);
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar-container {
  width: 250px;
  height: 100%;
  background-color: #f8f9fa;
  border-right: 1px solid #ddd;
  padding: 10px;
  display: flex;
  flex-direction: column;
  z-index: 3;
}

.sidebar-header {
  display: flex;
  gap: 5px;
  margin-bottom: 10px;
}

.sidebar-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}

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

.sidebar-item.active {
  background: #409eff;
  color: white;
}

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
