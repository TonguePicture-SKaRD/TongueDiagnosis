import {defineStore} from 'pinia';
import settings from '../config/config.js';

export const useStateStore = defineStore('state', {
    state: () => ({
        isOpenValue: 0,
        userImagePath: "./static/userDefault.jpg",
        aiImagePath: "./static/aiDefault.jpg",
        audioType: 'D',
        baseUrl: settings.apiBaseUrl + "/model/session",
        chatHistory: [],
        infoHistory: [],
        isPlayed: false,
        gender: "male",
        personalPrompt: "",
        isShow: true,
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
