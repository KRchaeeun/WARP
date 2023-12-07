<script setup>
import HomeSearch from '@/components/HomeSearch.vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ref, computed } from 'vue'

const searchQuery = ref('')
const router = useRouter()
const store = useAuthStore()
const isAuthenticated = computed(() => store.isAuthenticated) // 로그인 상태
const logOut = store.logOut
const username = store.username  // 현재 로그인한 사용자의 사용자명 가져오기

const submitSearch = () => {
    // SearchView.vue로 라우팅하면서 검색 쿼리 전달
    router.push({ name: 'Search', query: { q: searchQuery.value } })
}

// 애니메이션 클래스를 반응형 데이터로 선언합니다.
const isAnimating = ref(false)

// 로고 클릭 시 호출할 메소드입니다.
const triggerAnimation = () => {
  // 애니메이션 시작
  isAnimating.value = true

  // 애니메이션이 끝나는 시간(여기서는 1초) 후에 클래스를 제거합니다.
  setTimeout(() => {
    isAnimating.value = false
  }, 1000) // animate__rubberBand 애니메이션 지속 시간에 맞추세요.
}
</script>


<template>
  <header v-if="isAuthenticated">
    <div class="wrapper">
      <nav>
        <RouterLink to="/HomeRecommend">
        <img
          alt="logo"
          :class="['animate__animated', isAnimating ? 'animate__rubberBand' : '']"
          src="@/assets/logo.png"
          @click="triggerAnimation"
          style="width: 230px; height: 150px;"
        />
        </RouterLink>
        <!-- HOME, COMMUNITY, RECOMMEND, PROFILE을 하나의 div로 묶습니다. -->
        <div class="nav-links">
          <RouterLink to="/HomeRecommend">HOME</RouterLink>
          <RouterLink to="/community">COMMUNITY</RouterLink>
          <RouterLink to="/recommendation">RECOMMEND</RouterLink>
          <ul class="nav-item dropdown">
            <li>
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                PROFILE
              </a>
              <ul class="dropdown-menu">
                <li><RouterLink :to="`/mypage/${username}`" class="dropdown-item">MYPAGE</RouterLink></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#" @click="logOut">LOGOUT</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </nav>
      <div class="search-bar">
        <HomeSearch />
      </div>
    </div>
  </header>
  <RouterView />
</template>


<style>
@import "@/App.css";
nav {
  display: flex; /* Flexbox 레이아웃 사용 */
  flex-wrap: nowrap; /* 요소들이 줄바꿈되지 않고 한 줄에 표시되도록 설정 */
  align-items: center; /* 수직 방향으로 중앙 정렬 */
  justify-content: space-between; /* 요소들 사이에 공간을 동일하게 배분 */
  background-color: rgb(54, 54, 54);
  color: white;
  padding: 10px 50px;
}
    
.search-bar {
  background-color: rgb(54, 54, 54);
  height: 100px;
  /* position: absolute;
  z-index: 3; */
  right: 550px;
  top: 200px;
}

    /* 로고에 적용될 기본 크기를 설정합니다. */
.animate__rubberBand {
  width: 230px;
  height: 150px;
}

/* 커스텀 애니메이션 keyframes를 정의합니다. */
@keyframes rubberBand {
  from {
    transform: scale(1);
  }
  30% {
    transform: scale(1.25);
  }
  40%,
  60% {
    transform: scale(0.75);
  }
  100% {
    transform: scale(1);
  }
}

  nav > * {
      margin: 0 10px; /* 모든 직접 자식 요소에 마진 적용 */
  }


  nav a {
      color: white;
      text-decoration-line: none;
      padding-right: 45px;
  }

  .nav-item {
    list-style: none; /* 리스트 스타일 제거 */
    display: flex; /* 드롭다운도 flex 아이템으로 만듭니다 */
    padding-top: 17px;
    padding-left: 0px;
  }

  html, body {
  height: 100vh; /* 전체 뷰포트 높이의 100% */
  width: 100vw; /* 전체 뷰포트 너비의 100% */
  }
  .nav-links {
    display: flex; /* 내부 링크들도 flexbox 레이아웃을 사용 */
    align-items: center; /* 수직 방향으로 중앙 정렬 */
    justify-content: flex-end; /* 요소들을 오른쪽으로 정렬 */
    flex-grow: 1; /* 나머지 공간을 모두 차지하도록 설정 */
  }

  .nav-item .dropdown-menu {
    position: absolute; /* 드롭다운 위치 조정 */
    right: 0; /* 드롭다운을 오른쪽 정렬 */
  }

</style>
