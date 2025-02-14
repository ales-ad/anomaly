import { defineStore } from 'pinia'
import RequestService from '@/api'

const usersStore = defineStore('users', {
  state: () => ({
    items: [],
    currentUser: {},
    total: 0,
    role: [
      'admin', 'moderator',
    ],
  }),
  getters: {},
  actions: {
    async getList (param) {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/users/list',
        params: param,
      })

      this.total = result.data.total
      this.items = result.data.items
      return result
    },
    async getMy () {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/users/my',
      })
      this.currentUser = result.data
    },
    async update (user_id, data) {
      const result = await RequestService.sendRest({
        method: 'put',
        url: '/users/' + user_id,
        data: data,
      })

      return result
    },
    async patch (user_id, data) {
      const result = await RequestService.sendRest({
        method: 'patch',
        url: '/users/' + user_id,
        data: data,
      })

      return result
    },
    async create (data) {
      const result = await RequestService.sendRest({
        method: 'post',
        url: '/users/create',
        data: data,
      })

      return result
    },
  },
})

export default usersStore
