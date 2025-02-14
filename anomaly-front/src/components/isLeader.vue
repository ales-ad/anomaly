<template>
  <div class="flex-column">
    <div class="header--left header--abs" v-if="stepIsLid>0">
      <div class="btn-top-back btn-top-back--icon" v-on:click="back()"><img src="../assets/back.svg">Back</div>
    </div>
    <img v-if="stepIsLid==2" src="../assets/logo.png">
    <div class="h-main" :class="{  'max-width-300': stepIsLid==2 }">{{ stepData[stepIsLid].question }}</div>
    <button class="btn-main" v-if="stepIsLid<2" v-on:click="answerYes()">Да</button>
    <button class="btn-main btn-mt-up" v-if="stepIsLid<2" v-on:click="answerNo()">Нет</button>
  </div>
</template>

<script>
import stepsStore from '@/store/step'

export default {
  name: 'mainScreen',
  data () {
    return {
      stepIsLid: 0,
      stepData: [
        { question: 'У вас уже есть десятка?' },
        { question: 'Вы капитан своей десятки?' },
        { question: 'Супер! Просто подождите, капитан всё заполнит' },
      ],
    }
  },

  setup () {
    const steps = stepsStore()
    return { steps }
  },

  methods: {
    answerYes () {
      switch (this.stepIsLid) {
        case 0:
          this.stepIsLid++
          break
        case 1:
          this.steps.setIsLeader(true)
          this.onChangeStep()
          break
      }
    },
    answerNo () {
      this.steps.setIsLeader(false)
      switch (this.stepIsLid) {
        case 0:
          this.onChangeStep()
          break
        case 1:
          this.stepIsLid++
          break
      }
    },
    back () {
      this.stepIsLid--
    },
    onChangeStep () {
      this.steps.incrementStep()
    },
  },
}
</script>
