<script setup>

defineProps({
  msg: String
})

</script>

<template>
<div>
    <h1 class="home">You can read Articles and post a comment</h1> 
    <div class="textHome">(Remember, you need to be connected to be able to post a comment !)</div>   
</div>
</template>

<style>
.home{
    font-family: Bradley Hand, cursive;
}

.textHome{
    font-family: Bradley Hand, cursive;
}
</style>