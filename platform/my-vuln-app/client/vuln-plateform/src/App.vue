<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
import { reactive } from '@vue/reactivity'
import Home from './components/Home.vue'
const v = reactive({
  msg: 'coucou',
})
</script>

<template>
 <div>
    
   <div class="contain">
        <div>
            <div class="nav">
                    <router-link to="/home">Home</router-link> /
                    <router-link to="/about">About</router-link>
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
</template>

<style>
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
    height: 200px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 2.5em;
}

.container{
    width: 890px;
    height: 100px;
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
    height: 90px;
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
