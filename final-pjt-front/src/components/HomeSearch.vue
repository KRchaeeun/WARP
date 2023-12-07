<template>
  <div>
    <!-- 모달 -->
    <div v-show="modalActive" id="search-modal-search">
      <button @click="modalActiveTogle">닫기</button>
      <div id="search-modal-search-box">
        <img src="@/assets/star.png" alt="">
        <input 
        type="text" 
        @keyup="searchInput" 
        @keyup.esc="modalActiveTogle" 
        placeholder="SEARCH" 
        id="search-modal-search--input">
      </div>
      <div id="search-modal-search-result">
        <home-search-result 
        :search-input-data="searchInputData"
        @close-modal="modalActiveTogle"/>
      </div>
      <!-- <div v-show="modalActive" @click="modalActiveTogle" id="search-modal"></div> -->
    </div>
    <!-- 모달 배경 -->
    <div v-if="modalActive" @click="modalActiveTogle" id="search-modal-bg"></div>

      <!-- 홈화면에 보이는 검색창 -->
      <div id="home-search">
      <div id="home-search-box">
        <!-- 검색창은 비활성화 -->
        <img src="@/assets/star.png" alt="">
        <input @click="modalActiveTogle" placeholder="SEARCH" type="text" id="search--input" readonly>
      </div>
    </div>
  </div>
</template>

<script setup>
import HomeSearchResult from '@/components/HomeSearchResult.vue'
import { ref } from 'vue'

const modalActive = ref(false)
const ableSearch = ref(true)
const searchInputData = ref(null)

const modalActiveTogle = () => {
  modalActive.value = !modalActive.value
  setTimeout(() => {
    const searchModalInputTag = document.querySelector('#search-modal-search--input')
    searchModalInputTag.focus()
  }, 200)
}

const searchInput = () => {
  if (ableSearch.value) {
    ableSearch.value = false
    const searchModalInputTag = document.querySelector('#search-modal-search--input')
    setTimeout(() => {
      searchInputData.value = searchModalInputTag.value
      ableSearch.value = true
    }, 1000)
  }
}


</script>

<style scoped>
.modal {
  overflow-y: auto;
  max-height: 100%;
}

/* 홈화면에서의 서치 요소(작동 안하고, 모달을 띄우는데만 사용) */
#home-search {
  display: flex;
  justify-content: center;
  margin-bottom: 80px;
}

#home-search-box input {
  font-family: 'NanumSquareNeo-Variable';
  outline: none;
  border: none;
  border-bottom: white solid;
  background-color: #ffffff00;
  color: white;
}

#home-search-box input:hover {
  border-bottom: gray solid;
  transition: all 0.2s;
  transform: scale(1.03);
}

#home-search-box img {
  width: 35px;
  margin-right: 10px;
}

/* 서치용 모달 내부 요소 */
#search-modal {
  z-index: 10;
  position: fixed;
  top: 0px;
  width: 100vw;
  height: 100vw;
}

#search-modal-search {
  z-index: 20;
  width: 100%;
  position: fixed;
  top: 30px;
  display: flex;
  align-items: center;
  flex-direction: column;
  flex-wrap: nowrap;
}

#search-modal-search-box {
  z-index: 30;
  margin-top: 50px;
}

#search-modal-search-box input {
  font-family: 'NanumSquareNeo-Variable';
  outline: none;
  border: none;
  border-bottom: white solid;
  background-color: #ffffff00;
  color: white;
}

#search-modal-search-box input:hover {
  transition: all 0.2s;
  transform: scale(1.03);
}

#search-modal-search-box img {
  width: 35px;
  margin-right: 10px;
}

#search-modal-result {
  width: 100%;
  max-width: 900px;
  z-index: 30;
}

/* 배경 애니메이션 */
#search-modal-bg {
  z-index: 10;
  position: fixed;
  top: 0px;
  width: 100%;
  height: 100%;
  background-color: #222222b0;
  backdrop-filter: blur(20px);
}

button {
  color: rgba(116, 116, 116, 0);
}
/* Keyframes for fade-in animation */
@-webkit-keyframes fade-in {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

@keyframes fade-in {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>