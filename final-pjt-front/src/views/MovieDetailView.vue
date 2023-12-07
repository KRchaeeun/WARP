<template>
  <div class="main">
    <!-- <button class="gohome" @click="goHome">HOME</button> -->
    
    <div v-if="movie" class="movie-card-detail">
      
      <div class="movie-display">
        <div class="movie-display-main">
          <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`">
          <div class="content">
            <div class="genres" v-if="movie.genres && movie.genres.length">
              <ul>
                <li v-for="genre in movie.genres" :key="genre.id">{{ genre.name }}</li>
              </ul>
            </div>
              <p class="contenttitle">{{ movie.title }}</p>
              <div class="info">
                <p>개봉일 : {{ movie.release_date }}</p>
                <p>상영시간 : {{ formatRuntime(movie.runtime) }}</p>
                <p>평균 별점 : {{ formatNumber(movie.vote_average) }}</p>
                <p>인기도 : {{ formatNumber(movie.popularity) }}</p>
              </div>
          </div>
        </div>
        
        <button @click="toggleLiked">
          <span v-if="movie.liked" class="material-symbols-outlined">
            heart_minus
          </span>
          <span v-else class="material-symbols-outlined">
            heart_plus
          </span>
        </button>
        <button @click="toggleWish">
          <span v-if="movie.wishlist" class="material-symbols-outlined">
            bookmark_remove
          </span>
          <span v-else class="material-symbols-outlined">
            bookmark_add
          </span>
        </button>
        
        
        <p class="contentoverview">줄거리 : {{ movie.overview }}</p>
        
        <iframe v-if="movie.videos && movie.videos.length > 0" width="70%" height="315" :src="getVideoUrl(movie.videos[0])" frameborder="0" allowfullscreen></iframe>
      
      </div>


      <div><strong>{{ username }}</strong> 님을 위한 <strong>{{ movie.title }}</strong>과 비슷한 영화 추천</div>
      
      <div v-if="similarMovies.length" class="similar-movies-container">
        <div v-for="similarMovie in similarMovies" :key="similarMovie.id" class="similar-movie-item">
          <div @click="goToMovieDetail(similarMovie.id)">
            <img :src="`https://image.tmdb.org/t/p/original${similarMovie.poster_path}`">
          </div>
          <div class="similar-movie-title">{{ similarMovie.title }}</div>
        </div>
      </div>

      <div v-else>
        <strong>로딩 중...</strong>
      </div>

    </div>
  </div>
  
  <div>
    <ReviewList />
  </div>

</template>


<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import axios from 'axios'
import ReviewList from '@/components/ReviewList.vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const movie = ref(null)
const similarMovies = ref([])
const store = useAuthStore()
const username = store.username

// 페이지가 로드될 때 실행
onMounted(() => {
  fetchMovie()
})

const movieId = ref(route.params.movie_id)

watch(movieId, () => {
  fetchMovie()
}, { immediate: true })

// 영화 정보 가져오기
function fetchMovie() {
  const mypage = JSON.parse(localStorage.getItem('mypage')) || []

  if (movieId) {
    axios.get(`http://127.0.0.1:8000/api/v1/movies/${movieId.value}`)
      .then(response => {
        movie.value = response.data
        movie.value.liked = mypage.some(item => item.id === movie.value.id && item.liked)
        movie.value.wishlist = mypage.some(item => item.id === movie.value.id && item.wishlist)

        fetchSimilarMovies()
      })
      .catch(err => console.error(err))
  } else {
    console.error('Movie ID is undefined')
  }
}
onBeforeRouteUpdate((to, from) => {
  console.log('onBeforeRouteUpdate',to.params)
  movieId.value=to.params.movie_id
  fetchMovie()
  console.log('onBeforeRouteUpdate',movie.value)
})

function fetchSimilarMovies() {
  if (movie.value.id) {
    const options = {
      method: 'GET',
      headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1Yzk1MjAyNzQ2Njg1Y2Q1NDUwNTM4ZjdhYTcxOGY3NiIsInN1YiI6IjY1M2Y1MDhhY2M5NjgzMDBjOWU0ZTkzNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.tTzg95Rf9a-1A21zZPard3tyJYjlIRhLBoqo2qkAN0Y'
      }
    }
    fetch(`https://api.themoviedb.org/3/movie/${movie.value.id}/similar?language=ko-KR&page=1`, options)
      .then(response => response.json())
      .then(response => {
        similarMovies.value = response.results.filter(movie => movie.poster_path).slice(0, 5)
      })
      .catch(err => {
        console.error(err)
        router.push({ name: 'MovieDetail', params: { movie_id: route.params.movie_id } })
      });
  }
}

