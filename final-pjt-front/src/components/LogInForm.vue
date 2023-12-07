<template>
  <div :id="formId" class="auth">
    <h1 class="auth-title">LOGIN</h1>
    <form class="auth-form" @submit.prevent="logIn">
      <input class="auth-form-input" placeholder="Username" type="text" v-model="username">
      <div class="auth-password">
        <label for="password"></label>
        <input class="auth-form-input" placeholder="Password" type="password" id="password" v-model="password" required>
      </div>
      <input type="submit" class="auth-form-submit" value="Press Enter">
      <!-- <div class="auth-password">
        <input class="auth-form-input" placeholder="Password" :type="formState.passwordShow ? 'text' : 'password'" v-model="formState.password">
      </div> -->
      <!-- <div class="check-word" v-if="failedLogin">
        <span class="info-red">입력 정보를 다시 확인해주세요.</span>
      </div>
      <div @click="logIn" class="auth-form-submit">Press Enter</div> -->
      <div @click="$emit('moveToSignup')" class="auth-form-submit">아직 회원이 아니신가요?</div>
    </form>
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const store = useAuthStore()

const username = ref('')
const password = ref('')
const failedLogin = false

const formId = 'login-form' // Unique ID for LogInForm
const formRef = ref(null)

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}

onMounted(() => {
  // Get the height of the LogInForm after it's mounted
  const formElement = document.getElementById(formId)
  if (formElement) {
    formRef.value = formElement.clientHeight
  }
})
</script>

<style scoped>
@import "./AuthForm.css";
</style>