<template>
    <div class="main">
  <!-- 년도 선택 -->
  <div class="dropdown-container animated-style">
  <p class="choosetime">떠나고 싶은 시대를 선택해주세요</p>
  <select v-model="selectedYear">
    <option disabled value="">click !</option>
    <option v-for="year in years" :key="year" :value="year">
      {{ year }}
    </option>
  </select>
</div>


  <!-- 'All' 버튼 -->
  
  <!-- 장르 선택 -->
  <div class="genre-selection">
    <p class="choosegenre">지금 끌리는 장르를 선택해주세요</p>
    <div class="select-all-container">
      <span @click="toggleSelectAll" class="select-all" :class="{'selectedall': selectAll}">
        <label>All</label>
      </span>
    </div>
    <div class="genres">
      <span v-for="genre in genres" :key="genre.name" @click="toggleGenre(genre.name)" class="genre-item" :class="{'selected': selectedGenre.includes(genre.name)}">
        {{ genre.name }}
      </span>
    </div>
  </div>

  <button class="btn" @click="sendRecommendation">NEXT</button>
</div>

  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import { useRouter } from 'vue-router'
  import axios from 'axios'
  import { useMovieStore } from '../stores/movies' 
  
  const router = useRouter()
  
  // 선택된 년도와 장르
  const selectedYear = ref('')
  const selectedGenre = ref([])
  const selectAll = ref(false)
  
  // 사용 가능한 년도와 장르 목록
  const years = ref(['1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s'])
  const genres = ref([
    { id: 12, name: '모험' },
    { id: 14, name: '판타지' },
    { id: 16, name: '애니메이션' },
    { id: 18, name: '드라마' },
    { id: 27, name: '공포' },
    { id: 28, name: '액션' },
    { id: 35, name: '코미디' },
    { id: 36, name: '역사' },
    { id: 37, name: '서부' },
    { id: 53, name: '스릴러' },
    { id: 80, name: '범죄' },
    { id: 99, name: '다큐멘터리' },
    { id: 878, name: 'SF' },
    { id: 9648, name: '미스터리' },
    { id: 10402, name: '음악' },
    { id: 10749, name: '로맨스' },
    { id: 10751, name: '가족' },
    { id: 10752, name: '전쟁' },
    { id: 10770, name: 'TV 영화' },
  ])
  

  // 추천을 저장할 데이터 속성
  // const recommendedMovies = ref([])
  // const recommendedHiddenMovies = ref([])
  
  const { setRecommendedMovies, setRecommendedHiddenMovies } = useMovieStore()
  
  // '전체' 선택/해제 처리
const handleSelectAll = () => {
  if (selectAll.value) {
    selectedGenre.value = genres.value.map(genre => genre.name)
  } else {
    selectedGenre.value = []
  }
}

// 개별 장르 체크박스 변경 시 '전체' 상태 업데이트
const handleGenreChange = () => {
  selectAll.value = selectedGenre.value.length === genres.value.length
}

// 장르 목록 변경 감시
watch(genres, () => {
  handleGenreChange()
})

  
  // 추천 요청 함수
  const sendRecommendation = async () => {
    try {
      // const genreParams = selectedGenre.value.join(',')
      const recommendResponse = await axios.get('http://127.0.0.1:8000/api/v1/movies/recommend/', {
        params: {
          year: selectedYear.value,
          genre: selectedGenre.value
        }
      })
      // console.log(selectedYear.value, selectedGenre.value)
  
      const recommendHiddenResponse = await axios.get('http://127.0.0.1:8000/api/v1/movies/recommend_hidden', {
        params: {
          year: selectedYear.value,
          genre: selectedGenre.value
        }
      })

      // 추천 데이터를 store에 저장
      setRecommendedMovies(recommendResponse.data)
      setRecommendedHiddenMovies(recommendHiddenResponse.data)
      // console.log(recommendResponse.data)

      // HomeView_Recommend.vue로 라우팅
      router.push('/HomeRecommend')
      
      // 받은 추천을 데이터 속성에 업데이트
      // recommendedMovies.value = recommendResponse.data
      // recommendedHiddenMovies.value = recommendHiddenResponse.data

    } catch (error) {
      console.error('추천 요청 에러:', error)
    }
  }

  const toggleGenre = (genreName) => {
    const index = selectedGenre.value.indexOf(genreName);
    if (index >= 0) {
      selectedGenre.value.splice(index, 1);
    } else {
      selectedGenre.value.push(genreName);
    }
    handleGenreChange();
  };

  const toggleSelectAll = () => {
    selectAll.value = !selectAll.value;
    handleSelectAll();
  }

  </script>
  
  <style scoped>
.animated-style select {
  appearance: none;
  background-color: transparent;
  padding: 35px 15px 35px 25px;
  border-radius: 99%;
  font-size: 32px;
  color: gray;
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
}

.animated-style select:hover {
  background-color: #f0f0f0;
  transform: scale(1.05); /* 호버 시 약간 확대 */
}

.main {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding-left: 300px;
  padding-right: 300px;
  padding-bottom: 150px;
}

@media (max-width: 600px) {
  .dropdown-container, .select-all-container, .genre-selection {
    margin-bottom: 20px;
  }
  .genres {
    flex-direction: column; /* 화면이 작을 때 장르 세로로 표시 */
  }
}

.dropdown-container, .select-all-container, .genre-selection {
  margin-bottom: 60px;
  margin-top: 60px;
}

.select-all {
  cursor: pointer;
  transition: background-color 0.3s;
  padding: 5px 10px;
  border-radius: 20px;
  border: 3px solid #ccc;
}

.genres {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
}

.choosetime {
  margin-bottom: 50px;
  color: gray;
}

.choosegenre {
  margin-bottom: 50px;
  color: gray;
}

.genre-item {
  margin: 5px;
  padding: 5px 10px;
  border-radius: 20px;
  border: 3px solid #ccc;
  cursor: pointer;
  transition: background-color 0.3s;
}

.genre-item:hover, .select-all:hover {
  background-color: #f0f0f0;
}

.selected {
  font-weight: bold;
  background-color: white;
  color: rgb(54, 54, 54);
}

.btn {
  padding: 10px 20px;
  background-color: rgb(54, 54, 54);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn:hover {
  background-color: white;
  color: rgb(54, 54, 54);
}
  </style>
  