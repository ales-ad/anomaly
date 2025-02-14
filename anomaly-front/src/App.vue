<template>
  <router-view/>
</template>
<script>
import { useTelegram } from './services/telegram'

export default {
  setup () {
    const { tg } = useTelegram()
    return { tg }
  },
  mounted () {
    if (this.tg) {
      // Сигнализируем о том, что приложение готово
      this.tg.ready()
      // Разворачиваем на весь экран
      this.tg.expand()
    }
  },
}
</script>

<style lang="scss">
@import "assets/scss/style";
</style>
