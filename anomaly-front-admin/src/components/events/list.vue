<template>
  <div class="p-4">
    <h3 class="va-h3">
      Мероприятия
    </h3>
    <VaForm ref="formRefCreate" class="flex form-create" v-if="currentUser.role=='admin'">
      <VaInput
        v-model="newItem.name"
        class="my-6"
        :rules="[(value) => (value && value.length > 0) || 'Is required']"
        label="Наименование"
      />
      <VaDateInput v-model="newItem.date" label="Дата"/>
      <VaSelect
        v-model="newItem.city_id"
        class="mb-6"
        :options="optionsCities"
        track-by="id"
        :rules="[(value) => (value) || 'Is required']"
        label="Город"
        text-by="name"
        value-by="id"
      />
      <VaSelect
        v-model="newItem.moderator_id"
        class="mb-6"
        :options="options"
        track-by="id"
        :rules="[(value) => (value) || 'Is required']"
        label="Модератор"
        text-by="login"
        value-by="id"
      />

      <VaButton
        :disabled="!newItem"
        class="mt-3"
        @click="saveNew"
      >
        Добавить
      </VaButton>
    </VaForm>

    <VaDataTable
      v-if="listUsers"
      class="table-crud"
      striped
      :items="listUsers"
      :columns="columns"
    >
      <template #bodyAppend>
        <tr>
          <td colspan="6">
            <div class="flex justify-center mt-4">
              <VaPagination
                v-model="currentPage"
                :pages="totalPages"
              />
            </div>
          </td>
        </tr>
      </template>
      <template #cell(actions)="{ rowIndex, rowData }">
        <VaButton
          preset="plain"
          icon="edit"
          v-if="currentUser.role=='admin'"
          @click="openModalToEditItemById(rowIndex)"
        />
        <VaButton
          preset="plain"
          icon="visibility"
          class="ml-3"
          @click="openEvent(rowData.id)"
        />
      </template>
    </VaDataTable>

    <VaModal
      class="modal-crud"
      :model-value="!!editedItem"
      title="Редактирование"
      size="small"
      @ok="editItem"
      @cancel="resetEditedItem"
    >
      <VaInput
        v-model="editedItem.name"
        class="my-6"
        :rules="[(value) => (value && value.length > 0) || 'Is required']"
        label="Наименование"
      />
      <VaDateInput v-model="editedItem.date" :format-date="formatDate" class=".my-6" label="Дата"/>
      <VaSelect
        v-model="editedItem.city_id"
        class="my-6 width-full"
        :options="optionsCities"
        track-by="id"
        :rules="[(value) => (value) || 'Is required']"
        label="Город"
        text-by="name"
        value-by="id"
      />
      <VaSelect
        v-model="editedItem.moderator_id"
        class="my-6"
        :options="options"
        track-by="id"
        :rules="[(value) => (value) || 'Is required']"
        label="Модератор"
        text-by="login"
        value-by="id"
      />
    </VaModal>
  </div>
</template>

<script>

import usersStore from '@/store/users'
import eventsStore from '@/store/events'
import citiesStore from '@/store/cities'
import { useForm } from 'vuestic-ui'

export default {
  name: 'UserList',
  data () {
    return {
      showSidebar: true,
      currentPage: 1,
      editedItemId: null,
      editedItem: null,
      columns: [
        { key: 'id', width: 20 },
        { key: 'name', label: 'Наименовние' },
        { key: 'date', label: 'Дата' },
        { key: 'city_name', label: 'Город' },
        { key: 'moderator_name', label: 'Модератор' },
        { key: 'actions', name: 'actions', label: '  ', width: 80 },
      ],
      newItem: {
        name: null,
        date: null,
        city_id: null,
        moderator_id: null,
      },
      params: {
        limit: 20,
        offset: 0,
      },
    }
  },
  watch: {
    async currentPage (value) {
      this.params.offset = (value - 1) * this.params.limit
      await this.events.getList(this.params)
    },
  },
  computed: {
    currentUser () {
      return this.users.currentUser
    },
    totalPages () {
      return Math.ceil(this.users.total / this.params.limit)
    },
    listUsers () {
      return this.events.items
    },
    options () {
      return this.users.items
    },
    optionsCities () {
      return this.cities.items
    },
  },
  methods: {
    formatDate (date) {
      var z = n => ('0' + n).slice(-2)
      return `${date.getFullYear()}-${z(date.getMonth() + 1)}-${date.getDate()}`
    },
    openEvent (id) {
      this.$router.push({
        name: 'eventsOne',
        params: {
          idEvent: id,
        },
      })
    },

    async saveNew () {
      if (this.validate()) {
        var z = n => ('0' + n).slice(-2)

        this.newItem.date = `${this.newItem.date.getFullYear()}-${z(this.newItem.date.getMonth() + 1)}-${this.newItem.date.getDate()}`


        await this.events.create(this.newItem)
        await this.events.getList(this.params)

        this.reset()
        this.resetValidation()
      }
    },

    openModalToEditItemById (id) {
      this.editedItemId = id
      this.editedItem = { ...this.listUsers[id] }
    },
    resetEditedItem () {
      this.editedItem = null
      this.editedItemId = null
    },
    async editItem () {

      var z = n => ('0' + n).slice(-2)
      this.editedItem.date = new Date(this.editedItem.date)
      console.log(this.editedItem.date)
      this.editedItem.date = `${this.editedItem.date.getFullYear()}-${z(this.editedItem.date.getMonth() + 1)}-${this.editedItem.date.getDate()}`

      await this.events.update(this.editedItem.id, this.editedItem)
      await this.events.getList(this.params)
      this.resetEditedItem()
    },

  },
  setup () {
    console.log('setup')
    const { isValid, validate, reset, resetValidation } = useForm('formRefCreate')
    const users = usersStore()
    const events = eventsStore()
    const cities = citiesStore()

    return { users, events, cities, isValid, validate, reset, resetValidation }

  },
  async mounted () {

    console.log('mounted')
    await this.events.getList(this.params)
    await this.users.getList({ _full: true })
    await this.cities.getList({ _full: true })

  },
}
</script>

<style scoped>

</style>
