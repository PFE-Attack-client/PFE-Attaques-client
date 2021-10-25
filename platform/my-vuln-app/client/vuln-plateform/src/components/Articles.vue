<script setup>
import { reactive, ref } from 'vue'

const form = reactive({
    subject: '',
    email: '',
    message: '',
})
</script>

<template>
<div>
    <el-row  class="title">
        <h2> <i>skiing trip !!</i> </h2>
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
                    White hat
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
                    28/06/2021
                </i>
            </div>
        </el-col>
    </el-row>
    <br/>
    <el-row>
        <div>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam a elementum nunc. Maecenas fermentum libero eget erat suscipit eleifend. In rhoncus commodo viverra. 
            Sed blandit ligula nec auctor semper. Donec libero nisi, finibus a semper eget, imperdiet ac urna. Vestibulum vitae iaculis nibh. Quisque id augue ac nisl facilisis tincidunt. 
            Morbi malesuada libero eget odio euismod, at laoreet nisi cursus. Aliquam consectetur risus ac elit viverra, bibendum egestas ante dapibus.
            Proin interdum, nulla ac mattis gravida, nulla nulla vehicula eros, nec commodo turpis sem finibus turpis. Curabitur tempus mollis justo quis sagittis. 
            Nulla nec urna tincidunt, sodales nulla vel, auctor justo. Donec sed fermentum elit. Morbi lorem dolor, suscipit sit amet eros sit amet, finibus rutrum velit. 
            Sed quis ultrices felis. Sed euismod finibus accumsan.
            Quisque vulputate, enim quis suscipit fermentum, arcu massa facilisis massa, a ultrices orci nibh quis orci. Integer id dui diam. 
            Nulla vel nisl sit amet turpis fringilla molestie vitae nec quam. Morbi augue mi, mattis quis odio quis, viverra sodales enim. Quisque gravida pulvinar laoreet. 
            Sed dapibus feugiat mauris ac sodales. Proin vitae tellus et metus sollicitudin tempor non quis ipsum. Ut ut mollis est, ut ultricies nulla. 
            Proin semper eros lorem, ac porttitor lectus auctor gravida. 
        </div>
    </el-row>
    <br/>
    <el-row class="comment">
        <h3>Leave a comment :</h3>
    </el-row>
    <el-row>
        <el-form ref="form" :model="form" size="medium" label-width="200px">
            <el-form-item class="textForm" label="Subject">
                <el-input v-model="form.subject"></el-input>
            </el-form-item>
            <el-form-item class="textForm" label="Email">
                <el-input v-model="form.email"></el-input>
            </el-form-item>
            <el-form-item  class="textForm" label="Your message" prop="desc">
                <el-input v-model="form.message" type="textarea"></el-input>
            </el-form-item>
        </el-form>
    </el-row>
</div>
</template>

<style>

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