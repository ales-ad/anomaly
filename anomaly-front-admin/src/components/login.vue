<template>
  <main class="h-full flex items-center justify-center mx-auto max-w">
    <VaCard>
      <VaCardTitle>
        <h1>Авторизация</h1>
      </VaCardTitle>
      <VaCardContent>
        <VaForm ref="formRefAuth" class="form-login flex flex-col gap-2">
          <VaInput
            v-model="login"
            :rules="[(value) => (value && value.length > 0) || 'Is required']"
            label="Логин"
          />
          <VaInput
            v-model="password"
            label="Пароль"
            :rules="[(value) => (value && value.length > 0) || 'Is required']"
            type="password"
          />
          <VaButton @click="onLogin">
            Войти
          </VaButton>
        </VaForm>
      </VaCardContent>
    </VaCard>
  </main>

</template>

<script>
import useAuthStore from '@/store/auth'

import { useForm } from 'vuestic-ui'

export default {
  name: 'UserLogin',
  data () {
    return {
      password: null,
      login: null,
      error: null,
    }
  },
  setup () {
    console.log('setup')
    const { isValid, validate, reset, resetValidation } = useForm('formRefAuth')
    const auth = useAuthStore()

    return { auth, isValid, validate, reset, resetValidation }

  },
  methods: {
    redirectPage (path) {
      this.$router.push({ path })
    },
    async onLogin () {
      this.error = null
      if (this.validate()) {
        try {
          await this.auth.login({ login: this.login, password: this.password })

          this.redirectPage('/')
        } catch (e) {
          console.log(e)
          this.error = 'Ошибка авторизации'
        }
      }
    },
  },
}
</script>

<style scoped>
</style>
