<!-- 로그인/회원가입 후 메인페이지: 로그인/회원가입할 때마다 새롭게 추천해주기 + "모달창으로 로그아웃 시 다시 로그인했을 때 새롭게 추천해드립니다"를 띄워주고 + 다시 보지 않기 기능 -->
<template>
    <div class="main">
        
        <!-- 현재 선택된 영화의 이미지를 표시하는 캐러셀 -->
        <!-- <div class="carousel">
            <img :src="currentMovieBackdrop" class="carouselimg">
            <div class="arrow">
                <p @click="prevMovie" class="material-symbols-outlined">arrow_back_ios</p>
                <p @click="nextMovie" class="material-symbols-outlined">arrow_forward_ios</p>
            </div>
        </div> -->
        <div class="trailer-container">
            <span @click="prevTrailer" class="material-symbols-outlined">
                arrow_back_ios
            </span>
            <iframe v-if="currentTrailerKey"
                    width="80%" 
                    height="400px" 
                    :src="`https://www.youtube.com/embed/${trailerKeys[currentTrailerIndex]}?autoplay=1&mute=1`" 
                    frameborder="0" 
                    allow="autoplay; encrypted-media" 
                    allowfullscreen>
            </iframe>
            <span @click="nextTrailer" class="material-symbols-outlined">
                arrow_forward_ios
            </span>
        </div>


        <br><h2 class="title1"><strong>{{ username }}</strong> 님을 위한 <strong>명작</strong> 추천</h2><br><br>
        <div class="movie-list">
            <div v-for="movie in detailedMovies" :key="movie.id" class="movie-card">
                <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`">
                <strong>
                    <button @click="goDetail(movie)">{{ movie.title }}</button>
                </strong>
            </div>
        </div>
        <br><br><br><br><br><br>
        

        <!-- 숨겨진 추천 영화 -->
        
        <h2><strong>{{ username }}</strong> 님을 위한 <strong>숨겨진 명작 추천</strong></h2><br><br>

        <div class="movie-list">
            <div v-for="movie in detailedHiddenMovies" :key="movie.id" class="movie-card">
                <img :src="`https://image.tmdb.org/t/p/w500${movie.poster_path}`">
                <strong>
                    <button @click="goDetail(movie)">{{ movie.title }}</button>
                </strong>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

import { useMovieStore } from '../stores/movies' // 경로는 프로젝트 구조에 따라 다를 수 있음
import { useAuthStore } from '@/stores/auth'
const { recommendedMovies, recommendedHiddenMovies } = useMovieStore()
console.log(recommendedMovies, recommendedHiddenMovies)
const detailedMovies = ref([])
const detailedHiddenMovies = ref([])
const store = useAuthStore()
const username = store.username

// 캐러셀을 위한 현재 영화 인덱스 및 이미지 경로
// const currentMovieIndex = ref(0)
// const currentMovieBackdrop = ref('')
const currentTrailerKey = ref('')

// getRecommendations('2020s', '드라마')


// const fetchMovieBackdrop = async (movieId) => {
//   const apiKey = '5c95202746685cd5450538f7aa718f76'; // TMDB API 키
//   const url = `https://api.themoviedb.org/3/movie/${movieId}?api_key=${apiKey}`;

//   try {
//     const response = await axios.get(url);
//     return response.data.backdrop_path;
//   } catch (error) {
//     console.error('Error fetching movie backdrop:', error);
//     return null;
//   }
// }

const fetchMovieDetails = async (movieId) => {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/api/v1/movies/list/${movieId}`);
        const movieData = response.data;

        // TMDB API를 사용하여 백드롭 이미지 가져오기
        // const backdropPath = await fetchMovieBackdrop(movieId);
        // movieData.backdrop_path = backdropPath;

        return movieData;
    } catch (error) {
        console.error('Error fetching movie details:', error);
        return null;
    }
}


onMounted(async () => {
  detailedMovies.value = await Promise.all(recommendedMovies.map(movie => fetchMovieDetails(movie.id)))
  detailedHiddenMovies.value = await Promise.all(recommendedHiddenMovies.map(movie => fetchMovieDetails(movie.id)))

//   // 캐러셀에 사용할 첫 번째 영화의 backdrop_path 설정
//     // 첫 번째 영화의 백드롭 이미지 설정
//     if (detailedMovies.value.length > 0 && detailedMovies.value[0].backdrop_path) {
//         currentMovieBackdrop.value = `https://image.tmdb.org/t/p/original/${detailedMovies.value[0].backdrop_path}`;
//     }
    // 첫 번째 영화의 트레일러 가져오기
    if (detailedMovies.value.length > 0) {
        const trailerKey = await fetchMovieTrailer(detailedMovies.value[0].id);
        if (trailerKey) {
            currentTrailerKey.value = trailerKey;
        }
    }
})

const router = useRouter()
// const movies = ref([])
// const API_URL = 'http://127.0.0.1:8000/api/v1/movies' // Django 서버의 URL 주소


// axios.get(API_URL)
//   .then(response => {
//     movies.value = response.data
//     console.log(movies.value)
//   })
//   .catch(err => console.error(err))

// const movieIsEmpty = computed(() => {
//     return movies.value.length > 0 ? true : false
// })

const goDetail = (movie) => {
    router.push(`/movie/${movie.id}`)
}


// const updateCarouselImage = () => {
//     const totalMovies = detailedMovies.value.length + detailedHiddenMovies.value.length;

