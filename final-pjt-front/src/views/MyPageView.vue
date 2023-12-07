<!-- 마이페이지(프로필) -->
<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import MyPageCustom from '/src/components/MyPageCustom.vue'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()
const currentUser = store.username
const user = ref(null)
const token = localStorage.getItem('token')

// 기존 fetchUserData 함수 및 onMounted 로직 유지...

const fetchUserData = (username) => {
  return axios.get(`http://127.0.0.1:8000/api/v1/accounts/profile/${username}`, {
    headers: {
      'Authorization': `Token ${token}`
    }
  })
  .then(response => {
    return response.data;
  })
  .catch(error => {
    throw error;
  });
}

const isFollowing = ref(false);

// 사용자의 팔로우 상태를 확인하는 함수
const checkFollowStatus = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/accounts/user/${user.value.username}/follow/`, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    isFollowing.value = response.data.followed;
  } catch (error) {
    console.error('Error checking follow status:', error);
  }
};

// 팔로우 또는 언팔로우 수행
const toggleFollow = async () => {
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/v1/accounts/user/${user.value.username}/follow/`, {}, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    isFollowing.value = response.data.followed;
  } catch (error) {
    console.error('Error toggling follow status:', error);
  }
}

// computed 속성 정의 아래에 로그 추가
const isOwnPage = computed(() => {
  return currentUser === (user.value ? user.value.username : null);
})

// fetchUserData 및 onMounted 로직 내부에 로그 추가
onMounted(() => {
  const username = route.params.username
  fetchUserData(username).then(response => {
    user.value = response;
    console.log("Fetched user data:", user.value); // 로그 출력

    // fetchUserData가 완료된 후에 checkFollowStatus 호출
    checkFollowStatus();
  }).catch(error => {
    console.error('Error fetching user data:', error);
  });
});


const fetchFollowersList = async () => {
  try {
    const username = route.params.username;
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/accounts/${username}/followerslist/`, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    user.value.followers = response.data; // 팔로워 목록 업데이트
  } catch (error) {
    console.error('Error fetching followers list:', error);
  }
};

const fetchFollowingsList = async () => {
  try {
    const username = route.params.username;
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/accounts/${username}/followingslist/`, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    user.value.followings = response.data; // 팔로잉 목록 업데이트
  } catch (error) {
    console.error('Error fetching followings list:', error);
  }
};

// fetchUserData 및 onMounted 로직 내부에 로그 추가
onMounted(() => {
  const username = route.params.username
  fetchUserData(username).then(response => {
    user.value = response;
    console.log("Fetched user data:", user.value); // 로그 출력

    // fetchUserData가 완료된 후에 checkFollowStatus 호출
    checkFollowStatus();

    // 팔로워와 팔로잉 목록 가져오기
    fetchFollowersList();
    fetchFollowingsList();
  }).catch(error => {
    console.error('Error fetching user data:', error);
  });
});

const deleteAccount = () => {
  axios.post('http://127.0.0.1:8000/api/v1/accounts/delete_account/', {}, {
    headers: {
      'Authorization': `Token ${token}`
    }
  })
  .then(() => {
    alert('회원 탈퇴가 완료되었습니다.')

    localStorage.removeItem('token') // 토큰 삭제
    store.logOut(); // 사용자 인증 상태 업데이트

    router.push('/') // 홈 화면으로 리디렉션
  })
  .catch(error => {
    console.error('회원 탈퇴에 실패했습니다.', error)
  })
}

// 라우트 파라미터의 변경을 감시
watch(() => route.params.username, (newUsername) => {
  if (newUsername) {
    fetchUserData(newUsername).then(response => {
      user.value = response
      checkFollowStatus()
      fetchFollowersList()
      fetchFollowingsList()
    }).catch(error => {
      console.error('Error fetching user data:', error)
    })
  }
}, { immediate: true })
</script>

