<!-- 커뮤니티 전체 게시글 리스트 -->
<template>
  <div>
    <table class="table">
      <thead>
        <tr class="lst">
          <th scope="col">목록</th>
          <th scope="col">제목</th>
          <th scope="col">작성자</th>
          <th scope="col">작성일시</th>
          <th scope="col">좋아요 수</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="posts && posts.length" v-for="(post, index) in posts" :key="post.id" @click="navigateToPostDetail(post.id)">
          <th scope="row">{{ index + 1 }}</th>
          <td>{{ post.title }}</td>
          <td>{{ post.user.username }}</td>
          <td>{{ post.created_at }}</td>
          <td>{{ post.like_count }}</td>
        </tr>
        <tr v-if="!posts.length">
          <td colspan="5" class="text-center">게시글이 없습니다.</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

// props 정의
const props = defineProps({
  posts: Array
})

const router = useRouter()

const navigateToPostDetail = (postId) => {
  router.push({ name: 'CommunityDetail', params: { community_id: postId } })
}

// 게시글의 좋아요 개수를 업데이트하는 함수
function updatePostLikeCount(postId, likeCount) {
  const post = props.posts.find(p => p.id === postId)
  if (post) {
    post.like_count = likeCount
  }
}
</script>

<style scoped>
.table th, .table td {
  background-color: rgb(54, 54, 54);
  color: white;
}

.lst {
  justify-content: space-around;
}
</style>