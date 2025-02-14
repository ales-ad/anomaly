import { defineStore } from 'pinia'
import RequestService from '@/api'

const clientsStore = defineStore('clients', {
  state: () => ({
    items: [],
    groups: [],
    role: [],
    specialty: [],
    income: [],
    total: 0,
  }),
  getters: {},
  actions: {
    async getDic () {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/dictionaries/all',
      })
      this.income = result.data.income
      this.specialty = result.data.specialty
      this.role = result.data.role
      return result.data
    },
    async getListGroups (param) {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/groups/list',
        params: param,
      })

      this.groups = result.data.items

      return result
    },
    async getList (param) {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/clients/list',
        params: param,
      })

      this.total = result.data.total
      this.items = result.data.items
      return result
    },
    async update (events_id, data) {
      const result = await RequestService.sendRest({
        method: 'put',
        url: '/clients/' + events_id,
        data: data,
      })

      return result
    },
    async patch (user_id, data) {
      const result = await RequestService.sendRest({
        method: 'patch',
        url: '/clients/' + user_id,
        data: data,
      })

      return result
    },
    async create (data) {
      const result = await RequestService.sendRest({
        method: 'post',
        url: '/clients',
        data: data,
      })

      return result
    },
  },
})

export default clientsStore
