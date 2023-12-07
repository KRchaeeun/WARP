<template>
    <!-- 좋아요한 영화 섹션 -->
    <div class="likemovies">
      <h2>좋아요한 영화</h2>
      <div v-if="!likedMovies">
        <p>로딩 중...</p>
      </div>
      <div v-else-if="likedMovies.length === 0">
        <p class="no">좋아요한 영화가 없습니다.</p>
      </div>
      <div v-else class="movie-list">
        <!-- 여기에 좋아요한 영화 표시 -->
      <div v-for="movie in likedMovies" :key="movie.id" class="movie-card">
        <!-- {{ movie.movie.title }} -->
        <img :src="`https://image.tmdb.org/t/p/w500${movie.movie.poster_path}`" alt="Movie Poster">
        <h3>{{ movie.movie.title }}</h3>
        <button @click="goDetail(movie.movie)">상세페이지로 이동</button>
        <button @click="removeLike(movie.movie.id)">좋아요 목록에서 삭제</button>
      </div>
    </div>
  </div>

  <!-- 위시리스트 섹션 -->
  <div class="wishlist" v-if="isOwnPage">
    <h2>위시리스트</h2>
    <div v-if="!wishlistMovies">
      <p>로딩 중...</p>
    </div>
    <div v-else-if="wishlistMovies.length === 0">
      <p class="no">위시리스트에 영화가 없습니다.</p>
    </div>
    <div v-else class="movie-list">
      <!-- 여기에 위시리스트 영화 표시 -->
      <div v-for="movie in wishlistMovies" :key="movie.id" class="movie-card">
        <img :src="`https://image.tmdb.org/t/p/w500${movie.movie.poster_path}`" alt="Movie Poster">
        <h3>{{ movie.movie.title }}</h3>
        <button @click="goDetail(movie.movie)">상세페이지로 이동</button>
        <button @click="removeWish(movie.movie.id)">위시리스트 목록에서 삭제</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router'; 
const router = useRouter();

const { user, isOwnPage } = defineProps(['user', 'isOwnPage']);

const token = localStorage.getItem('token');

const likedMovies = ref(null);
const wishlistMovies = ref(null);

const fetchLikedMovies = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/accounts/users/${user.username}/likelist/`, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    likedMovies.value = response.data;
  } catch (error) {
    console.error('좋아요한 영화 목록을 가져오는 중 오류 발생:', error);
  }
};

const fetchWishlistMovies = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/accounts/users/${user.username}/wishlistlist/`, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    wishlistMovies.value = response.data;
  } catch (error) {
    console.error('위시리스트 영화 목록을 가져오는 중 오류 발생:', error);
  }
};

onMounted(() => {
  fetchLikedMovies();
  fetchWishlistMovies();
});

// 영화 상세 페이지로 이동하는 함수
// const goDetail = (movieId) => {
//   router.push({ name: 'MovieDetail', params: { id: movieId } });
// };
const goDetail = (movie) => {
  router.push(`/movie/${movie.id}`);
};


// 좋아요 목록에서 영화 삭제
const removeLike = async (movieId) => {
  try {
    await axios.post(`http://127.0.0.1:8000/api/v1/accounts/movies/${movieId}/like/`, {}, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    likedMovies.value = likedMovies.value.filter(movie => movie.movie.id !== movieId);
  } catch (error) {
    console.error('좋아요 목록에서 영화 삭제 중 오류 발생:', error);
  }
};

// 위시리스트 목록에서 영화 삭제
const removeWish = async (movieId) => {
  try {
    await axios.post(`http://127.0.0.1:8000/api/v1/accounts/movies/${movieId}/wishlist/`, {}, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });
    wishlistMovies.value = wishlistMovies.value.filter(movie => movie.movie.id !== movieId);
  } catch (error) {
    console.error('위시리스트 목록에서 영화 삭제 중 오류 발생:', error);
  }
};


</script>

<style scoped>
/* 여기에 컴포넌트에 필요한 CSS 스타일을 추가하세요 */
.likemovies {
  margin-top: 100px;
  margin-bottom: 100px;
}
.wishlist {
  margin-bottom: 100px;
}
.movie-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.movie-card {
  width: 200px;
}

.movie-card img {
  width: 100%;
  height: auto;
}

.no {
  color: gray;
  margin-top: 20px;
}
</style>

