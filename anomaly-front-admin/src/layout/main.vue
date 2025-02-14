<template>
  <VaLayout style="height: 100vh" :left="{ absolute: breakpoints.smDown }">
    <template #top>
      <VaNavbar color="primary" class="py-2">
        <template #left>
          <VaButton :icon="showSidebar ? 'menu_open' : 'menu'" @click="showSidebar = !showSidebar"/>
        </template>
        <template #center>
          <VaNavbarItem class="font-bold text-lg ">
            <h3 class="va-h3"> Аномалия </h3>
          </VaNavbarItem>
        </template>
        <template #right>
          <div class="flex flex-col ">
            <h4 class="va-h6"> {{ currentUser.login }} </h4>
            <VaButton class="mt-0" color="warning" @click="onLogout">Выход</VaButton>
          </div>
        </template>
      </VaNavbar>
    </template>
    <template #left>
      <VaSidebar v-model="showSidebar">
        <VaSidebarItem v-if="currentUser.role=='admin'">
          <VaSidebarItemContent>
            <VaIcon name="home"/>
            <VaSidebarItemTitle v-on:click='push("users")'>
              Пользователи
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
        <VaSidebarItem>
          <VaSidebarItemContent>
            <VaIcon name="event"/>
            <VaSidebarItemTitle v-on:click='push("events")'>
              Мероприятия
            </VaSidebarItemTitle>
          </VaSidebarItemContent>
        </VaSidebarItem>
      </VaSidebar>
    </template>

    <template #content>
      <router-view/>
    </template>
  </VaLayout>
</template>

<script>
import usersStore from '@/store/users'
import useAuthStore from '@/store/auth'
import { useBreakpoint } from 'vuestic-ui'

export default {

  name: 'LayoutMain',
  data () {
    return {
      showSidebar: true,
      breakpoints: useBreakpoint(),
      columns: [
        { key: 'id' },
        { key: 'Логин' },
        {
          key: 'action',
          name: 'action',
          label: '  ',
        },
      ],
      items: [],
    }
  },
  computed: {
    currentUser () {
      return this.user.currentUser
    },
  },
  methods: {
    push (value) {
      this.$router.push({ name: value })
    },
    onLogout () {
      this.auth.logout()
      window.location.href = '/login'
    },
  },
  setup () {
    const user = usersStore()
    const auth = useAuthStore()
    return {
      user,
      auth,
    }

  },
  async mounted () {
    await this.user.getMy()
  },

}
</script>
