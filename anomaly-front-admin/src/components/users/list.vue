<template>
  <div class="p-4">
    <h3 class="va-h3">
      Пользователи
    </h3>
    <VaForm ref="formRefCreate" class="flex form-create">
      <VaInput
        v-model="newItem.login"
        class="my-6"
        :rules="[(value) => (value && value.length > 0) || 'Is required']"
        label="Логин"
      />
      <VaSelect
        v-model="newItem.role"
        class="mb-6"
        :options="options"
        track-by="value"
        :rules="[(value) => (value && value.length > 0) || 'Is required']"
        label="роль"
      />
      <VaInput
        v-model="newItem.password"
        class="my-6"
        label="Пароль"
        type="password"
      />
      <VaInput
        :key="login"
        v-model="newItem.passwordConfirm"
        class="my-6"
        label="Повторите пароль"
        type="password"
        :rules="[(value) => (value && value.length > 0 ) || 'Is required',(value) => (value==newItem.password) || 'password not confirm']"
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
          <td colspan="3">
            <div class="flex justify-center mt-4">
              <VaPagination
                v-model="currentPage"
                :pages="totalPages"
              />
            </div>
          </td>
        </tr>
      </template>
      <template #cell(actions)="{ rowIndex }">
        <VaButton
          preset="plain"
          icon="edit"
          @click="openModalToEditItemById(rowIndex)"
        />
        <VaButton
          preset="plain"
          icon="key"
          class="ml-3"
          @click="openModalToPassItemById(rowIndex)"
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
        :key="login"
        v-model="editedItem.login"
        class="my-6"
        label="Логин"
      />
      <VaSelect
        v-model="editedItem.role"
        class="mb-6"
        :options="options"
        track-by="value"
        label="роль"
      />
    </VaModal>

    <VaModal
      class="modal-crud"
      :model-value="!!editedPassItemId"
      title="Изменить пароль"
      size="small"
      @ok="editPassItem"
      @cancel="resetEditedItem"
    >
      <VaInput
        :key="login"
        v-model="pass"
        class="my-6"
        label="Пароль"
        type="password"
        :error="errorPass"

      />
      <VaInput
        :key="login"
        v-model="passConfirm"
        class="my-6"
        label="Повторите пароль"
        type="password"
        :error="errorPass"
      />
    </VaModal>
  </div>
</template>

<script>

import usersStore from '@/store/users'
import { useForm } from 'vuestic-ui'

export default {
  name: 'UserList',
  data () {
    return {
      showSidebar: true,
      currentPage: 1,
      editedItemId: null,
      passConfirm: null,
      pass: null,
      errorPass: false,
      editedPassItemId: null,
      editedItem: null,
      columns: [
        { key: 'id', width: 20 },
        { key: 'login', label: 'Логин' },
        { key: 'role', label: 'Роль' },
        { key: 'actions', name: 'actions', label: '  ', width: 80 },
      ],
      newItem: {
        login: null,
        role: null,
        password: null,
        passwordConfirm: null,
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
      await this.users.getList(this.params)
    },
  },
  computed: {
    totalPages () {
      return Math.ceil(this.users.total / this.params.limit)
    },
    listUsers () {
      return this.users.items
    },
    options () {
      return this.users.role
    },
  },
  methods: {
    async saveNew () {
      if (this.validate()) {
        await this.users.create(this.newItem)
        await this.users.getList(this.params)

        this.reset()
        this.resetValidation()
      }
    },
    openModalToPassItemById (id) {
      this.editedPassItemId = this.listUsers[id].id
    },
    openModalToEditItemById (id) {
      this.editedItemId = id
      this.editedItem = { ...this.listUsers[id] }
    },
    resetEditedItem () {
      this.editedItem = null
      this.passConfirm = null
      this.pass = null
      this.editedItemId = null
      this.editedPassItemId = null
    },
    async editItem () {
      await this.users.update(this.editedItem.id, this.editedItem)
      await this.users.getList(this.params)
      this.resetEditedItem()
    },
    async editPassItem () {
      this.errorPass = false
      if (this.pass == null || this.passConfirm == null || this.passConfirm != this.pass) {
        this.errorPass = true
      } else {
        let data = {
          password: this.pass,
        }
        await this.users.patch(this.editedPassItemId, data)
        await this.users.getList(this.params)
        this.resetEditedItem()
      }


    },
  },
  setup () {
    console.log('setup')
    const { isValid, validate, reset, resetValidation } = useForm('formRefCreate')
    const users = usersStore()

    return { users, isValid, validate, reset, resetValidation }

  },
  async mounted () {
    console.log('mounted')
    await this.users.getList(this.params)

  },
}
</script>

<style scoped>

</style>
