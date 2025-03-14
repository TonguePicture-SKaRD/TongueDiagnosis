// src/stores/stateStore.js
import { defineStore } from 'pinia';

export const useStateStore = defineStore('state', {
    state: () => ({
        isOpenValue: 0, // 状态栏是否收缩
        userImagePath: "./static/userDefault.jpg", // 存储用户图片路径
        aiImagePath: "./static/aiDefault.jpg", // 存储ai图片路径
        audioType: 'D', // 音频类型
        baseUrl: "http://localhost:5000/api/model/session", // IPv4地址
        chatHistory: [],
        infoHistory: [],
        isPlayed: false, // 检测是否已经播放过介绍页面
        gender: "male", // 性别
        personalPrompt: "", // 个人prompt
        isShow: true, // 演示模式
    }),
    actions: {
        setisOpenValue(newValue) {
            this.isOpenValue = newValue;
        },
        setuserImagePath(newValue) {
            this.userImagePath = newValue;
        },
        setaiImagePath(newValue) {
            this.aiImagePath = newValue;
        },
        setaudioType(newValue) {
            this.audioType = newValue;
        },
        setbaseUrl(newValue) {
            this.baseUrl = newValue;
        },
        setisPlayed(newValue) {
            this.isPlayed = newValue;
        },
        setGender(newValue) {
            this.gender = newValue;
        },
        setPersonalPrompt(newValue) {
            this.personalPrompt = newValue;
        },
        setIsShow(newValue) {
            this.isShow = newValue;
        },
        setChatHistory(newValue) {
            this.chatHistory = newValue;
        },
        setInfoHistory(newValue) {
            this.infoHistory = newValue;
        },
    },
});
