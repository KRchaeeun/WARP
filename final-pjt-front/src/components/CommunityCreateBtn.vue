<!-- 게시글 작성 버튼 -->
<template>
  <button @click="showCreateModal">게시글 작성</button>
  <!-- <div v-if="modalActive" @click="modalActiveTogle" id="search-modal-bg"></div> -->
</template>
  
<script setup>
import { ref, defineEmits } from 'vue'

// 모달 상태를 관리하는 ref
const isCreateModalVisible = ref(false)

// 이벤트 정의
const emit = defineEmits(['toggleCreateModal'])

// 버튼 클릭 시 모달 표시 함수
function showCreateModal() {
  isCreateModalVisible.value = true
  emit('toggleCreateModal', isCreateModalVisible.value)
}
</script>
  
<style scoped>

</style>