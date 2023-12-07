import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { useRouter } from 'vue-router'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const posts = ref([])
  // const username = ref('') // username 추가
  const username = ref(localStorage.getItem('username') || '')
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(localStorage.getItem('token') || null)
  const isAuthenticated = computed(() => !!token.value)

  const getPosts = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/'`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
    .then((res) =>{
      posts.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }
  
  // 회원가입 axios 요청을 보낼 수 있는 actions
  const signUp = function (payload) {
    const { username, password1, password2 } = payload
  
    console.log('Sending request with payload:', payload)

    axios({
      method: 'post',
      url: `${API_URL}/api/v1/accounts/signup/`,
      headers: {
        'Content-Type': 'application/json'  // 콘텐츠 타입 명시적으로 설정
      },
      data: JSON.stringify({  // 데이터를 JSON 형식으로 변환
        username, password1, password2
      })
    })
    .then((res) => {
      console.log(res)
      const password = password1
      logIn({ username, password })
    })
    .catch((err) => {
      console.error('Error:', err)
    })
  }

  // 로그인 axios 요청을 보낼 수 있는 actions
  const logIn = function (payload) {
    const { username: newUsername, password } = payload

    axios({
      method: 'post',
      url: `${API_URL}/api/v1/accounts/login/`,
      data: {
        username: newUsername, password
      }
    })
      .then((res) => {
        // console.log(res.data)
        token.value = res.data.key
        username.value = newUsername
        localStorage.setItem('token', token.value)
        localStorage.setItem('username', newUsername)
        router.push({ name: 'Recommendation' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  const logOut = function () {
    token.value = null
    // username.value = '' // 로그아웃 시 username 제거
    localStorage.removeItem('token')
    // localStorage.removeItem('username')
    router.push({ name: 'Intro' })
  }

  return { posts, API_URL, getPosts, signUp, logIn, logOut, token, username, isAuthenticated }
}, { persist: true })