import { defineStore } from 'pinia'
import RequestService from '@/api'

const citiesStore = defineStore('cities', {
  state: () => ({
    items: [],
    total: 0,
  }),
  getters: {},
  actions: {
    async getList (param) {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/cities/list',
        params: param,
      })

      this.total = result.data.total
      this.items = result.data.items
      return result
    },

  },
})

export default citiesStore
