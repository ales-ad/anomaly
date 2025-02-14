<template>
  <div class="flex-column">
    <img src="../assets/logo.png">
    <div class="h-main">Найди свою десятку!</div>
    <button class="btn-main" v-on:click="onChangeStep">Заполнить анкету</button>
  </div>
</template>

<script>
import stepsStore from '@/store/step'

export default {
  name: 'mainScreen',

  setup () {
    const steps = stepsStore()
    return { steps }
  },

  methods: {
    onChangeStep () {
      this.steps.incrementStep()
    },
  },
}
</script>

<style scoped>

</style>