<template>
  <div class="main">
    <div class="board">
      <h1>MYPAGE</h1>
      <h1 class="reverse">MYPAGE</h1>
    </div>
    <div v-if="user">
      <!-- 표시할 사용자 결정 -->
      <p class="mypage-username">{{ currentUser && currentUser.username === user.username ? currentUser.username : user.username }}</p>
      <!-- 다른 사용자의 프로필 페이지일 때만 팔로우 버튼 표시 -->
      <button v-if="!isOwnPage" @click="toggleFollow" class="btn mybtn">
        <span v-if="isFollowing" class="material-symbols-outlined">
          <p class="fonts">follow</p>
          <p>sentiment_satisfied</p>
        </span>
        <span v-else class="material-symbols-outlined">
          <p class="fonts">unfollow</p>
          <p>sentiment_dissatisfied</p>
        </span>
      </button>   
      <!-- 팔로우와 팔로잉 목록은 다른 사용자에게도 보이도록 수정 -->
      <div class="followfollowing">
        <div>
          <h2>팔로워</h2>
          <p v-if="user.followers.length === 0">목록이 비었습니다.</p>
          <p v-else v-for="(follower, index) in user.followers" :key="`follower-${index}`">
            <router-link :to="{ name: 'MyPage', params: { username: follower.username } }">{{ follower.username }}</router-link>
          </p>
        </div>
        <div>
          <h2>팔로잉</h2>
          <p v-if="user.followings.length === 0">목록이 비었습니다.</p>
          <p v-else v-for="(following, index) in user.followings" :key="`following-${index}`">
            <router-link :to="{ name: 'MyPage', params: { username: following.username } }">{{ following.username }}</router-link>
          </p>
        </div>
      </div>
      <!-- <MyPageCustom :isOwnPage="isOwnPage" /> -->
      <MyPageCustom :user="user" :isOwnPage="isOwnPage" />
      <div class="delete_account">
        <button @click="deleteAccount" class="delete_account_btn">회원탈퇴</button>
      </div>  

    </div>
    <div v-else>
      <p>페이지를 불러오는 중...</p>
    </div>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Fugaz+One&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Abril+Fatface&display=swap');

.delete_account {
  padding-bottom: 100px;
}
.fonts {
  font-size: 18px;
}
.delete_account_btn {
  color: rgb(244, 173, 173);
}

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

.reverse {
  margin-top: -78px;
  margin-left: 60px;
  color: rgb(66, 66, 66);
}

.main {
  min-height: 100vh;
}

.board {
  background-color: rgb(54, 54, 54);
  padding: 20px;
  font-weight: 900;
  font-family: 'Kanit', sans-serif;
}

.mypage-username {
  font-size: 50px;
  font-family: 'Abril Fatface', serif;
  /* border: 1px solid white; */
  border-radius: 50%;
  box-shadow: 20px 20px 50px 20px;
  padding: 15px 10px;
  margin-bottom: 5%;
  margin-left: 20%;
  margin-right: 20%;
  color: gray;
}

.mybtn {
  margin-bottom: 30px;
}
.followfollowing {
  display: flex; /* 플렉스 컨테이너 설정 */
  font-family: 'Poppins', sans-serif;
  flex-direction: row; /* 아이템들을 가로로 나열 */
  flex-wrap: wrap; /* 아이템들이 너무 많아서 한 줄에 다 못 들어갈 경우 다음 줄로 넘김 */
  gap: 70px; /* 아이템들 사이의 간격 설정 */
  margin-bottom: 70px; /* 아래쪽 마진 설정 */
  justify-content: center;

}

/* 아이템에 대한 스타일 설정 */
@import url('https://fonts.googleapis.com/css2?family=Poppins&display=swap');
.followfollowing p {
  font-family: 'Poppins', sans-serif;
  margin: 0; /* 기본 마진 제거 */
  padding: 5px; /* 패딩 설정 */
  margin-top: 20px;
  /* border: 1px solid white; */
  background-color: rgba(128, 128, 128, 0.24);
  border-radius: 5px; /* 경계선 둥글게 설정 */
  color: gray;
  padding: 20px 15px;
}

/* 팔로워와 팔로잉 목록의 링크 스타일 */
/* 팔로워와 팔로잉 목록의 링크 스타일 */
.followfollowing a {
  font-family: 'Poppins', sans-serif;
  margin: 0; /* 기본 마진 제거 */
  padding: 5px; /* 패딩 설정 */
  margin-top: 20px;
  background-color: rgba(128, 128, 128, 0.24);
  border-radius: 5px; /* 경계선 둥글게 설정 */
  color: white; /* 링크 색상 변경 */
  padding: 20px 15px;
  text-decoration: none; /* 밑줄 제거 */
}

/* 호버 효과 */
.followfollowing a:hover {
  font-size: 1.3em; /* 폰트 크기 증가 */
  cursor: pointer; /* 마우스 커서 변경 */
}

</style>
