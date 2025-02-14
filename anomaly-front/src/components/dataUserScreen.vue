<template>
  <div class="flex-column gap-0" v-on:click="closeKB">
    <div class="header--left header--abs">
      <div class="btn-top-back btn-top-back--icon" v-on:click="back()"><img src="../assets/back.svg">Back</div>
    </div>
    <img class="mini-logo" src="../assets/logo2.png">
    <div class="text-city">{{ event.city_name }}</div>
    <div class="text-form">Анкета
      <template v-if=leader>
        капитана
      </template>
      <template v-else>
        участника
      </template>
    </div>

    <div class="input-wrapper">
      <label>Имя</label>
      <input type="text" v-model="name" placeholder="Укажите имя и фамилию">
      <img v-if="name" v-on:click="name=null" class="btn-inner-input" src="../assets/clear.svg">
    </div>
    <div class="input-wrapper">
      <label>Возраст</label>
      <input type="number" v-model="age" placeholder="Укажите возраст">
      <img v-if="age" v-on:click="age=null" class="btn-inner-input" src="../assets/clear.svg">
    </div>

    <div class="wrapper-select" v-if="leader">
      <template v-if="count_group_current>0">
        <div class="wrapper-select__content">
          <div class="wrapper-select__label">
            Сколько участников в десятке
          </div>
          <div class="wrapper-select__text">{{ count_group_current }}</div>
        </div>
      </template>
      <template v-else>
        <div class="wrapper-select__text">
          Сколько участников в десятке
        </div>
      </template>
      <div class="btn-top-back" v-on:click="openSelect('count')">
        <template v-if="count_group_current>0">
          Изменить
        </template>
        <template v-else>
          Выбрать
        </template>
      </div>
    </div>

    <div class="wrapper-select">
      <template v-if="specialty">
        <div class="wrapper-select__content">
          <div class="wrapper-select__label">
            <template v-if=leader>
              Ниши участников
            </template>
            <template v-else>
              Ниша
            </template>
          </div>
          <div class="wrapper-select__text">{{ specialty }}</div>
        </div>
      </template>
      <template v-else>
        <div class="wrapper-select__text">
          <template v-if=leader>
            Ниши участников
          </template>
          <template v-else>
            Ниша
          </template>
        </div>
      </template>
      <div class="btn-top-back" v-on:click="openSelect('specialty')">
        <template v-if="specialty">
          Изменить
        </template>
        <template v-else>
          Выбрать
        </template>
      </div>
    </div>

    <div class="wrapper-select">
      <template v-if="income">
        <div class="wrapper-select__content">
          <div class="wrapper-select__label">
            <template v-if=leader>
              Средний доход участников
            </template>
            <template v-else>
              Твой личный доход
            </template>
          </div>
          <div class="wrapper-select__text">{{ income }}</div>
        </div>
      </template>
      <template v-else>
        <div class="wrapper-select__text">
          <template v-if=leader>
            Средний доход участников
          </template>
          <template v-else>
            Твой личный доход
          </template>
        </div>
      </template>
      <div class="btn-top-back" v-on:click="openSelect('income')">
        <template v-if="income">
          Изменить
        </template>
        <template v-else>
          Выбрать
        </template>
      </div>
    </div>

    <div class="wrapper-select">
      <template v-if="role">
        <div class="wrapper-select__content">
          <div class="wrapper-select__label">
            <template v-if=leader>
              Из кого состоит ваша десятка
            </template>
            <template v-else>
              Роль
            </template>
          </div>
          <div class="wrapper-select__text">{{ role }}</div>
        </div>
      </template>
      <template v-else>
        <div class="wrapper-select__text">
          <template v-if=leader>
            Из кого состоит ваша десятка
          </template>
          <template v-else>
            Роль
          </template>
        </div>
      </template>
      <div class="btn-top-back" v-on:click="openSelect('role')">
        <template v-if="role">
          Изменить
        </template>
        <template v-else>
          Выбрать
        </template>
      </div>
    </div>

    <div class="custom-checkbox-wrapper">
      <input type="checkbox" class="custom-checkbox" id="req" v-model="confirm">
      <label for="req"><span>Я даю согласие на обработку персональных данных на условиях <a
          href="https://anomalysquad.ru/Policy.pdf" target="_blank">Политики конфиденциальности</a></span></label>
    </div>

    <div class="select-options" v-if="getVisibleSelect">
      <div class="header--left">

        <div class="btn-top-back btn-top-back--icon" v-on:click="Close"><img src="../assets/back.svg">Back</div>
      </div>
      <div class="select-options__title">
        <template v-if=leader>
          {{ titleLeader[options.type] }}
        </template>
        <template v-else>
          {{ title[options.type] }}
        </template>

      </div>
      <div class="select-options__item" v-for="(item,key) in options.item" v-on:click="choose(item)" :key="key">
        {{ item.name }}
      </div>
    </div>

    <button class="btn-main btn-main--loader mt-8" :disabled="validateData || isload" v-on:click="onChangeStep"><img
        v-if="isload" src="../assets/loader.svg">Найти десятку
    </button>


  </div>
