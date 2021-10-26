<script setup>
import { onMounted, watch } from '@vue/runtime-core'
import { reactive } from '@vue/reactivity'
import Home from './components/Home.vue'
import Login from './components/Login.vue'

// const props = defineProps({
//   success: {
//     type: Boolean,
//     required: true,
//   },
// })

const v = reactive({
    is_click: false,
    is_log: false,
})

const isLogged = () =>{   //knowing if the user has logged in or not Login.vue
    if (localStorage.getItem('token') === null || localStorage.getItem('token') === 'null'){
        v.is_log = false
    }
    else{
        v.is_log = true
    }
}

const log = () =>{
    if (v.is_log === false){
        v.is_click = true
        v.is_log = true
    }
    else{
        v.is_log = false
        localStorage.setItem('token', 'null')
    }
}

onMounted(() => {
  isLogged()
})

</script>

<template>
<div>
    <div v-if="v.is_click === true">
        <Login 
            :is_log="v.is_log"
            :is_click="v.is_click"
        />
    </div>
    <div v-if="v.is_click === false">
    <div class="contain">
            <div>
                <div class="connect">
                    <el-col span="10">
                        <div v-if="v.is_log === false">
                            <el-button type="success" round @click="log">
                                Log in
                            </el-button>
                        </div>
                        <div v-if="v.is_log === true">
                            <el-col span="3">
                                <el-button type="danger" round @click="log">Log out</el-button>
                            </el-col>
                            <el-col span="2">
                                <div class="user">Welcome {user} !</div>
                            </el-col>
                        </div>
                    </el-col>
                        
                </div>
                <div class="nav">
                    <router-link to="/home">Home</router-link> /
                    <router-link to="/articles">Articles</router-link> /
                    <router-link to="/about">About</router-link> /
                    <router-link to="/contact">Contact us</router-link>
                </div>
                <el-header class="header">
                    <br/>
                    <div class="welcome">Welcome to the blog !</div>
                </el-header>
                <el-image
                    style="width: 1000px; height: 500px; margin-bottom: 1em;"
                    src="/src/assets/paysage.png"
                    fit="contain">
                </el-image>
                <el-container class="container">
                    <el-main class="main">
                        <router-view></router-view>
                    </el-main>

                </el-container>
            </div>
        </div>
    <!-- <Home/> -->
    <!-- <Home :msg="v.msg" /> -->
    </div>
</div>
</template>

<style>
.user{
    font-family: Avenir, Helvetica, Arial, sans-serif;
}

.connect{
    width: 890px;
    text-align: right;
}

.connect2{
    height: 40px;
    width: 40px;
}

.welcome{
    /* font-family: Luminari, fantasy; */
    margin-bottom: 3em;
    margin-top: 10px;
    color: lavenderblush;
    text-align:center;
    font-size: 40px;
    /* text-align:center ; */
}
.nav{
    text-align: center;
    font-size: 20px;
    color: white;
    margin-bottom: 1em;
}

.contain{
    width: 1000px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 2.5em;
}

.container{
    width: 890px;
    position: inherit;
    margin-left: auto;
    margin-right: auto;

}

.header{
    height: 90px;
    width: 890px;
    text-align: left;
    position: inherit;
    background-color: #545c64;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 1em;
}

.main{
    width: 790px;
    text-align: center;
    position: inherit;
    background-color:lightsalmon;
}

/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
