<template>
    <div class="mainly">
      <CommunityDetails :post="post" />
      <CommunityUpdateModal
        v-if="isUpdateModalVisible"
        :isVisible="isUpdateModalVisible"
        :existingPost="post"
        @closeModal="toggleUpdateModal(false)"
        @postUpdated="handlePostUpdated"
      />  
      <button class="btn art" @click="toggleLike">
        <span v-if="isLiked" class="material-symbols-outlined">
          게시글 thumb_down
        </span>
        <span v-else class="material-symbols-outlined">
          게시글 thumb_up
        </span>
      </button>
      <div class="holebtn" v-if="isAuthor">
        <CommunityUpdateBtn @update="toggleUpdateModal" />
        <CommunityDeleteBtn v-if="post" :postId="post.id" @deleted="handleDeletion" />
      </div>
    </div>
    <div>
      <CommentList v-if="post" :postId="post.id" />
    </div>
</template>
  
<script setup>
import { ref, onMounted, defineEmits } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import CommunityDetails from '@/components/CommunityDetails.vue'
import CommunityDeleteBtn from '@/components/CommunityDeleteBtn.vue'
import CommunityUpdateBtn from '@/components/CommunityUpdateBtn.vue'
import CommunityUpdateModal from '@/components/CommunityUpdateModal.vue'
import CommentList from '@/components/CommentList.vue'


const route = useRoute()
const post = ref(null)
const emit = defineEmits(['like-updated'])
const userId = ref(localStorage.getItem('username')); // 현재 사용자 ID를 localStorage에서 가져옴
console.log(userId.value)
onMounted(() => {
  fetchPost()
})

function fetchPost() {
  const postId = route.params.community_id;
  const token = localStorage.getItem('token');
  axios.get(`http://127.0.0.1:8000/api/v1/communities/posts/${postId}`, {
    headers: {
      'Authorization': `Token ${token}`
    }
  })
    .then(response => {
      post.value = response.data;
      console.log(post.value.user.username);
      isLiked.value = response.data.user_has_liked;
      // 추가: 현재 사용자와 게시글 작성자 비교
      isAuthor.value = post.value.user.username === userId.value;
    })
    .catch(error => {
      console.error('Error fetching post:', error);
    });
}

const isAuthor = ref(false);

// 게시글 수정
const isUpdateModalVisible = ref(false)

function toggleUpdateModal(show = true) {
  // console.log(`Updating modal visibility to ${show}`);
  isUpdateModalVisible.value = show;
}

function handlePostUpdated() {
  // 게시글 목록을 다시 불러오기
  fetchPost();
}
// 게시글 삭제 
const router = useRouter()

function handleDeletion() {
  router.push('/community') // 게시글 리스트 페이지로 리디렉트
}

// 좋아요 상태를 추적하는 반응형 참조
const isLiked = ref(false)


// 좋아요 버튼 토글 함수
function toggleLike() {
  if (isLiked.value) {
    // 이미 좋아요가 된 상태라면 좋아요 취소 요청 보내기
    removeLike()
  } else {
    // 좋아요가 되지 않은 상태라면 좋아요 요청 보내기
    addLike()
  }
}


// 좋아요 상태 업데이트 함수
function updateLikeStatus(updatedLikeCount) {
  emit('like-updated', { postId: route.params.community_id, likeCount: updatedLikeCount });
}


// 좋아요 요청 보내기
function addLike() {
  const postId = route.params.community_id
  const token = localStorage.getItem('token')
  axios.post(`http://127.0.0.1:8000/api/v1/communities/posts/${postId}/like/`, {}, {
    headers: {
      'Authorization': `Token ${token}`
    }
  })
  .then(() => {
      isLiked.value = true
      const updatedLikeCount = post.value.like_count + 1
      post.value.like_count = updatedLikeCount
      updateLikeStatus(updatedLikeCount)
    })
    .catch(error => {
      console.error('Error adding like:', error)
      console.log(postId)
      console.log(token)
    })
}

// 좋아요 취소 요청 보내기
function removeLike() {
  const postId = route.params.community_id
  const token = localStorage.getItem('token')
  axios.post(`http://127.0.0.1:8000/api/v1/communities/posts/${postId}/like/`, {}, {
  headers: {
    'Authorization': `Token ${token}`
  }
})
.then(() => {
    isLiked.value = false
    const updatedLikeCount = Math.max(0, post.value.like_count - 1)
    post.value.like_count = updatedLikeCount
    updateLikeStatus(updatedLikeCount)
  })
}

// 좋아요 상태 초기화
onMounted(() => {
  fetchPost()
  // checkLikeStatus()
})

</script>
  
<style scoped>
.holebtn {
  padding-top: 0px;
  padding-bottom: 100px;
}

.material-symbols-outlined {
  font-size: 25px; /* 이 값을 조정하여 아이콘 크기 변경 */
}
.mainly {
    width: 100vw;
    min-height: 50vh;
    background-color: rgb(54, 54, 54);
    text-align: center;
    color: white;
    padding-left: 3%;
    padding-right: 3%;
    padding-bottom: 50px;
}
.art {
  margin-top: 20px;
}
</style>
  