<template>
  <div class="modal" :class="{ 'show': isVisible }" :style="isVisible ? 'display: block;' : 'display: none;'">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">게시글 작성</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="titleInput" class="form-label">제목</label>
            <input type="text" class="form-control" id="titleInput" v-model="title">
          </div>
          <div class="mb-3">
            <label for="contentInput" class="form-label">내용</label>
            <textarea class="form-control" id="contentInput" v-model="content"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" @click="closeModal">닫기</button>
          <button type="button" class="btn btn-primary" @click="submitUpdate">수정하기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits, watch } from 'vue'
import axios from 'axios'

const props = defineProps({
  isVisible: Boolean,
  existingPost: Object
})

const emit = defineEmits(['closeModal', 'postUpdated'])

const title = ref('')
const content = ref('')

const closeModal = () => {
  emit('closeModal');
};

watch(() => props.existingPost, (newPost) => {
  if (newPost) {
    title.value = newPost.title; // 원래의 게시글 제목을 title에 설정
    content.value = newPost.content; // 원래의 게시글 내용을 content에 설정
  }
}, { immediate: true });

function submitUpdate() {
  const postId = props.existingPost.id;
  const updatedData = { title: title.value, content: content.value };
  const token = localStorage.getItem('token');

  axios.put(`http://127.0.0.1:8000/api/v1/communities/posts/${postId}/`, updatedData, {
    headers: {
      'Authorization': `Token ${token}`,
      'Content-Type': 'application/json'
    }
  })
  .then(() => {
    emit('postUpdated');
    closeModal(); // closeModal 함수를 호출하여 모달을 닫습니다.
  })
  .catch(error => {
    console.error('Error updating post:', error);
  });
}
</script>
