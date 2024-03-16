<template>
    <div class="back-ground">
        <div class="center-container">
            <div class="container">
                <div class="form-box" :style="refstyle">

                    <div class="register-box" v-show=show_change>
                        <h1>register</h1>
                        <Registerblock />

                    </div>
                    <!-- 登录 -->
                    <div class="login-box" v-show=!show_change>
                        <h1>login</h1>

                        <Loginblock />
                    </div>
                </div>


                <!-- 左右显示内容 -->
                <div class="con-box left">
                    <h2>欢迎来到<span>舌诊宝</span></h2>
                    <p> </p>
                    <img src="@\assets\Chat_Tongue.webp" alt="">
                    <p>已有账号</p>
                    <button id="login" @click="change_style">去登录</button>
                </div>

                <div class="con-box right">
                    <h2>欢迎来到<span>舌诊宝</span></h2>
                    <p> </p>
                    <img src="@\assets\Chat_Tongue.webp" alt="">
                    <p>没有账号?</p>
                    <button id="register" @click="change_style">去注册</button>
                </div>
            </div>
        </div>
    </div>

</template>

<script setup lang="ts">
import Registerblock from '@/components/Registerblock.vue';
import Loginblock from './Loginblock.vue';
import { ref,inject,watch } from 'vue'


let slide_tip = false
let refstyle = ref({
    transform: 'translateX(0%)'
})
let show_change = false
let receivedMessage = inject('message', ref(''));

watch(receivedMessage.value, (newValue, oldValue) => {
  console.log(`Counter 改变了：${oldValue} -> ${newValue}`);
});


const change_style = () => {
    show_change = !show_change
    slide_tip = !slide_tip
    refstyle.value.transform = slide_tip ? 'translateX(80%)' : 'translateX(0%)'
}

</script>

<style scoped>
.center-container {
    display: flex;
    justify-content: center;
    /* 水平居中 */
    align-items: center;
    /* 垂直居中 */
    height: 100vh;

}

body {
    /* 100%窗口高度 */
    height: 100vh;
    /* 弹性布局 水平+垂直居中 */
    display: flex;
    justify-content: center;
    align-items: center;
    /* 渐变背景 */
    background: linear-gradient(200deg, #f3e7e9, #e3eeff);
}

.container {
    background-color: #fff;
    width: 650px;
    height: 415px;
    border-radius: 5px;
    /* 阴影 */
    box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.1);
    /* 相对定位 */
    display: flex;
    justify-content: center;
    align-items: center;
    position: relative;
}

.form-box {
    /* 绝对定位 */
    position: absolute;
    top: -10%;
    left: 5%;
    background-color: #d3b7d8;
    width: 320px;
    height: 500px;
    border-radius: 5px;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 2;
    /* 动画过渡 加速后减速 */
    transition: 0.5s ease-in-out;
}


.register-box,
.login-box {
    /* 弹性布局 垂直排列 */
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}


h1 {
    text-align: center;
    margin-bottom: 25px;
    /* 大写 */
    text-transform: uppercase;
    color: #fff;
    /* 字间距 */
    letter-spacing: 5px;
}

.con-box {
    width: 50%;
    /* 弹性布局 垂直排列 居中 */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    /* 绝对定位 居中 */
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
}

.con-box.left {
    left: -2%;
}

.con-box.right {
    right: -2%;
}

.con-box h2 {
    color: #8e9aaf;
    font-size: 25px;
    font-weight: bold;
    letter-spacing: 3px;
    text-align: center;
    margin-bottom: 4px;
}

.con-box p {
    font-size: 12px;
    letter-spacing: 2px;
    color: #8e9aaf;
    text-align: center;
}

.con-box span {
    color: #d3b7d8;
}

.con-box img {
    width: 150px;
    height: 150px;
    opacity: 0.9;
    margin: 40px 0;
}

.con-box button {
    margin-top: 3%;
    background-color: #fff;
    color: #a262ad;
    border: 1px solid #d3b7d8;
    padding: 6px 10px;
    border-radius: 5px;
    letter-spacing: 1px;
    outline: none;
    cursor: pointer;
}

.con-box button:hover {
    background-color: #d3b7d8;
    color: #fff;
}

.background {
  background-color: #405ba0; /* 设置背景颜色 */
  width: 100%; /* 宽度占满整个屏幕 */
  height: 100vh; /* 高度占满整个屏幕 */
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
}
</style>