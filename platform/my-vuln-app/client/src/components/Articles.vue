<script setup>
import { onMounted, watch } from '@vue/runtime-core'
import { reactive, ref } from 'vue'
import axios from 'axios';

const ip_serv = 'localhost:8181'

const form = reactive({
    articles: [],
    comment: [],
    art_content: [],
    art_auth: [],
    art_title: [],
    art_temp: [],
    art_date: [],
    art_time: [],
    art_id: [],
    is_loading: true,
    article: '',
    subject: '',
    email: '',
    message: '',
})

// const com = reactive({
//     display: false,
//     id: [],
//     author: {},
//     content: [],
//     temporal: [],
//     date: [],
//     time: [],
//     title: [],
//     link_art_id: [],
// })

const getArticles = () => {
    axios.get(`http://${ip_serv}/article`)
    .then(res => {
        form.articles = res.data.articles
        for (let i = 0; i < res.data.articles.length; i++){
            form.art_temp[i] = res.data.articles[i].date 
            form.art_auth[i] = res.data.articles[i].author
            form.art_content[i] = res.data.articles[i].content 
            form.art_title[i] = res.data.articles[i].title
            form.art_id[i] = res.data.articles[i].id
            const y = form.art_id[i]
            
            // get the comments:

            axios.get(`http://${ip_serv}/article/${y}/comment`)
            .then(res => {
                form.comment[i] = res.data.commentaries
                // com.id[i] = []
                // com.temporal[i] = []
                // com.author[i] = []
                // com.content[i] = []
                // com.title[i] = []
                // com.link_art_id[i] = []
                // for (var j = 0; j < res.data.commentaries.length; j++){
                //     com.id[i][j] = res.data.commentaries[j].id
                //     com.temporal[i].push(res.data.commentaries[i].date)
                //     com.author[i][j] = res.data.commentaries[i].author
                //     com.content[i][j] = res.data.commentaries[i].content 
                //     com.title[i][j] = res.data.commentaries[i].title
                //     com.link_art_id[i][j] = res.data.commentaries[i].article_id
                // }
            })
        } 
        if (form.art_id.length !== 0){
            form.is_loading = false
            for (const x in form.art_temp){
                const split = form.art_temp[x].split('T')
                form.art_date[x] = split[0]
                form.art_time[x] = split[1]
            }
        }
    })
}

const postComment = () => {
    console.log(form.comment)
    console.log(form.article)
    const result = form.articles.find( article => article.title === form.article)
    const l = form.comment[result.id-1].length + 1
    const data = {        
        'article_id': result.id,
        'author': form.email,
        'content' : form.message,
        'date': "2021-11-30T21:42:55",
        'id': l,
        'title': form.subject,
    }
    axios.post(`http://${ip_serv}/article/${result.id}/comment`, data)
    .then(res=>{
        console.log(res.data)
    })
}

// const getComment = () => {
//     com.display = true
//     try {
//         console.log(form.comment[0][1].title)
//     } catch(r) {
//         console.log('cela ne fonctionne pas')
//     }

// }
    
// const increment = () => {
//     count.value += 1
//     console.log(count)
// }

// setInterval(function(){ 
//     getComment()
// }, 5000);

// onMounted(() => {
//   getArticles()
// })

watch(
  () => {
    getArticles()
  },
)

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
            <el-col :span="2.2">
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
            <el-col :span="3">
                <div>
                    <i>
                        {{form.art_date[index-1]}},
                    </i>
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
        <el-row>
            <div>
                {{form.art_content[index-1]}} 
            </div>
        </el-row>
        <br/>
        <br/>
        <div>
            <el-row class="comment">
                    <div>Comments:</div>
                </el-row>
            <br/>
            <hr>
            <br/>
            <div v-for="jindex in form.comment[index-1].length" :key="jindex">                
                <el-row :span="1.5">
                    <el-col :span="1.8">
                        <div>
                            Title:  <i>{{form.comment[index-1][jindex-1].title}}.</i>
                        </div>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="1.8">
                        <div>
                            Author: <i>{{form.comment[index-1][jindex-1].author}}.</i>
                        </div>
                    </el-col>
                </el-row>
                <br/>
                <el-row>
                    <div>
                        {{form.comment[index-1][jindex-1].content}}.
                    </div>
                </el-row>
                <br/>
                <hr>
                <br/>
            </div>
        </div>
        <br/>
        <br/>
    </div>
    <el-row class="comment">
            <div>Leave a comment :</div>
        </el-row>
        <br/>
        <el-row>
            <div class="comments">
                <el-form 
                    ref="formulaire" 
                    :model="form" 
                    size="medium" 
                    label-width="200px">
                        <el-form-item class="textForm" label="your email" label-width="540px">
                            <el-input v-model="form.email" placeholder="Enter your email"></el-input>
                        </el-form-item>
                        <el-form-item class="textForm" label="Name of the article" >
                            <el-input v-model="form.article" placeholder="Name of the article you want ot comment"/>
                        </el-form-item>
                        <el-form-item class="textForm" label="Subject" >
                            <el-input v-model="form.subject" placeholder="Enter your subject"/>
                        </el-form-item>
                        <el-form-item  class="textForm" label="Your message" prop="desc">
                            <el-input v-model="form.message" type="textarea" placeholder="Write your message"></el-input>
                        </el-form-item>
                </el-form>
            </div>
    </el-row>
    <div>
        <el-button @click="postComment" class="post">Post comment</el-button>
    </div>
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
     font-size: 20px;
     font-family: Bradley Hand, cursive;
}

.comments{
    text-align: center;
}

.post{
    margin-top: 2.5em;
    margin-bottom: 2.5em;
}

.textForm{
    font-family: Bradley Hand, cursive;
    font-size: 12px;
    position: left;
}
</style>