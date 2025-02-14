<template>
  <div class="flex-column">
    <div class="span-text">Номер твоей десятки</div>
    <div class="number">{{ currentUser.groups_number }}</div>
    <button class="btn-main" v-on:click="onChangeStep">Нашёл своих</button>
  </div>
</template>

<script>
import stepsStore from '@/store/step'

export default {
  name: 'awaitScreen',
  props: ['EventId'],
  setup () {
    const steps = stepsStore()
    return { steps }
  },
  computed: {
    currentUser () {
      return this.steps.currentUser
    },
  },
  methods: {
    async onChangeStep () {
      await this.steps.patchUser(this.EventId, { status: 'completed' })
      this.steps.incrementStep()
      await this.steps.detailUsers(this.EventId)
    },
  },
}
</script>

<style scoped>

</style>
