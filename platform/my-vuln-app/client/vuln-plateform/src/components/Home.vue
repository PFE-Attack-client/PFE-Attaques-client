<script setup>

defineProps({
  msg: String
})

</script>

<template>
<div>
    Home
    <!-- <div class="contain">
        <div>
            <el-header class="header">
                <br/>
                 <span class="welcome">Welcome to the blog !</span>
                 <div class="nav">
                 <router-link to="/login">Login</router-link>
                 <router-view></router-view>
                 </div>
            </el-header>
            <el-image
                style="width: 1000px; height: 500px; margin-bottom: 1em;"
                src="/src/assets/paysage.png"
                fit="contain">
               
            </el-image>
            <el-container class="container">
                <el-main class="main">
                    <div>Coucou</div>
                </el-main>

            </el-container>
        </div>
    </div> -->
    
</div>
</template>

<style>
/* .welcome{
    font-family: Luminari, fantasy; */
    /* margin-bottom: 3em;
    margin-top: 10px;
    color: lavenderblush;
    text-align:left;
    font-size: 40px; */
    /* text-align:center ;
} 
/* .nav{
    text-align: right;
    font-size: 30px;
} */

/* .contain{
    width: 1000px;
    height: 200px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 10em;
} */

/* .container{
    width: 890px;
    height: 100px;
    position: inherit;
    margin-left: auto;
    margin-right: auto;

} */

/* .header{
    height: 90px;
    width: 890px;
    text-align: left;
    position: inherit;
    background-color: #545c64;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 1em;
} */

/* .main{
    height: 90px;
    width: 790px;
    text-align: center;
    position: inherit;
    background-color:lightsalmon;
} */

</style>