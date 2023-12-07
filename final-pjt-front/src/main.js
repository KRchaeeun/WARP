// import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'animate.css'


// BootstrapVue 3
import BootstrapVue3 from 'bootstrap-vue-3'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-3/dist/bootstrap-vue-3.css'

const app = createApp(App)

// BootstrapVue 3 사용

app.use(BootstrapVue3)
app.use(createPinia())  // Pinia 스토어 초기화
app.use(router)

app.mount('#app')