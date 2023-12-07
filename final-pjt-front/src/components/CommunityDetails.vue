<template>
  <div class="container" v-if="post">
    <div class="subinfo">
      <p @click="goToUserProfile(post)">WRITER :  {{ post.user.username }}</p>
      <p>WRITE_DATE : {{ post.created_at }}</p>
    </div>
    <h2>TITLE : {{ post.title }}</h2>
    <h2>CONTENT : {{ post.content }}</h2>
  </div>
  <div v-else>
    <p>게시글을 불러오는 중...</p>
  </div>
</template>
  
<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth' // auth 스토어 가져오기

const props = defineProps({
  post: Object
})

const router = useRouter();
const store = useAuthStore(); // auth 스토어 사용
const currentUser = store.username; // 현재 로그인한 사용자의 사용자명

const goToUserProfile = (post) => {
  if (post && post.user && post.user.username) {
    console.log('Post User:', post.user.username); // 작성자 정보를 콘솔에 출력
    if (currentUser === post.user.username) {
      // 작성자가 현재 사용자와 같으면 MyPage로 이동
      console.log('Going to MyPage');
      router.push({ name: 'MyPage', params: { username: currentUser } });
    } else {
      // 작성자가 현재 사용자와 다르면 해당 사용자의 프로필 페이지로 이동
      console.log('Going to UserProfile');
      router.push({ name: 'MyPage', params: { username: post.user.username } });
    }
  } else {
    console.error('Post 정보가 없거나 유효하지 않습니다.');
  }
}
</script>

  
<style scoped>
h2 {
  padding: 20px;
} 

.subinfo {
  text-align: center;
  padding-top: 50px;
  padding-bottom: 10px;
}

.container {
  border-radius: 50%;
  box-shadow: 20px 20px 60px 60px gray;
  padding-bottom: 70px;
}

</style>
