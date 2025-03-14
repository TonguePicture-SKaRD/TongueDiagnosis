<template>
  <!-- <h2>这是login表单</h2> -->
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <el-form ref="Email_Password_login" style="max-width: 210px" :model="user" status-icon :rules="rules"
               label-width="auto" class="Email_Password_form" v-loading="loading" element-loading-background="#ffffff" size="large">

        <el-form-item label="" prop="Email">
          <el-input v-model="user.Email" placeholder="请输入邮箱" id="l_email" :prefix-icon="Avatar" size="large"/>
        </el-form-item>

        <el-form-item label="" prop="Password">
          <el-input v-model="user.Password" placeholder="请输入密码" id="l_password" type="password" show-password
                    :prefix-icon="Key" size="large"/>
          <br>
          <!-- <div v-show="not_register">尚未注册？<router-link to='/register'>注册</router-link></div> -->
        </el-form-item>

        <el-form-item>
<!--          <el-button class="reset_l" @click="reset(Email_Password_login)" round>重置</el-button>-->
<!--          <br>-->
          <el-button class="login_b" type="primary" @click="login(Email_Password_login)" size="large">登录</el-button>


        </el-form-item>

      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import {reactive, ref, h} from 'vue'
import {ElMessage, type FormInstance, type FormRules} from 'element-plus'
import router from '@/router';


const Email_Password_login = ref<FormInstance>() //表单ref属性
let loading = ref(false)
let token = ''
let not_register = ref<boolean>(false)
let timeout = 50000//超时


const validatePassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    const pattern = /^[a-zA-Z0-9]+$/;
    if (value.length < 6) {
      callback(new Error('密码过短'))
    } else {
      if (value.length > 20) {
        callback(new Error('密码过长'))
      } else {
        callback()
      }
    }
  }
}


// if (user.Password !== '') {
//             if (!Email_Password_login.value) return
//             Email_Password_login.value.validateField('checkPassword', () => null)
//         }


const validateEmail = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入邮箱地址'));
  } else {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      callback(new Error('请输入有效的邮箱地址'));
    } else {
      callback();
    }
  }
};

let user = reactive({
  Email: '',
  Password: '',
})

//创建规则
const rules = reactive<FormRules<typeof user>>({
  Email: [{validator: validateEmail, trigger: ['blur']}],
  Password: [{validator: validatePassword, trigger: ['blur']}],
})


const login = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      // console.log('submit!')
      loading.value = true
      set_Login_put()
    } else {
      // console.log('error submit!')
      fail_message("请按要求填写")
      return false
    }
  })
}

const reset = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}


import axios from 'axios';


const generate_form = () => {
  let dataform = new FormData()
  dataform.append('email', user.Email)
  dataform.append('password', user.Password)
  return dataform
}


const set_Login_put = () => {
  axios({
    method: 'put',
    data: generate_form(),
    url: '/user/login',
    timeout: 5000
  })
      .then(response => {
        loading.value = false
        analyze_response(response.data)
        // console.log("成功")

      })
      .catch(error => {
        loading.value = false
        if (error === 'ECONNABORTED') {
          loading.value = false
          fail_message('请求超时')
        } else {
          loading.value = false
          fail_message("出错请重试")
          console.error(error);
        }
      });
}


const success_message = (message: string) => {
  ElMessage({
    showClose: true,
    message: message,
    type: 'success',
    duration: 1500
  })
}

const fail_message = (message: string) => {
  ElMessage({
    showClose: true,
    message: message,
    type: 'error',
    duration: 3000
  })
}

const analyze_response = (data: any) => {
  if (data.code === 0) {
    success_message("登录成功")
    token = data.data.token
    deliver_token(token)
    jump_home(1)
    // console.log(token)
  } else {
    if (data.code === 101) {
      fail_message("用户不存在")
      not_register.value = true
    } else {
      if (data.code === 102) {
        fail_message("密码错误")
      } else {
        fail_message("出错请重试")
      }
    }
  }
}

const deliver_token = (t: string) => {
  // console.log("t:", t) //
  localStorage.setItem('token', t);
}

function jump_home(seconds: any) {
  setTimeout(function () {
    router.push('./home')
  }, seconds * 1000);
}


//原代码
import {watchEffect} from 'vue'
import {Avatar, Key, Checked} from '@element-plus/icons-vue'
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
}


.login-card {
  padding: 5px;
  border-radius: 12px;
  max-height: 20%;
}

.login_b {
  width: 100%;
  margin-top: 20px;
  /* background-color: #f6f6f6;
  outline: none;
  border-radius: 8px;
  padding: 13px;
  color: #0b51de;
  letter-spacing: 2px;
  border: none;
  cursor: pointer;  */
}

.reset_l {
  justify-content: flex-end;
}
</style>