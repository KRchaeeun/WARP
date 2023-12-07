<!-- 최신순, 좋아요순으로 정렬할 버튼 -->
<template>
    <div class="filter-buttons">
      <button @click="sortPosts('latest')">최신순</button>
      |
      <button @click="sortPosts('likes')">좋아요 순</button>
    </div>
  </template>
  
  <script setup>
  // 이벤트를 발생시키기 위한 Emits 함수 정의
  const emit = defineEmits(['sortPosts'])
  
  // 게시글을 정렬하는 함수
  function sortPosts(order) {
    emit('sortPosts', order)
  }
  </script>
  
  <style scoped>
  .filter-buttons {
    margin-bottom: 20px;
    text-align: right;
  }
  </style>