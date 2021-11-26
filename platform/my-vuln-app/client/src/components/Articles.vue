<script setup>
import { onMounted } from '@vue/runtime-core'
import { reactive, ref } from 'vue'
import axios from 'axios';

const form = reactive({
    articles: [],
    art_content: [],
    art_auth: [],
    art_title: [],
    art_temp: [],
    art_date: [],
    art_time: [],
    art_id: [],
    is_loading: true,
    subject: '',
    email: '',
    i: 0,
    message: '',
    
})

const getArticles = () =>{
    axios.get('http://localhost:8181/article')
    .then(res => {
        for (let i = 0; i < res.data.articles.length; i++){
            form.art_temp[i] = res.data.articles[i].date 
            form.art_auth[i] = res.data.articles[i].author
            form.art_content[i] = res.data.articles[i].content 
            form.art_title[i] = res.data.articles[i].title
            form.art_id[i] = res.data.articles[i].id
        }
        if (form.art_id.length !== 0){
            form.is_loading = false
            for (const x in form.art_temp){
                const split = form.art_temp[x].split('T')
                form.art_date[x] = split[0]
                form.art_time[x] = split[1]
                console.log(form.art_time)
            }
        }
    })
}

const increment = () => {
    count.value += 1
    console.log(count)
}

onMounted(() => {
  getArticles()
})

</script>

<template>
<div v-if="form.is_loading === false">
    <div v-for="index in form.art_id" :key="index">
        <el-row class="title">
            <h2> <i>{{form.art_title[index-1]}}</i> </h2>
        </el-row>
        <el-row>
            <el-image
                style="width: 500px; height: 250px; margin-bottom: 1em; border-radius: 2px;"
                src="/src/assets/ski.jpg"
                fit="contain">
            </el-image>
        </el-row>
        <el-row class="author">
            <el-col :span="1.8">
                <div>
                    Author:
                </div>
            </el-col>
            <el-col :span="3">
                <div>
                    <i>
                        {{form.art_auth[index-1]}},
                    </i>
                </div>
            </el-col>
            <el-col :span="1.8">
                <div>
                    Date:
                </div>
            </el-col>
            <el-col :span="3">
                <div>
                    <i>
                        {{form.art_date[index-1]}},
                    </i>
                </div>
            </el-col>
            <el-col :span="1.5">
                <div>
                    Time:
                </div>
            </el-col>
            <el-col :span="3">
                <div>
                    <i>
                         {{form.art_time[index-1]}}
                    </i>
                </div>
            </el-col>
        </el-row>
        <br/>
        <el-row>
            <div>
                {{form.art_content[index-1]}} 
            </div>
        </el-row>
    <br/>
    </div>
    <el-row class="comment">
        <h3>Leave a comment :</h3>
    </el-row>
    <el-row>
        <div>
            <el-form 
                ref="form" 
                :model="form" 
                size="medium" 
                label-width="200px">
                    <el-form-item class="textForm" label="Subject">
                        <el-input :v-model="form.subject" clearable placeholder="Enter your subject"></el-input>
                    </el-form-item>
                    <el-form-item class="textForm" label="Email">
                        <el-input v-model="form.email" clearable placeholder="Enter your email"></el-input>
                    </el-form-item>
                    <el-form-item  class="textForm" label="Your message" prop="desc">
                        <el-input v-model="form.message" type="textarea" placeholder="Write your message"></el-input>
                    </el-form-item>
            </el-form>
            <div>{{form.subject}}</div>
        </div>
    </el-row>
</div>
</template>

<style>

.test{
    color:blue;
    left: 50px;
    top: 50px;
}

.title{
    text-align: left;
    font-family: Bradley Hand, cursive;
}

.author{
    text-align: left;
    font-size: 16px;
    font-family: Bradley Hand, cursive;
}

.comment{
    font-family: Bradley Hand, cursive;
}

.textForm{
    font-family: Bradley Hand, cursive;
    font-size: 12px;
    position: left;
}
</style>