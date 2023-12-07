<template>
    <button type="button" class="btn" @click="showUpdateModal">게시글 수정</button>
</template>
  
<script setup>
import { defineEmits } from 'vue'

const emit = defineEmits(['update'])

function showUpdateModal() {
  emit('update')
}
</script>

<style scoped>
  .btn {
    color: white;
    border: 3px solid white;
    margin: 30px;
  }
</style>
