<template>
  <div class="main">
    <ReviewCreateForm @createReview="createReview" />
    <br>
    <hr>
    <div v-if="reviews.length > 0">
      <ul>
        <li v-for="review in reviews" :key="review.id">
          <div class="review" v-if="!review.isEditing">
            
            <p>작성자: {{ review.user.username }}</p>
            <p>내용: {{ review.content }}</p>
            <p>평점: {{ review.rating }}</p>
            <div class="holebtn" v-if="review.isAuthor">
              <button type="button" class="btn" @click="toggleEditForm(review)">수정</button>
              <button type="button" class="btn" @click="deleteReview(review)">삭제</button>
            </div>  
          </div>
          <div v-else>
            
            <div class="review-form-container">

            <form @submit.prevent="updateReview(review)">
              <div class="mb-3">
                <label for="editedContent" class="form-label">내용 수정</label>
                <textarea class="form-control" id="editedContent" v-model="review.editedContent"></textarea>
              </div>
              <div class="mb-3">
                <label for="editedRating" class="form-label">평점 수정</label>
                <input type="number" class="form-control" id="editedRating" v-model="review.editedRating">
              </div>
              <button type="submit" class="btn">SAVE</button>
            </form>

            </div>

          </div>
          <br>
        </li>
      </ul>
    </div>
    <div class="noreview" v-if="reviews.length === 0">
      <p>리뷰가 없습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

import ReviewCreateForm from '@/components/ReviewCreateForm.vue'

const route = useRoute()
const reviews = ref([])
const movie_id = ref(null)
const userId = localStorage.getItem('username'); // 현재 사용자 ID를 localStorage에서 가져옴
console.log(userId)
// createReview 함수 정의
function createReview(reviewData) {
  // 로컬 스토리지에서 토큰 가져오기
  const token = localStorage.getItem('token')

  if (token) {
    // Axios를 사용하여 백엔드로 데이터를 전송
    axios
      .post(`http://127.0.0.1:8000/api/v1/movies/${movie_id.value}/reviews/`, reviewData, {
        headers: {
          'Authorization': `Token ${token}` // Django가 Token 기반 인증을 사용하는 경우
        }
      })
      .then(response => {
        // 리뷰 생성 후 처리
        console.log('Review created:', response.data)

        // 리뷰 목록을 다시 불러오는 메서드를 호출
        fetchReviews()
      })
      .catch(error => {
        console.error('Error creating review:', error)
      })
  } else {
    // 토큰이 없는 경우 처리
    console.error('Token not found. User is not authenticated.')
  }
}

// fetchReviews 함수 정의
function fetchReviews() {
  const token = localStorage.getItem('token');
  // movie_id 변수를 사용하여 영화 정보를 가져옴
  axios.get(`http://127.0.0.1:8000/api/v1/movies/${movie_id.value}/reviews/`, {
    headers: {
      'Authorization': `Token ${token}` // Django가 Token 기반 인증을 사용하는 경우
    }
  })
    .then(response => {
      reviews.value = response.data.map(review => ({
          ...review,
          isEditing: false,
          isAuthor: review.user.username === userId, // 현재 사용자가 작성자인지 확인
      }))
      console.log(reviews)

      // 리뷰 목록을 받아올 때 각 리뷰의 수정 상태 및 내용, 평점을 초기화합니다.
      for (const review of reviews.value) {
        review.isEditing = false
        review.editedContent = review.content
        review.editedRating = review.rating
      }
    })
    .catch(error => {
      console.error(error)
    })
}

// movie_id를 설정하는 로직 추가
onMounted(() => {
  movie_id.value = route.params.movie_id
  fetchReviews()
})

// 수정 폼을 토글하는 함수 정의
function toggleEditForm(review) {
  review.isEditing = !review.isEditing
}

// 리뷰를 업데이트하는 함수 정의
function updateReview(review) {
  const updatedData = {
    content: review.editedContent,
    rating: review.editedRating
  }

  axios
    .put(`http://127.0.0.1:8000/api/v1/movies/reviews/${review.id}/`, updatedData, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
    })
    .then(response => {
      console.log('Review updated:', response.data)
      // 업데이트가 성공하면 수정 폼을 닫습니다.
      review.isEditing = false
      // 리뷰 목록을 다시 불러오는 메서드를 호출
      fetchReviews()
    })
    .catch(error => {
      console.error('Error updating review:', error)
    })
}

// 리뷰를 삭제하는 함수 정의
function deleteReview(review) {
  axios
    .delete(`http://127.0.0.1:8000/api/v1/movies/reviews/${review.id}/`, {
      headers: {
        'Authorization': `Token ${localStorage.getItem('token')}`,
      },
    })
    .then(response => {
      console.log('Review deleted:', response.data)
      fetchReviews()
    })
    .catch(error => {
      console.error('Error deleting review:', error)
    })
}
</script>


<style scoped>

.main {
  min-height: 100vh; /* 최소 높이를 유지하면서 내용에 따라 늘어날 수 있음 */
  background-color: rgb(54, 54, 54);
  padding: 70px;
}

.main li {
  list-style-type: none;
}

.main ul {
  margin-left: auto;
  margin-right: auto;
  padding-top: 20px;
  padding-left: 0px;
  width: fit-content; /* 혹은 고정 너비 */
}


.noreview {
  padding-top: 30px;
  color: rgba(128, 128, 128, 0.623);
}

button {
  border: 3px solid white;
  padding-top: 0;
  border-radius: 10px;
}

.holebtn {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding-top: 10px;
}

.review {
  margin-top: 20px;
}

.btn {
  color: white;
  padding-top: 6px;
}


.review-form-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

</style>