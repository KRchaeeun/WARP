<template>
    <div class="main">
        <div class="image-text-overlay">
            <img alt="logo" class="img-logo" src="@/assets/logo_Edited_word.png" />
            <span id="typed-strings"></span>
        </div>

        <div class="container">
            <div class="form-container">
                <LogInForm v-if="showLoginForm" formType="login" @moveToSignup="toggleForm"/>
                <div v-if="!showLoginForm" class="hidden-form"></div>
            </div>
            <div class="form-container">
                <div v-if="showLoginForm" class="hidden-form"></div>
                <SignUpForm v-show="!showLoginForm" formType="signup" @moveToLogin="toggleForm"/>
            </div>
            <h3>기능설명</h3><br>
            <div class="description">
                <p class="title">맞춤형 빠른 추천</p>
                <p>약 1500개의 영화 데이터베이스를 바탕으로 정밀한 취향 분석 진행</p>                
            </div>
            <div class="description">
                <p class="title">숨겨진 명작</p>
                <p>평점이 좋지만 숨겨져있었던 명작 소개</p>
            </div>
            <div class="description">
                <p class="title">간편한 검색</p>
                <p>검색을 통한 영화 선택 가능</p>
            </div>
            <h3>자주 묻는 질문</h3><br>
            <div class="question">
                <p class="title"><strong>warp</strong>란 무엇인가요?</p>
                <p>WARP는 속도와 정확성을 갖춘 영화 추천 서비스입니다. <br>
                    즉, 사용자가 원하는 영화를 신속하고 정확하게 찾을 수 있도록 설계된 영화 추천 서비스입니다.
                    마치 우주선이 워프 드라이브를 사용하여 먼 거리를 순식간에 이동하는 것처럼, 사용자가 원하는 영화를 빠르게 찾아주는 것을 목표로 합니다. 
                    이러한 서비스를 통해 영화 선택의 고민을 최소화하고, 보다 만족스러운 시청 경험을 제공합니다.
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';
import Typed from 'typed.js'
import LogInForm from '@/components/LogInForm.vue'
import SignUpForm from '@/components/SignUpForm.vue'

const showLoginForm = ref(true)

const toggleForm = () => {
    showLoginForm.value = !showLoginForm.value
}

onMounted(() => {
    new Typed('#typed-strings', {
        strings: ['Time <strong>WARP</strong>', 'Movie <strong>WARP</strong>', 'Space <strong>WARP</strong>'],
        typeSpeed: 50,
        backSpeed: 25,
        fadeOut: true,
        loop: true,
        showCursor: false // 커서를 숨깁니다
    });
});
</script>

<style scoped>

h1 {
    color: white;
    padding-top: 20%;
}

.container {
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.forms {
    display: flex;
    justify-content: center;
    margin-bottom: 30px;
    gap: 50px;
}

h3 {
    margin-top: 50px;
}
/* 기능 설명 섹션 *//* 기능 설명 및 FAQ 섹션 공통 스타일 */
.description, .question {
    border: 1px solid #362727; /* 테두리 색상과 두께 */
    padding: 20px; /* 내부 여백 */
    margin-bottom: 30px; /* 섹션 사이의 여백 */
    border-radius: 10px; /* 모서리 둥글게 */
    background-color: #f9f9f92c; /* 배경색 */
    width: 80%; /* 너비 */
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); /* 그림자 효과 */
}

/* 기능 설명 섹션 */
.title {
    font-weight: bold;
    margin-bottom: 10px;
    font-size: 1.2em;
}

.description p {
    margin-bottom: 20px;
    font-size: 1em;
}

/* 자주 묻는 질문(FAQ) 섹션 */
.question .title {
    font-weight: bold;
    margin-bottom: 10px;
    font-size: 1.2em;
}

.question p {
    margin-bottom: 30px;
    font-size: 1em;
    line-height: 1.5;
}


.logo-container {
  margin-right: 10px;
}

.img-logo {
  width: 300px; /* Set the width to make the image three times larger */
  height: auto;
  
}

.text-container {
  color: white;
  font-size: 50px; /* Adjust the font size as needed */

}

.image-text-overlay {
    position: relative;
    display: inline-block;
    margin-right: 130px; /* 오른쪽으로 20px 마진 추가 */
}

.img-logo {
    display: block; /* 이미지가 블록 요소로 표시되도록 설정 */
    width: 100%; /* 이미지 크기 설정 */
    height: auto; /* 이미지 비율 유지 */
}

#typed-strings {
    position: absolute; /* 절대 위치 설정으로 이미지 위에 표시 */
    top: 50%; /* 상위 컨테이너 기준으로 상단에서부터 50% 위치 */
    left: 50%; /* 상위 컨테이너 기준으로 왼쪽에서부터 50% 위치 */
    transform: translate(-80%, -50%); /* 요소의 중앙이 상위 컨테이너의 정중앙에 위치하도록 조정 */
    color: white; 
    font-size: 45px;
}

</style>
