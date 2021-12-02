<script setup>
import { reactive, ref } from 'vue'
import Home from './Home.vue'
import App from '../App.vue'
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus'

const ip_serv = '10.0.0.3'

const reg = reactive({
    username: '',
    email: '',
    password: '',
    confirm_password: '',
    access: false,
})

const props = defineProps({
  want_register: {
      type: Boolean,
      required: true,
  }
})

const register = () => {
    if(reg.password !== reg.confirm_password){
        ElMessageBox(
        {
            message: 'Wrong password match. Try again'})
    }
    if(reg.confirm_password === ''){
        ElMessageBox(
        {
            message: 'Confirm your password'})
    }
    const data = {
        "username": reg.username,
        "email": reg.email,
        "password": reg.password
    }
    axios.post(`http://${ip_serv}/user/signup`, data)
    .then(res =>{
        if(res.data.message === "Successfully registered."){
            ElMessageBox(
        {
            message: 'Successfully registered !!'})
        reg.access = true
        }
    })

}

</script>

<template>
<div>
    <div class="contain3" v-if="reg.access === false">
            <div>
                <el-header class="header">
                    <br/>
                    <div class="welcome">Please register to the blog !</div>
                </el-header>
                <el-image
                    style="width: 1000px; height: 500px; margin-bottom: 1em;"
                    src="/src/assets/paysage.png"
                    fit="contain">
                
                </el-image>
                <el-container class="container">
                    <el-main class="main2">
                        <div>
                            <el-card class="box-card">
                                <div>
                                <h1>Register</h1>
                                    <div>
                                        <el-form
                                        ref="register"
                                        label-position="top"
                                        label-width="100px"
                                        :model="reg"
                                        class='form'>
                                            <el-form-item label="Username">
                                                <el-input v-model="reg.username" placeholder="Enter your username"/>
                                            </el-form-item>
                                            <el-form-item label="Email">
                                                <el-input v-model="reg.email" placeholder="Enter your email"/>
                                            </el-form-item>
                                            <el-form-item label="Password">
                                                <el-input v-model="reg.password" placeholder="Please input password" show-password />
                                            </el-form-item>
                                            <el-form-item label="Confirm password">
                                                <el-input v-model="reg.confirm_password" placeholder="Please confirm password" show-password />
                                            </el-form-item>
                                            <el-form-item>
                                                <el-button type="info" @click="register">Submit</el-button>
                                            </el-form-item>
                                        </el-form>
                                    </div>
                                </div>
                            </el-card>
                        </div>
                    </el-main>

                </el-container>
            </div>
        </div>
    <div v-if="reg.access === true">
        <App/>
    </div>
</div>    
</template>

<style>
.contain3{
    width: 1000px;
    height: 900px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 4.5em;
}

.welcome2{
    position: absolute;
    top: 8%;
    left: 34%;
    text-align: center;

}

.box-card {
  position: absolute;
  top: 21%;
  left: 38%;
  width: 450px;
  height: 600px;
  background-color: #dce8e0;
}

.form{
    margin-top: 10px;
}

.main2{
    width: 790px;
    text-align: center;
    position: inherit;
}

.result{
  margin-top: 10%;
}

.refresh{
  margin-top: -3.5%;
}

</style>