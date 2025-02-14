<template>
  <div class="flex-column flex-column--finish gap-0">
    <div class="text-city">Десятка № {{ currentUser.groups_number }}</div>
    <div class="text-form">Чат</div>

    <div class="wrapper-select" v-if="!currentUser.link">
      <div class="wrapper-select__text">Ссылка на чат в Telegram</div>
      <div class="btn-top-back" v-if="leader || !leaderOther" v-on:click="openLinkEdit()">
        Добавить
      </div>
    </div>
    <button class="btn-main mt-12" v-else v-on:click="openLink()">Перейти в чат десятки</button>

    <div class="text-form">Участники</div>
    <div class="item-clients-wrapper">
      <div class="flex-column-clear" v-for="(item,key) in currentItemsClients" :key="key">
        <div class="item-clients">
          <div class="item-clients__number">{{ key + 1 }}</div>
          <div class="item-clients__content">
            <div class="item-clients__text">{{ item.name }}, {{ item.age }} лет</div>
            <div class="item-clients__desc">{{ item.role_name }} • {{ item.specialty_name }}</div>
          </div>
        </div>
        <svg style="margin-top: 16px;" width="100%" height="2" viewBox="0 0 344 2" fill="none"
             xmlns="http://www.w3.org/2000/svg">
          <path d="M1 1H343" stroke="black" stroke-opacity="0.15" stroke-width="0.5" stroke-linecap="round"/>
        </svg>
      </div>
    </div>

    <div class="select-options" v-if="getVisibleSelectTg">
      <div class="header--left">

        <div class="btn-top-back btn-top-back--icon" v-on:click="Close"><img src="../assets/back.svg">Back</div>
      </div>
      <div class="select-options__title">Введите ссылку на ваш чат в Telegram</div>
      <div class="input-wrapper">
        <input type="text" v-model="currentUser.link" placeholder="Ввести ссылку">
        <img v-if="currentUser.link" v-on:click="currentUser.link=null" class="btn-inner-input"
             src="../assets/clear.svg">
      </div>
      <button class="btn-main " :disabled="validateData" v-on:click="onChangeStep">Сохранить</button>
    </div>
  </div>
</template>

<script>
import stepsStore from '@/store/step'
import { useTelegram } from '@/services/telegram'

export default {
  name: 'mainScreen',
  props: ['EventId'],
  setup () {
    const steps = stepsStore()
    const { tg, user } = useTelegram()
    return { steps, tg, user }
  },
  data () {
    return {
      timer: null,
    }
  },
  async unmounted () {

    clearInterval(this.timer)
  },
  async mounted () {
    let vim = this
    await this.getData()
    this.timer = setInterval(async () => {
      await vim.getData()
    }, 2000)
  },
  computed: {
    leader () {
      return this.steps.isLeader
    },
    leaderOther () {
      return this.steps.itemsClients.filter((_i) => _i.is_leader).length
    },
    validateData () {
      return !(!!this.currentUser.link)
    },
    getVisibleSelectTg () {
      return this.steps.visibleSelectTg
    },
    currentUser () {
      return this.steps.currentUser
    },
    currentItemsClients () {
      return this.steps.itemsClients
    },
  },
  methods: {
    Close () {
      this.steps.setVisibleSelectTg(false)
    },
    async getData () {

      await this.steps.getList({ _full: true, group_id: this.currentUser.groups_id })
      let item = this.currentItemsClients.find((_i) => _i.link != null)
      if (item) {

        if (!this.currentUser.link)
          this.currentUser.link = item.link
      }
    },
    openLinkEdit () {
      this.steps.setVisibleSelectTg(true)
    },
    openLink () {
      if (this.user) {
        this.tg.openTelegramLink(this.currentUser.link)
      } else {
        window.open(this.currentUser.link, '_blank')
      }

    },
    async onChangeStep () {
      await this.steps.patchUser(this.EventId, { link: this.currentUser.link })
      this.steps.setVisibleSelectTg(false)
    },
  },
}
</script>

<style scoped>

</style>
