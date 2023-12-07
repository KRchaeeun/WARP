<template>
    <div>
        <h1>검색 결과</h1>
        <ul v-if="movies.length > 0">
            <li v-for="movie in movies" :key="movie.id">
                <img :src="getImageUrl(movie.poster_path)" alt="Movie Poster">
                {{ movie.title }}
            </li>
        </ul>
        <p v-else>검색 결과가 없습니다.</p>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const searchQuery = ref('')
const movies = ref([])

const TMDB_API_KEY = '5c95202746685cd5450538f7aa718f76'
const TMDB_BASE_URL = 'https://api.themoviedb.org/3'
const TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

const fetchMovies = async () => {
    try {
        const response = await axios.get(`${TMDB_BASE_URL}/search/movie`, {
            params: {
                api_key: TMDB_API_KEY,
                query: searchQuery.value
            }
        })
        movies.value = response.data.results
    } catch (error) {
        console.error('영화 검색 중 오류 발생:', error)
        // 오류 처리 로직
    }
}

const getImageUrl = (path) => {
    return `${TMDB_IMAGE_BASE_URL}${path}`;
}

onMounted(() => {
    searchQuery.value = route.query.q
    fetchMovies()
})
</script>
