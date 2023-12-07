<template>
  <div class="main">
    <!-- <h2>댓글 목록</h2> -->
    <CommentCreateForm @createComment="createComment" />
    <div v-if="comments.length > 0">
      <ul>
        <li v-for="comment in comments" :key="comment.id">
          <div class="comment" v-if="!comment.isEditing">
            
            <p>작성자: {{ comment.user.username }}</p>
            <p>내용: {{ comment.content }}</p>
            <p>작성일: {{ comment.created_at }}</p>
            <div class="holebtn" v-if="comment.isAuthor">
              <button @click="toggleEdit(comment)">수정</button>
              <button @click="deleteComment(comment.id)">삭제</button>
            </div>

          </div>
          <div v-else>
            <br>
            <br>
            <form @submit.prevent="updateComment(comment)">
              <textarea v-model="comment.editedContent"></textarea>
              <br>
              <button type="submit">저장</button>
            </form>
          </div>
        </li>
      </ul>
    </div>
    <div class="nocomment" v-else>
      <p>댓글이 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import CommentCreateForm from '@/components/CommentCreateForm.vue'

const props = defineProps({
  postId: Number
})

const comments = ref([])
const userId = localStorage.getItem('username'); // 현재 사용자 ID를 localStorage에서 가져옴
console.log(userId)
// 댓글 목록 불러오기
function fetchComments() {
  axios.get(`http://127.0.0.1:8000/api/v1/communities/posts/${props.postId}/comments/`, {
    headers: {
      'Authorization': `Token ${token}`
    }
  })
  .then(response => {
    comments.value = response.data.map(comment => ({
      ...comment,
      isEditing: false,
      isAuthor: comment.user.username === userId
    }));
    console.log(comments.value); // 'comments.value' 전체를 로깅
  })
  .catch(error => console.error('Error fetching comments:', error));
}

const token = localStorage.getItem('token') // 토큰 가져오기
watch(() => props.postId, fetchComments, { immediate: true })

onMounted(fetchComments)

watch(() => props.postId, fetchComments, { immediate: true })

// 댓글 수정 토글
function toggleEdit(comment) {
  comment.isEditing = !comment.isEditing
  comment.editedContent = comment.content
}


// 댓글 생성 로직
function createComment(content) {
  if (!token) {
    console.error('Token not found. User is not authenticated.')
    return
  }

  const commentData = {
    content: content,
  }

  axios.post(`http://127.0.0.1:8000/api/v1/communities/posts/${props.postId}/comments/`, commentData, {
    headers: {
      'Authorization': `Token ${token}` // Django가 Token 기반 인증을 사용하는 경우
    }
  })
  .then(response => {
    console.log('Comment created:', response.data)
    fetchComments() // 댓글 목록을 다시 불러오는 메서드를 호출
  })
  .catch(error => {
    console.error('Error creating comment:', error)
  })
}


// 댓글 수정 로직
function updateComment(comment) {
  if (!token) {
    console.error('Token not found. User is not authenticated.')
    return
  }

  const updatedCommentData = {
    content: comment.editedContent, // 수정된 내용
  }

  axios.put(`http://127.0.0.1:8000/api/v1/communities/comments/${comment.id}/`, updatedCommentData, {
    headers: {
      'Authorization': `Token ${token}` // Django가 Token 기반 인증을 사용하는 경우
    }
  })
  .then(response => {
    console.log('Comment updated:', response.data)
    comment.isEditing = false // 수정 모드 종료
    fetchComments() // 댓글 목록을 다시 불러오는 메서드를 호출
  })
  .catch(error => {
    console.error('Error updating comment:', error)
  })
}


// 댓글 삭제 로직
function deleteComment(commentId) {
  if (!token) {
    console.error('Token not found. User is not authenticated.')
    return
  }

  axios.delete(`http://127.0.0.1:8000/api/v1/communities/comments/${commentId}/`, {
    headers: {
      'Authorization': `Token ${token}` // Django가 Token 기반 인증을 사용하는 경우
    }
  })
  .then(() => {
    console.log('Comment deleted')
    fetchComments() // 댓글 목록을 다시 불러오는 메서드를 호출하여 목록 갱신
  })
  .catch(error => {
    console.error('Error deleting comment:', error)
  })
}
</script>

<style scoped>
.main {
  background-color: rgb(54, 54, 54);
  height: 100vh;
  padding: 50px;
}

.main li {
  list-style-type: none;
}

.main ul {
  padding-top: 30px;
  padding-left: 0px;
}

.nocomment {
  padding-top: 30px;
  color: rgba(128, 128, 128, 0.623);
}

button {
  border: 3px solid white;
  padding-top: 0;
  border-radius: 10px;
}

.holebtn {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding-top: 20px;
}

.comment {
  margin-top: 50px;
}

</style>
