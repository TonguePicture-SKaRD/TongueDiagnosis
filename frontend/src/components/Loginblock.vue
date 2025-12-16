<template>
  <div class="login-container">
    <el-card class="login-card" shadow="hover">
      <el-form ref="Email_Password_login" style="max-width: 210px" :model="user" status-icon :rules="rules"
               label-width="auto" class="Email_Password_form" v-loading="loading" element-loading-background="#ffffff" size="large">
        <el-form-item label="" prop="Email">
          <el-input v-model="user.Email" placeholder="Your email" id="l_email" size="large"/>
        </el-form-item>
        <el-form-item label="" prop="Password">
          <el-input v-model="user.Password" placeholder="Your password" id="l_password" type="password" show-password size="large"/>
          <br>
        </el-form-item>
        <el-form-item>
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
import axios from 'axios';

const Email_Password_login = ref<FormInstance>()
let loading = ref(false)
let token = ''
let not_register = ref<boolean>(false)
let timeout = 50000

const validatePassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please enter a password'))
  } else {
    const pattern = /^[a-zA-Z0-9]+$/;
    if (value.length < 6) {
      callback(new Error('The password is too short'))
    } else {
      if (value.length > 20) {
        callback(new Error('The password is too long'))
      } else {
        callback()
      }
    }
  }
}

const validateEmail = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please enter your email address'));
  } else {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      callback(new Error('Please enter a valid email address'));
    } else {
      callback();
    }
  }
};

let user = reactive({
  Email: '',
  Password: '',
})

const rules = reactive<FormRules<typeof user>>({
  Email: [{validator: validateEmail, trigger: ['blur']}],
  Password: [{validator: validatePassword, trigger: ['blur']}],
})


const login = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      loading.value = true
      set_Login_put()
    } else {
      fail_message("Please fill in as required.")
      return false
    }
  })
}

const reset = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.resetFields()
}

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
    timeout: 20000
  })
      .then(response => {
        loading.value = false
        analyze_response(response.data)

      })
      .catch(error => {
        loading.value = false
        if (error === 'ECONNABORTED') {
          loading.value = false
          fail_message('request timeout')
        } else {
          loading.value = false
          fail_message("Encounter an error, please try again")
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
    success_message("login success")
    token = data.data.token
    deliver_token(token)
    jump_home(1)
  } else {
    if (data.code === 101) {
      fail_message("The user does not exist")
      not_register.value = true
    } else {
      if (data.code === 102) {
        fail_message("wrong password")
      } else {
        fail_message("Encounter an error, please try again")
      }
    }
  }
}

const deliver_token = (t: string) => {
  localStorage.setItem('token', t);
}

function jump_home(seconds: any) {
  setTimeout(function () {
    router.push('./home')
  }, seconds * 1000);
}

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
}

.reset_l {
  justify-content: flex-end;
}
</style>