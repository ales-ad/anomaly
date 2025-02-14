import { defineStore } from 'pinia'
import RequestService from '@/api'
import { useTelegram } from '@/services/telegram'

const { user } = useTelegram()

const stepsStore = defineStore('steps', {
  state: () => ({
    step: 0,
    isLeader: false,
    visibleSelect: false,
    visibleSelectTg: false,
    currentEvent: {},
    itemsClients: [],
    currentUser: {},
    role: [],
    specialty: [],
    income: [],
  }),
  getters: {
    getRole () {

      if (this.isLeader) {
        this.role.map(_i => {
          if (_i.name.toLowerCase() == 'предприниматель') {
            console.log(_i)
            _i.name = _i.name.slice(0, -1) + 'и'
          }
        })
      }
      return this.role
    },

  },
  actions: {
    setIsLeader (value) {
      this.isLeader = value
    },
    setVisibleSelect (value) {
      this.visibleSelect = value
    },
    setVisibleSelectTg (value) {
      this.visibleSelectTg = value
    },
    incrementStep () {
      this.step++
    },
    decrimentStep () {

      this.step--
      console.log(this.step)
    },

    async detailEvents (event_id) {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/events/' + event_id,
      })
      this.currentEvent = result.data

      return result.data
    },
    async createUser (eventId, data) {
      const result = await RequestService.sendRest({
        method: 'post',
        url: '/clients',
        data: data,
      })
      if (!user) {
        localStorage.setItem('userId_' + eventId, result.data.id)
      }
      return result
    },
    async patchUser (eventId, data) {
      let result = null
      if (user) {
        result = await RequestService.sendRest({
          method: 'patch',
          url: '/clients/get-by-tg/' + user.id + '/' + eventId,
          data: data,
        })
      } else {
        let userId = localStorage.getItem('userId_' + eventId)
        result = await RequestService.sendRest({
          method: 'patch',
          url: '/clients/' + userId,
          data: data,
        })
      }

      return result
    },
    async detailUsers (eventId) {
      let result = null
      if (user) {
        result = await RequestService.sendRest({
          method: 'get',
          url: '/clients/get-by-tg/' + user.id + '/' + eventId,
        })
      } else {
        let userId = localStorage.getItem('userId_' + eventId)
        if (userId) {
          result = await RequestService.sendRest({
            method: 'get',
            url: '/clients/' + userId,
          })
        }
      }
      if (result && result.data) {
        this.currentUser = result.data
        this.isLeader = result.data.is_leader

        this.step = 3

        if (result.data.groups_number) {
          this.step = 4
        }
        if (result.data.status == 'completed') {
          this.step = 5
        }
      }
    },
    async getList (param) {
      const result = await RequestService.sendRest({
        method: 'get',
        url: '/clients/list',
        params: param,
      })

      this.itemsClients = result.data.items
      return result
    },
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
  },
})

export default stepsStore
