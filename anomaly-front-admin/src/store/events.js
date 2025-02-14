import { defineStore } from 'pinia'
import RequestService from '@/api'

const eventsStore = defineStore('events', {
  state: () => ({
    items: [],
    currentEvent: {},
    total: 0,
  }),
  getters: {},
  actions: {
    async getList (param) {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/events/list',
        params: param,
      })

      this.total = result.data.total
      this.items = result.data.items
      return result
    },
    async createGroup (events_id) {
      const result = await RequestService.sendRest({
        method: 'post',
        url: '/events/create-group/' + events_id,
      })

      return result
    },
    async resetGroup (events_id) {
      const result = await RequestService.sendRest({
        method: 'post',
        url: '/events/reset-group/' + events_id,
      })

      return result
    },
    async update (events_id, data) {
      const result = await RequestService.sendRest({
        method: 'put',
        url: '/events/' + events_id,
        data: data,
      })

      return result
    },
    async patch (event_id, data) {
      const result = await RequestService.sendRest({
        method: 'patch',
        url: '/events/' + event_id,
        data: data,
      })

      return result
    },
    async create (data) {
      const result = await RequestService.sendRest({
        method: 'post',
        url: '/events',
        data: data,
      })

      return result
    },
    async detail (event_id) {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/events/' + event_id,
      })
      this.currentEvent = result.data
      return result.data
    },
  },
})

export default eventsStore
