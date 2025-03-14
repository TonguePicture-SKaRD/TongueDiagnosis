<template>
  <!-- <h2>这是表单</h2> -->
  <div class="register-container">
    <el-card class="register-card" shadow="hover">
      <el-form ref="Email_Password_register" style="max-width: 210px;margin-top: 10px" :model="user" status-icon :rules="rules"
               label-width="auto" class="Email_Password_form" v-loading="loading" element-loading-background="#ffffff"
               size="large">

        <el-form-item label="" prop="Email">
          <el-input v-model="user.Email" placeholder="请输入邮箱" id="r_email" :prefix-icon="Avatar" size="large"/>
        </el-form-item>

        <el-form-item label="" prop="Password">
          <el-input v-model="user.Password" placeholder="请设置密码" id="r_password" type="password"
                    show-password :prefix-icon="Key" size="large"/>
        </el-form-item>

        <el-form-item label="" prop="checkPassword">
          <el-input v-model="user.checkPassword" placeholder="请确认密码" id="r_cpassword" type="password" show-password
                    :prefix-icon="Checked" size="large"/>
          <br>
          <!-- <router-link to='/login' v-show="finish_register">跳转至登录页面</router-link> -->
        </el-form-item>

        <el-form-item>
          <!--          <el-button class="reset_r" @click="reset(Email_Password_register)" size="small" round>重置</el-button>-->
          <br>
          <el-button class="register_b" type="primary" @click="register(Email_Password_register)" size="large">注册
          </el-button>


        </el-form-item>

      </el-form>
    </el-card>

  </div>
</template>

<script lang="ts" setup>
import {reactive, ref, provide} from 'vue'
import {ElMessage, type FormInstance, type FormRules} from 'element-plus'
const emit = defineEmits(["change"])

const Email_Password_register = ref<FormInstance>() //表单ref属性
let loading = ref(false)
const timeout = 5000//超时报错
let finish_register = ref<boolean>(false)


const validatePassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请设置密码'))
  } else {
    const pattern = /^[a-zA-Z0-9]+$/;
    if (value.length < 6) {
      callback(new Error('密码过短'))
    } else {
      if (value.length > 20) {
        callback(new Error('密码过长'))
      } else {
        if (pattern.test(value)) {
          callback()
        } else {
          callback(new Error('请不要使用特殊字符'))
        }
      }
    }
  }
}


// if (user.Password !== '') {
//             if (!Email_Password_register.value) return
//             Email_Password_register.value.validateField('checkPassword', () => null)
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

//检查密码一致
const validatecheckPassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== user.Password) {
    callback(new Error("前后密码不一样"))
  } else {
    callback()
  }
}

const user = reactive({
  Email: '',
  Password: '',
  checkPassword: '',
})

//创建规则
const rules = reactive<FormRules<typeof user>>({
  Email: [{validator: validateEmail, trigger: ['blur']}],
  Password: [{validator: validatePassword, trigger: ['blur']}],
  checkPassword: [{validator: validatecheckPassword, trigger: 'change'}],
})


const register = (formEl: FormInstance | undefined) => {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      // console.log('submit!')

      set_Register_post()
      loading.value = true
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

          fail_message('请求超时')
        } else {

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
    success_message("注册成功")

    finish_register.value = true

    jump_login(1) //等待1s后跳转
  } else {
    if (data.code === 101) {
      fail_message("此账号已被注册")
    } else {
      fail_message("注册失败，请重试")
    }
  }
}

//等待
function jump_login(seconds) {
  setTimeout(function () {
    emit('change');
  }, seconds * 1000);
}




//原代码
import {watchEffect} from 'vue'
import {Avatar, Key, Checked} from '@element-plus/icons-vue'
import router from '@/router';
</script>

<style scoped>
.register_b {
  width: 100%;
  margin-top: 10px;
  /* background-color: #f6f6f6;
  outline: none;
  border-radius: 8px;
  padding: 13px;
  color: #0b51de;
  letter-spacing: 2px;
  border: none;
  cursor: pointer;  */
}

/* .register_b:hover {
    background-color: #a262ad;
    color: #f6f6f6;
    transition: background-color 0.5s ease;
} */


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