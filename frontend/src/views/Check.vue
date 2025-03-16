<template>
  <div class="back-ground">
    <Header class="Header"></Header>

    <div class="content">
      <!-- 侧边栏 -->
      <div class="sidebar-container">
        <div class="sidebar-header">
          <el-input v-model="newItemLabel" placeholder="输入记录名称" size="large"/>
          <el-button type="primary" size="large" @click="addItem" @keydown="handleKeyDown">添加</el-button>
        </div>

        <div class="sidebar-list">
          <div
              v-for="item in items"
              :key="item.id"
              :class="['sidebar-item', { active: activeItem === item.id }]"
              @click="handleItemClick(item.id)"
          >
            {{ item.label }}
            <!--            <el-icon @click.stop="removeItem(item.id)" class="delete-icon">-->
            <!--              <el-icon-delete/>-->
            <!--            </el-icon>-->
          </div>

        </div>
      </div>

      <!-- 主内容区域 -->
      <div class="main-container">
        <GuidePage v-if="showGuide" ref="guidePageRef"/>
        <Main ref="mainPageRef" @back-id="handleBackId" v-else/>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {nextTick, onMounted, ref, watch} from 'vue';
import Header from "@/components/Header.vue";
import Main from "@/components/mainPage/mainContainer.vue";
import GuidePage from "@/components/mainPage/guidePage.vue";
import {Delete as ElIconDelete} from '@element-plus/icons-vue';
import axios from "axios";

//是否显示引导页
const showGuide = ref(true);
//引导页
const guidePageRef = ref(null);

// 选中的项
const activeItem = ref<string | null | number>(null);
//页面ref
const mainPageRef = ref(null);


// 列表项
const items = ref([]);

// 新增项名称
const newItemLabel = ref('');
let itemIdCounter = 10000000;

/**
 * 处理点击侧边栏项
 * @param id 选中项的 ID
 */
const handleItemClick = async (id: string | number) => {

  showGuide.value = false;
  await nextTick();
  console.log(`选中项: ${id}`);
  const tempTip = items.value.find(item => item.id === id).temp
  if (tempTip) {
    console.log("临时页面")
    mainPageRef.value.resetPage();
    activeItem.value = id;
    //传输名字
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
    //注入数据
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

  // 触发数据加载或页面跳转（如果有路由的话）
  // router.push(`/page/${id}`); // 需要 Vue Router
};

// 监听 activeItem 变化，执行其他响应逻辑
watch(activeItem, (newVal) => {
  //临时的就及时更新在哪
  // console.log("activeItem", activeItem)
  // if (items.value.find(item => item.id === activeItem.value).temp) {
  //   mainPageRef.value.setTempName(items.value.find(item => item.id === activeItem.value).label)
  // }
});

// 添加新项
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
  handleItemClick(newItemId); // 自动选中新添加的项
  newItemLabel.value = '';
  // mainPageRef.value.resetPage();


};

// 删除项
const removeItem = (targetId: string) => {
  items.value = items.value.filter(item => item.id !== targetId);
  if (activeItem.value === targetId) {
    activeItem.value = items.value.length ? items.value[0].id : null;
  }
};


//格式化返回的数据
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
  // 获取所有session
  axios.get("/model/session", {
    headers: {
      'Authorization': 'Bearer ' + localStorage.getItem('token')
    }, timeout: 3000
  }).then(res => {
    console.log("初始化数据", res.data.data)
    items.value = formatData(res.data.data)
    if (items.value.length) {
      guidePageRef.value.changeGuideText("记录查看详情")
    } else guidePageRef.value.changeGuideText("添加记录")
  }).catch(error => {
    console.log(error);
  })
})
;

//得到了返回的id
const handleBackId = (id: string) => {
  // console.log("返回的id", id)
  items.value[items.value.length - 1].id = id
  activeItem.value = id
  items.value[items.value.length - 1].temp = false
}

// 按下 Enter 键触发添加记录
const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    addItem();
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
  z-index: 3;
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
