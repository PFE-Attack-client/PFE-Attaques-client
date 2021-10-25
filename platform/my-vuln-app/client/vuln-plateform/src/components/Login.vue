<script setup>
import { reactive, ref } from 'vue'
import Home from './Home.vue'
import App from '../App.vue'

const log = reactive({
    username: '',
    password: '',
    access: false,
})

const props = defineProps({
  is_log: {
    type: Boolean,
    required: true,
  },
  is_click: {
      type: Boolean,
      required: true,
  }
})

const login = () => {
    if(log.username === "test" && log.password === 'test'){
        log.access = true
        localStorage.setItem('token', 'got it')
    }

}

</script>

<template>
<div>
    <div class="contain2" v-if="log.access === false">
            <div>
                <el-header class="header">
                    <br/>
                    <div class="welcome">Please connect to the blog !</div>
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
                                <!-- <div v-if="log.msg==='ok'">
                                <el-result
                                    icon="success"
                                    title="Connection successful"
                                    class="result"
                                />
                                </div> -->
                                <!-- <div v-if="log.msg==='error'">
                                <el-result
                                    icon="error"
                                    title="Connection denied"
                                    class="result2"
                                    sub-title="Please try again"
                                />
                                <el-button @click="retry">Back</el-button>
                                </div> -->
                                <!-- <div v-if="log.msg===''"> -->
                                <div>
                                <h1>Login</h1>
                                    <div>
                                        <el-form
                                        ref="login"
                                        label-position="top"
                                        label-width="100px"
                                        :model="log"
                                        class='form'>
                                            <el-form-item label="Username">
                                                <el-input v-model="log.username" placeholder="Enter your username"/>
                                            </el-form-item>
                                            <el-form-item label="Password">
                                                <el-input v-model="log.password" placeholder="Please input password" show-password />
                                            </el-form-item>
                                            <el-form-item>
                                                <el-button type="info" @click="login">Submit</el-button>
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
    <div v-if="log.access === true">
        <App/>
    </div>
</div>    
</template>

<style>
.contain2{
    width: 1000px;
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
  height: 450px;
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