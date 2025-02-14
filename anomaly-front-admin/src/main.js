import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createVuestic } from 'vuestic-ui'
import 'vuestic-ui/css'

import 'material-design-icons-iconfont/dist/material-design-icons.min.css'
import { createPinia } from 'pinia'

const pinia = createPinia()
createApp(App).use(createVuestic()).use(router).use(pinia).mount('#app')