const goToMovieDetail = (movieId) => {
  router.push({ name: 'MovieDetail', params: { movie_id: movieId } });
}

// 포맷 함수들
const formatRuntime = runtime => runtime ? `${runtime}분` : ''
const formatNumber = number => number ? number.toFixed(1) : ''
const getVideoUrl = video => video ? `https://www.youtube.com/embed/${video.key}` : ''

// 좋아요 토글
const toggleLiked = () => {
  axios.post(`http://127.0.0.1:8000/api/v1/accounts/movies/${movie.value.id}/like/`, {
    }, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`
      }
    })
    .then(response => {
      // 서버 응답에 따라 상태 업데이트
      movie.value.liked = !movie.value.liked;
    })
    .catch(error => {
      console.error('좋아요 상태 변경 실패:', error);
    });
};

// 위시리스트 토글
const toggleWish = () => {
  axios.post(`http://127.0.0.1:8000/api/v1/accounts/movies/${movie.value.id}/wishlist/`, {
    }, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`
      }
    })
    .then(response => {
      // 서버 응답에 따라 상태 업데이트
      movie.value.wishlist = !movie.value.wishlist;
    })
    .catch(error => {
      console.error('위시리스트 상태 변경 실패:', error);
    });
};


// 홈으로 이동
const goHome = () => {
  router.push('/HomeRecommend')
}

</script>

<style scoped>
.main {
  padding-left: 10%;
  padding-right: 13%;
}

img {
  padding-top: 40px;
  border-radius: 10px;
  width: 30vw;
  padding-left: 10px;
}

.genres li {
  list-style-type: none;
  display: inline-block;
  padding: 0px 10px;
}

button {
  padding: 40px 60px;
}
.genres {
  padding-top: 40px;
  padding-left: 20px;
  white-space: nowrap;
  margin-bottom: 12%;
}

.genres li {
  border: 3px solid white;
  border-radius: 10px;
  margin: 0px 10px;
}
.info {
  padding-top: 40px;
}

.content p {
  padding-top: 5%;
  margin: 0% 20%;
  text-align: left;
  width: 60%;
}

.contentoverview {
  padding: 0% 10%;
}

iframe {
  margin-top: 60px;
  margin-bottom: 60px;
  border-radius: 10px;
}
.movie-display {
  border-radius: 20px;
  box-shadow: 20px 20px 60px 60px gray;
  padding-top: 50px;
  padding-bottom: 50px;
  margin-bottom: 50px;
  overflow: hidden; /* 이 부분을 추가 */
}

.movie-display-main{
  display: flex; /* Flexbox를 적용 */
  justify-content: center; /* 가로 방향으로 중앙 정렬 */
  align-items: center; /* 세로 방향으로 중앙 정렬 */
  gap: 40px;
}

.movie-card-detail {
  /* text-align: center; */
}

.similar-movies-container {
  display: flex;
  overflow-x: auto;
  white-space: nowrap;
  -ms-overflow-style: none;
  scrollbar-width: none;
  /* margin-left: 20px; */
}

.similar-movies-container::-webkit-scrollbar {
  display: none;
}

.similar-movie-item {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  width: 400px; /* 이미지와 동일한 너비 */
  height: auto; /* 높이 자동 조정 */
  margin-right: 40px;
  border-radius: 10px;
  overflow: hidden; /* 내용이 넘칠 경우 숨김 */
}

.similar-movie-item img {
  width: 100%; /* 이미지 너비를 카드 너비에 맞춤 */
  height: 100%; /* 이미지 높이를 자동으로 설정 */
  object-fit: cover; /* 이미지 비율 유지 */
}

.similar-movie-title {
  word-wrap: break-word; /* 단어가 너비를 초과할 경우 줄바꿈 */
  width: 100%; /* 부모 컨테이너의 너비에 맞춤 */
  text-align: center;
  padding: 10px;
}

</style>
