<template>
  <div class="flex-column">
    <img src="../assets/logo.png">

    <div class="h-main">Ждите, происходит магия…</div>


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
  data () {
    return {
      timer: null,
    }
  },
  async unmounted () {

    clearInterval(this.timer)
  },
  mounted () {
    let vim = this
    this.timer = setInterval(async () => {
      let data = await this.steps.detailEvents(vim.EventId)
      if (data.status == 'generated') {
        await this.steps.detailUsers(this.EventId)
      }
    }, 2000)
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