//     if (currentMovieIndex.value < detailedMovies.value.length) {
//         currentMovieBackdrop.value = `https://image.tmdb.org/t/p/original/${detailedMovies.value[currentMovieIndex.value].backdrop_path}`;
//     } else if (currentMovieIndex.value - detailedMovies.value.length < detailedHiddenMovies.value.length) {
//         currentMovieBackdrop.value = `https://image.tmdb.org/t/p/original/${detailedHiddenMovies.value[currentMovieIndex.value - detailedMovies.value.length].backdrop_path}`;
//     }
// };


// // 케러셀
// const prevMovie = () => {
//     const totalMovies = detailedMovies.value.length + detailedHiddenMovies.value.length;

//     if (currentMovieIndex.value > 0) {
//         currentMovieIndex.value -= 1;
//     } else {
//         currentMovieIndex.value = totalMovies - 1; // 마지막 영화로 이동
//     }
//     updateCarouselImage();
// };

// // 케러셀
// const nextMovie = () => {
//     const totalMovies = detailedMovies.value.length + detailedHiddenMovies.value.length;

//     if (currentMovieIndex.value < totalMovies - 1) {
//         currentMovieIndex.value += 1;
//     } else {
//         currentMovieIndex.value = 0; // 첫 번째 영화로 이동
//     }
//     updateCarouselImage();
// };

const trailerKeys = ref([]) // 트레일러 키를 저장하는 배열
const currentTrailerIndex = ref(0) // 현재 표시되는 트레일러의 인덱스

// 추천된 영화의 트레일러 키를 가져오는 함수
const fetchAllTrailers = async () => {
  for (let movie of recommendedMovies) {
    const trailerKey = await fetchMovieTrailer(movie.id);
    if (trailerKey) {
      trailerKeys.value.push(trailerKey);
    }
  }
}

// 컴포넌트가 마운트될 때 모든 트레일러 키를 가져옵니다.
onMounted(fetchAllTrailers);

const fetchMovieTrailer = async (movieId) => {
  const apiKey = 'Your API Key'; // TMDB API 키
  const url = `https://api.themoviedb.org/3/movie/${movieId}/videos?api_key=${apiKey}`;

  try {
    const response = await axios.get(url);
    const trailers = response.data.results.filter(video => video.site === 'YouTube' && video.type === 'Trailer');
    return trailers.length > 0 ? trailers[0].key : null;
  } catch (error) {
    console.error('Error fetching movie trailer:', error);
    return null;
  }
}

const prevTrailer = () => {
    if (currentTrailerIndex.value > 0) {
        currentTrailerIndex.value--;
    } else {
        currentTrailerIndex.value = trailerKeys.value.length - 1;
    }
}

const nextTrailer = () => {
    if (currentTrailerIndex.value < trailerKeys.value.length - 1) {
        currentTrailerIndex.value++;
    } else {
        currentTrailerIndex.value = 0;
    }
}
</script>



<style>

.title1 {
    padding-top: 40px;
}

.carousel {
    position: relative;
    margin-bottom: 20px;
    overflow: hidden; /* 화면을 넘어가는 이미지를 숨김 처리 */
}

.carousel img {
    width: 90vw; /* 이미지의 너비를 뷰포트의 100%로 설정 */
    height: 50vh; /* 이미지의 높이를 뷰포트의 100%로 설정 */
    object-fit: cover; /* 이미지가 비율을 유지하면서 요소에 완전히 채워지도록 설정 */
    object-position: center; /* 이미지가 요소의 중앙에 위치하도록 설정 */
    border-radius: 3%;
    margin-right: 30px;
    margin-left: 0px;
    margin-bottom: 55px;
}


.arrow {
  position: absolute;
  top: 46%;
  width: 97%;
  margin-left: 5px;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
}

.material-symbols-outlined {
  cursor: pointer;
  padding: 10px;
  color: white;
  font-size: 24px; /* 아이콘 크기 조절 */
}


.main {
    width: 100vw;
    min-height: 100vh;
    background-color: rgb(54, 54, 54);
    text-align: center;
    color: white;
    padding-left: 3%;
    padding-right: 3%;
    padding-bottom: 50px;
}

.movie-list {
    display: flex;
    flex-wrap: wrap;
    gap: 40px 20px;
    justify-content: center;
}

.movie-card {
    width: 200px;
}

.movie-card:hover {
    transform: scale(1.07);
}

.movie-card img {
    width: 200px;
    height: 300px;
    object-fit: fill;
    border-radius: 10%;
    box-shadow: 20px 20px 40px 20px rgb(43, 43, 43);
}

button {
    border: 0;
    background-color: transparent;
    color: white;
    padding-top: 20px;
}

.movebtn {
    top: 55px;
    background-color: transparent;
}

iframe {
  width: 80%;
  height: auto;
  aspect-ratio: 16 / 9; /* 16:9 비율 */
  object-fit: cover; /* 영상이 프레임을 가득 채우도록 설정 */
}

.trailer-container {
    display: flex; /* Flexbox 레이아웃 사용 */
    align-items: center; /* 세로 방향으로 중앙 정렬 */
    justify-content: center; /* 가로 방향으로 중앙 정렬 */
}

.material-symbols-outlined {
    font-size: 36px; /* 기본 아이콘 크기 */
    cursor: pointer; /* 마우스 오버 시 커서 변경 */
    margin: 0 10px; /* 양쪽 아이콘 간격 조절 */
    transition: transform 0.3s ease, opacity 0.3s ease; /* 효과 전환 */
}

.material-symbols-outlined:hover {
    transform: scale(1.1); /* 마우스 오버 시 크기 10% 증가 */
    opacity: 0.7; /* 마우스 오버 시 투명도 조정 */
}

</style>