<!-- 커뮤니티 생성 모달창 -->
<template>
  <div class="modal" :class="{ 'show': isVisible }" :style="isVisible ? 'display: block;' : 'display: none;'">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">게시글 작성</h5>
          <!-- <button type="button" class="btn-close" @click="closeModal"></button> -->
        </div>
        <div class="modal-body">
          <div class="mb-3">
            <label for="titleInput" class="form-label">TITLE</label>
            <input type="text" class="form-control" id="titleInput" v-model="title">
          </div>
          <div class="mb-3">
            <label for="contentInput" class="form-label">CONTENT</label>
            <textarea class="form-control" id="contentInput" v-model="content"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btnclose" @click="closeModal">CLOSE</button>
          <button type="button" class="btnsave" @click="submitPost">SAVE</button>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script setup>
import { ref, defineEmits } from 'vue'
import axios from 'axios'

const props = defineProps({
  isVisible: Boolean
})

const emit = defineEmits(['closeModal', 'postCreated'])

const title = ref('')
const content = ref('')

function submitPost() {
  if (title.value && content.value) {
    axios.post('http://127.0.0.1:8000/api/v1/communities/posts/', {
      title: title.value,
      content: content.value
    }, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`
      }
    })
    .then(() => {
      // 게시글 생성 후 처리
      title.value = ''
      content.value = ''
      emit('closeModal')
      // 커뮤니티 목록을 다시 불러오는 로직 추가
      emit('postCreated')
    })
    .catch(err => {
      console.error('Error creating post:', err)
    })
  }
}

function closeModal() {
  emit('closeModal')
}
</script>
  
<style scoped>

.modal {
  background-color: rgba(0, 0, 0, 0.637);
}
.modal-content {
  color: white;
  background-color: rgb(68, 68, 68);
  box-shadow: 60px 60px 120px 120px rgb(20, 20, 20);
  border: none;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 50%;
}
.btnclose {
  color: gray;
}
.btnsave {
  color: rgb(103, 103, 206);
}

</style>