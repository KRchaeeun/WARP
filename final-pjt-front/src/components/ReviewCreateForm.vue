<template>
  <div>
    <h3 class="text-margin">REVIEW</h3>
    <br>
    <form @submit.prevent="submitReview">
      <div>
        <label for="content" ></label>
        <textarea v-model="newReview.content" id="content" required class="content-size"></textarea>
      </div>
      <div class="rating-margin">
        <label for="rating"></label>
        <rating-star ref="starRating" :movie-data="newReview" @ratingSelected="handleRatingSelected"/>
        <!-- <input v-model="newReview.rating" id="rating" type="number" min="0" max="5" required> -->
      </div>
      <button type="submit">CREATE</button>
    </form>
  </div>
</template>

<script>
import RatingStar from "./RatingStar.vue"

export default {
  components: {
    'rating-star': RatingStar // 컴포넌트 등록
  },
  data() {
    return {
      newReview: {
        content: '',
        rating: 0,
      },
    };
  },
  methods: {
    handleRatingSelected(rating) {
      this.newReview.rating = rating;
    },
    submitReview() {
      // 사용자가 작성한 리뷰 데이터를 부모 컴포넌트로 전달
      this.$emit('createReview', this.newReview);

      // 리뷰 작성 후 입력된 내용 초기화
      this.newReview.content = '';
      this.newReview.rating = 0;
      // 리뷰 생성 후 별점 초기화
      this.$refs.starRating.resetRating()
    },
  },
};
</script>

<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Fugaz+One&display=swap');

h3 {
  font-family: 'Fugaz One', sans-serif !important;
  font-size: 30px;
  color: white !important;

  /* 드래그 방지 */
  -webkit-user-select:none;
  -moz-user-select:none;
  -ms-user-select:none;
  user-select:none;
}

button {
  padding-top: 0px;
  border: 3px solid white;
  border-radius: 10px;
  margin-top: 20px;
}

.content-size {
  width: 400px; 
  height: 50px;
}

.text-margin {
  margin-bottom: 0px;
}

.rating-margin {
  margin-top: 10px;
}
</style>