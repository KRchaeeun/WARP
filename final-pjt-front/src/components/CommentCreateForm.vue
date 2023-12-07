<template>
    <div>
      <h3>COMMENT</h3>
      <br>
      <form @submit.prevent="submitReview">
        <div>
          <label for="content"></label>
          <textarea v-model="newReview.content" id="content" required></textarea>
        </div>
        <button type="submit">CREATE</button>
      </form>
    </div>
  </template>

<script setup>
import { ref, defineEmits } from 'vue'

// 이벤트를 발생시키기 위한 emit 정의
const emit = defineEmits(['createComment'])

// 댓글 내용을 저장할 반응형 데이터 객체
const newReview = ref({
  content: ''
})

// 폼 제출 이벤트 핸들러
const submitReview = () => {
  if (!newReview.value.content) {
    alert('댓글 내용을 입력해주세요.')
    return
  }

  // 부모 컴포넌트에 댓글 내용을 전달하고, 폼을 초기화
  emit('createComment', newReview.value.content)
  newReview.value.content = ''
}

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fugaz+One&display=swap');

h3 {
  font-family: 'Fugaz One', sans-serif !important;
  font-size: 30px;
  color: white !important;

  /* 드래그 방지 */
  -webkit-user-select:none;
  -moz-user-select:none;
  -ms-user-select:none;
  user-select:none
}

button {
  padding-top: 0px;
  border: 3px solid white;
  border-radius: 10px;
  margin-top: 20px;
}

</style>