</template>

<script>
import stepsStore from '@/store/step'
import { useTelegram } from '@/services/telegram'

export default {
  name: 'dataUserScreen',
  props: ['EventId'],
  data () {
    return {
      name: null,
      isload: false,
      age: null,
      income: null,
      income_id: null,
      specialty: null,
      specialty_id: null,
      count_group_current: 0,
      confirm: null,
      role: null,
      role_id: null,
      options: {
        item: [],
        type: '',
      },
      title: {
        'role': 'Выберите роль',
        'income': 'Выберите доход',
        'specialty': 'Выберите нишу',
      },
      titleLeader: {
        'count': 'Сколько участников в десятке',
        'role': 'Выберите, из кого состоит ваша десятка',
        'income': 'Выберите средний доход участников',
        'specialty': 'Выберите ниши участников',
      },
    }
  },
  setup () {
    const steps = stepsStore()
    const { user } = useTelegram()
    return { steps, user }
  },
  mounted () {
    this.options.item = this.incomeList
  },
  computed: {
    validateData () {
      return !(!!this.name && !!this.age && !!this.income && !!this.specialty && !!this.role && !!this.confirm && ((this.leader && this.count_group_current) || !this.leader))
    },
    leader () {
      return this.steps.isLeader
    },
    event () {
      return this.steps.currentEvent
    },
    roleList () {

      return this.steps.getRole

    },
    specialtyList () {
      return this.steps.specialty
    },
    incomeList () {
      return this.steps.income
    },
    getVisibleSelect () {
      return this.steps.visibleSelect
    },
  },
  methods: {
    back () {
      this.steps.setIsLeader(false)
      this.steps.decrimentStep()
    },
    closeKB (event) {
      const focusedElement = document.activeElement
      if (focusedElement && focusedElement !== event.target && ['INPUT', 'TEXTAREA'].includes(focusedElement.tagName)) {
        focusedElement.blur()
      }
    },
    openSelect (type) {
      console.log(type)
      this.options.type = type
      switch (type) {
        case 'role':
          this.options.item = this.roleList
          break
        case 'income':
          this.options.item = this.incomeList
          break
        case 'specialty':
          this.options.item = this.specialtyList
          break
        case 'count':
          let itemCount = []
          for (var i = 1; i <= 10; i++) {
            itemCount.push({ name: i })
          }

          this.options.item = itemCount
          break
      }

      this.steps.setVisibleSelect(true)
    },
    Close () {
      this.steps.setVisibleSelect(false)
    },
    async onChangeStep () {
      this.isload = true

      let data = {
        'tg_id': (this.user) ? String(this.user.id) : null,
        'tg_username': (this.user) ? this.user.username : null,
        'name': this.name,
        'age': this.age,
        'link': null,
        'specialty_id': this.specialty_id,
        'income_id': this.income_id,
        'role_id': this.role_id,
        'is_leader': this.leader,
        'count_group_current': this.count_group_current,
        'event_id': this.EventId,
      }
      await this.steps.createUser(this.EventId, data)

      await this.steps.detailUsers(this.EventId)
      this.isload = false

    },
    choose (data) {
      switch (this.options.type) {
        case 'role':
          this.role = data.name
          this.role_id = data.id
          break
        case 'income':
          this.income = data.name
          this.income_id = data.id
          break
        case 'specialty':
          this.specialty = data.name
          this.specialty_id = data.id
          break
        case 'count':
          this.count_group_current = data.name
          break
      }
      this.steps.setVisibleSelect(false)
    },


  },
}
</script>

<style scoped>

</style>
