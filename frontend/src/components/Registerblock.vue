<template>
  <div class="register-container">
    <el-card class="register-card" shadow="hover">
      <el-form ref="Email_Password_register" style="max-width: 210px;margin-top: 10px" :model="user" status-icon :rules="rules"
               label-width="auto" class="Email_Password_form" v-loading="loading" element-loading-background="#ffffff"
               size="large">
        <el-form-item label="" prop="Email">
          <el-input v-model="user.Email" placeholder="Your email" id="r_email" size="large"/>
        </el-form-item>
        <el-form-item label="" prop="Password">
          <el-input v-model="user.Password" placeholder="Set a password" id="r_password" type="password"
                    show-password size="large"/>
        </el-form-item>
        <el-form-item label="" prop="checkPassword">
          <el-input v-model="user.checkPassword" placeholder="Confirm your password" id="r_cpassword" type="password" show-password
                    size="large"/>
          <br>
        </el-form-item>
        <el-form-item>
          <br>
          <el-button class="register_b" type="primary" @click="register(Email_Password_register)" size="large">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import {reactive, ref, provide} from 'vue'
import {ElMessage, type FormInstance, type FormRules} from 'element-plus'
const emit = defineEmits(["change"])

const Email_Password_register = ref<FormInstance>()
let loading = ref(false)
const timeout = 5000
let finish_register = ref<boolean>(false)

const validatePassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please set a password'))
  } else {
    const pattern = /^[a-zA-Z0-9]+$/;
    if (value.length < 6) {
      callback(new Error('The password is too short'))
    } else {
      if (value.length > 20) {
        callback(new Error('The password is too long'))
      } else {
        if (pattern.test(value)) {
          callback()
        } else {
          callback(new Error('Please do not use special characters'))
        }
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

const validatecheckPassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('Please re-enter your password.'))
  } else if (value !== user.Password) {
    callback(new Error("Passwords do not match"))
  } else {
    callback()
  }
}

const user = reactive({
  Email: '',
  Password: '',
  checkPassword: '',
})

const rules = reactive<FormRules<typeof user>>({
  Email: [{validator: validateEmail, trigger: ['blur']}],
  Password: [{validator: validatePassword, trigger: ['blur']}],
  checkPassword: [{validator: validatecheckPassword, trigger: 'change'}],
})

const register = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {

      set_Register_post()
      loading.value = true
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

import axios from 'axios';

const set_Register_post = () => {
  axios.post('/user/register', {
    email: user.Email,
    password: user.Password
  }, {timeout: timeout})
      .then(response => {
        analyze_response(response.data)
        loading.value = false
      })
      .catch(error => {
        loading.value = false
        if (error === 'ECONNABORTED') {

          fail_message('request timeout')
        } else {

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
    success_message("registered success")

    finish_register.value = true

    jump_login(1)
  } else {
    if (data.code === 101) {
      fail_message("This account has been registered")
    } else {
      fail_message("Registration failed, please try again.")
    }
  }
}

function jump_login(seconds) {
  setTimeout(function () {
    emit('change');
  }, seconds * 1000);
}
</script>

<style scoped>
.register_b {
  width: 100%;
  margin-top: 10px;
}

.reset_r {
  justify-content: flex-end;
}

.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-card {
  padding: 5px;
  border-radius: 12px;
  max-height: 30%;
}
</style>