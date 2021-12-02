<script setup>
import { onMounted, watch } from '@vue/runtime-core'
import { reactive, ref } from 'vue'
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus'

const ip_serv = '10.0.0.3'

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
    leave_com: false,
})

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

const postComment = (value) => {
    if (localStorage.getItem('token') === null || localStorage.getItem('token') === 'null'){
        ElMessageBox(
        {
            message: 'You must be logged in to post a comment...'})
    }
    else{
        const result = form.articles.find( article => article.id === value)
        const args = {        
            'article_id': result.id,
            'author': form.email,
            'content' : form.message,
            'title': form.subject,
        }
        axios.post(`http://10.0.0.3/article/${result.id}/comment/`, args)
        .then(res=>{
            if(res.data.message === 'Your commentary has been saved.'){
                getArticles()
                form.email = ''
                form.message = ''
                form.subject = ''
            }
        })
        .catch(e => console.log(e))
    }
    
}

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
                    <b>Author: </b>
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
                            <b>Title: </b>  <i>{{form.comment[index-1][jindex-1].title}}.</i>
                        </div>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="1.8">
                        <div>
                            <b>Author :</b> <i>{{form.comment[index-1][jindex-1].author}}.</i>
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
            <el-row class="comment">
                <div><b>Leave a comment :</b></div>
            </el-row>
            <br/>
            <div>
                <el-row>
                    <div class="comments">
                        <el-form 
                            ref="formulaire" 
                            :model="form" 
                            size="medium" 
                            label-width="200px">
                                <el-form-item class="textForm" label="EMAIL:" label-width="540px">
                                    <el-input v-model="form.email" placeholder="Enter your email"></el-input>
                                </el-form-item>
                                <el-form-item class="textForm" label="SUBJECT: " >
                                    <el-input v-model="form.subject" placeholder="Enter your subject"/>
                                </el-form-item>
                                <el-form-item  class="textForm" label="MESSAGE:" prop="desc">
                                    <el-input v-model="form.message" type="textarea" placeholder="Write your message"></el-input>
                                </el-form-item>
                        </el-form>
                    </div>
                </el-row>
                <div>
                    <el-button @click="postComment(index)" class="post">Post comment</el-button>
                </div>
            </div>
            
    </div>
       
</div>
</template>

<style>
.title{
    font-size: 20px;
    text-align: left;
    font-family: Bradley Hand, cursive;
}

.author{
    text-align: left;
    font-size: 22px;
    font-family: Bradley Hand, cursive;
}

.comment{
     font-family: Bradley Hand, cursive;
     font-size: 22px;
     font-family: Bradley Hand, cursive;
}

.comments{
    text-align: center;
}

.post{
    margin-top: 2.5em;
    margin-bottom: 2.5em;
    color: white;
    background-color: #545c64;
}

.textForm{
    font-family: Bradley Hand, cursive;
    font-size: 18px;
    position: left;
}
</style>