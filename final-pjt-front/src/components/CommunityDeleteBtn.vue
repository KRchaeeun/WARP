<template>
    <button type="button" class="btn" @click="deletePost">게시글 삭제</button>
</template>
  
  <script setup>
  import { ref, defineEmits } from 'vue'
  import axios from 'axios'
  
  const emit = defineEmits(['deleted'])
  const props = defineProps({
    postId: Number
  })
  const token = localStorage.getItem('token')
  
  function deletePost() {
    axios.delete(`http://127.0.0.1:8000/api/v1/communities/posts/${props.postId}`, {
    headers: {
      'Authorization': `Token ${token}` // 요청 헤더에 토큰 추가
    }
    })
      .then(() => {
        emit('deleted') // 삭제 후 부모 컴포넌트에 알림
      })
      .catch(error => {
        console.error('Error deleting post:', error)
      })
  }
  </script>

  <style scoped>
  .btn {
    color: white;
    border: 3px solid white;
    margin: 30px;
  }

  </style>