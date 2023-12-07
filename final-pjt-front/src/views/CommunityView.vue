<!-- 커뮤니티 전체 목록 게시판 -->
<template>
  <div class="board">
    <h1>COMMUNITY</h1>
    <h1 class="reverse">COMMUNITY</h1>
    <CommunityFilterBtn @sortPosts="handleSortPosts" />
    <CommunityList :posts="sortedPosts" />
    <CommunityCreateBtn class="btn" @toggleCreateModal="toggleCreateModal" />
    <CommunityCreateModal 
        :isVisible="isCreateModalVisible" 
        @closeModal="toggleCreateModal(false)" 
        @postCreated="fetchPosts"
    /> 
  </div>
</template>

<script setup>
import axios from 'axios'
import CommunityFilterBtn from '@/components/CommunityFilterBtn.vue'
import CommunityList from '@/components/CommunityList.vue'
import CommunityCreateBtn from '@/components/CommunityCreateBtn.vue'
import CommunityCreateModal from '@/components/CommunityCreateModal.vue'

import { ref, computed, onMounted } from 'vue'

const posts = ref([])

onMounted(() => {
  fetchPosts()
})

function fetchPosts() {
  const token = localStorage.getItem('token')

  axios.get('http://127.0.0.1:8000/api/v1/communities/posts/', {
    headers: {
      'Authorization': `Token ${token}` // Django가 Token 기반 인증을 사용하는 경우
    }
  })
    .then(response => {
      posts.value = response.data
      console.log(posts.value)
    })
    .catch(error => {
      console.error('Error fetching posts:', error)
    })
}



// 현재 선택된 정렬 방식
const currentSort = ref('latest')

// 정렬된 게시글 목록을 계산하는 Computed 프로퍼티
const sortedPosts = computed(() => {
  return posts.value.slice().sort((a, b) => {
    if (currentSort.value === 'latest') {
      return new Date(b.created_at) - new Date(a.created_at)
    } else if (currentSort.value === 'likes') {
      return b.likes_count - a.likes_count
    }
    return 0
  })
})

// 정렬 이벤트를 처리하는 함수
function handleSortPosts(order) {
  currentSort.value = order
}

// 모달 표시 상태
const isCreateModalVisible = ref(false)

// 모달 토글 함수
function toggleCreateModal(show = true) {
  isCreateModalVisible.value = show
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fugaz+One&display=swap');

h1 {
  font-family: 'Fugaz One', sans-serif !important;
  font-size: 30px;
  color: rgb(102, 102, 102);
  text-align: center;
  font-size: 150px;

  /* 드래그 방지 */
  -webkit-user-select:none;
  -moz-user-select:none;
  -ms-user-select:none;
  user-select:none
}
.board {
  background-color: rgb(54, 54, 54);
  height: 100vh;
  padding-left: 50px;
  padding-right: 80px;
  font-weight: 900;
  font-family: 'Kanit', sans-serif;
}
.btn {
  color: white;
}

.reverse {
  margin-top: -78px;
  margin-left: 60px;
  color: rgb(66, 66, 66);
}

</style>