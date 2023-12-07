import axios from 'axios'
import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useMovieStore = defineStore('movie', () => {
  const movieList = ref([])
  const recommendedMovies = ref([])
  const recommendedHiddenMovies = ref([])
  
  const getMovieList = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/api/v1/movies/'
    })
    .then(res => movieList.value = res.data)
    .catch(err => console.log(err))
  }

  const detailMovie = ref([])

  const getDetailMovie = function (pk) {
    axios({
      method: 'get',
      url: `http://127.0.0.1:8000/api/v1/movies/${pk}/`
    })
    .then(res => detailMovie.value = res.data)
    .catch(err => console.log(err))
  }

  // const getRecommendations = async (year, genre) => {
  //   try {
  //     const response = await axios.get('http://127.0.0.1:8000/api/v1/movies/recommend/', {
  //       params: { year, genre }
  //     })
  //     recommendedMovies.value = response.data

  //     const hiddenResponse = await axios.get('http://127.0.0.1:8000/api/v1/movies/recommend_hidden', {
  //       params: { year, genre }
  //     })
  //     recommendedHiddenMovies.value = hiddenResponse.data
  //   } catch (error) {
  //     console.error('Error fetching recommendations:', error)
  //   }
  // }
  const initRecommendedMovies = () => {
    const storedMovies = localStorage.getItem('recommendedMovies');
    if (storedMovies) {
      recommendedMovies.value = JSON.parse(storedMovies);
    }

    const storedHiddenMovies = localStorage.getItem('recommendedHiddenMovies');
    if (storedHiddenMovies) {
      recommendedHiddenMovies.value = JSON.parse(storedHiddenMovies);
    }
  }

  // 추천된 영화 목록을 설정하고 로컬 스토리지에 저장합니다.
  const setRecommendedMovies = (movies) => {
    recommendedMovies.value = movies;
    localStorage.setItem('recommendedMovies', JSON.stringify(movies));
  }

  const setRecommendedHiddenMovies = (movies) => {
    recommendedHiddenMovies.value = movies;
    localStorage.setItem('recommendedHiddenMovies', JSON.stringify(movies));
  }

  // 스토어가 생성될 때 초기화 함수를 호출합니다.
  initRecommendedMovies();

  return { movieList, getMovieList, detailMovie, getDetailMovie, recommendedMovies, recommendedHiddenMovies, setRecommendedMovies, setRecommendedHiddenMovies }
})

