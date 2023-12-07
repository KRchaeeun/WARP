<template>
  <div class="signup">
    <h1>SignUp</h1>
      <form class="signup-form" @submit.prevent="signUp">
          <input class="signup-form-input" placeholder="Username" type="text" v-model="username">
        <div class="signup-password">
          <label for="password1"></label>
          <input class="signup-form-input" placeholder="Password" type="password" id="password1" v-model="password1" required>
        </div>
        <div class="signup-password">
          <label for="password2"></label>
          <input class="signup-form-input" placeholder="Password Confirm" type="password" id="password2" v-model="password2" required>
        </div>
        <input type="submit" class="auth-form-submit" value="Press Enter">
        <div @click="$emit('moveToLogin')" class="signup-form-submit">이미 회원이신가요?</div>
      </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {useAuthStore} from '@/stores/auth'

const store = useAuthStore()
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}

defineProps({
  formType: String
})
</script>



<style scoped>
@import "./AuthForm.css";
</style>
