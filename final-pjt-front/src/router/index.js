import { createRouter, createWebHistory } from 'vue-router'
import IntroView from '@/views/IntroView.vue'  // 로그인/회원가입 전 인트로 페이지
import MovieDetailView from '@/views/MovieDetailView.vue'  // 영화 상세 페이지
import RecommendationView from '@/views/RecommendationView.vue'  // 영화 추천 페이지
import CommunityView from '@/views/CommunityView.vue'  // 커뮤니티 전체 목록 게시판
import CommunityDetailView from '@/views/CommunityDetailView.vue'  // 게시판 상세 페이지
import MyPageView from '@/views/MyPageView.vue'  // 마이페이지(프로필)
import SearchView from '@/views/SearchView.vue'  // 영화 검색 페이지
import HomeRecommendView from '@/views/HomeRecommendView.vue' // 추천된 영화
import LogInForm from '@/components/LogInForm.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'LoginForm', // name 속성은 moveToLogin 메소드에서 사용된 이름과 일치해야 합니다.
      component: LogInForm // LoginForm 컴포넌트가 있다고 가정
    },
    {
      // 로그인/회원가입 전 인트로 페이지
      path: '/',
      name: 'Intro',
      component: IntroView
    },
    {
      // 영화 상세 페이지
      path: '/movie/:movie_id',
      name: 'MovieDetail',
      component: MovieDetailView
    },
    {
      // 영화 추천 페이지
      path: '/recommendation',
      name: 'Recommendation',
      component: RecommendationView
    },
    {
      // 커뮤니티 전체 목록 게시판
      path: '/community',
      name: 'Community',
      component: CommunityView
    },
    {
      path: '/community/:community_id',
      name: 'CommunityDetail',
      component: CommunityDetailView
    },
    // {
    //   // 마이페이지(프로필)
    //   path: '/mypage',
    //   name: 'MyPage',
    //   component: MyPageView,
    //   props: true
    // },
    {
      // 마이페이지(프로필)
      path: '/mypage/:username',
      name: 'MyPage',
      component: MyPageView,
    },
    {
      // 영화 검색 페이지
      path: '/search',
      name: 'Search',
      component: SearchView
    },
    {
      // 추천 받은 영화 페이지(홈)
      path: '/HomeRecommend',
      name: 'HomeRecommend',
      component: HomeRecommendView
    },
  ]
})

export default router
