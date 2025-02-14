import { defineStore } from 'pinia'
import RequestService from '@/api'

const TOKEN_KEY = 'access_token'
const REFRESH_TOKEN = 'refresh_token'

const useAuthStore = defineStore('auth', {
  state: () => ({
    logged: !!localStorage.getItem(TOKEN_KEY),
    token: localStorage.getItem(TOKEN_KEY),
    isRefresh: false,
  }),
  getters: {
    logined: (state) => {
      return state.logged
    },
  },
  actions: {
    logout () {
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(REFRESH_TOKEN)
      this.logged = false
    },
    async login (data) {
      let result = await RequestService.sendRest(
        {
          method: 'post',
          url: '/users/auth',
          data: data,
        })
      localStorage.setItem(TOKEN_KEY, result.data.access_token)
      localStorage.setItem(REFRESH_TOKEN, result.data.refresh_token)
      this.logged = true
    },
  },
})

export default useAuthStore
