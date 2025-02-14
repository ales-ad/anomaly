<template>
  <div class="p-4">
    <h3 class="va-h3">Событие № {{ currentEvent.name }} ({{ currentEvent.city_name }} - {{ currentEvent.date }})</h3>
    Ссылка WEB: <span class="click-link"
                      v-on:click="copyToClipboard">https://anomalysquad.ru?event_id={{ idEvent }}</span><br>
    Ссылка TG: <span class="click-link"
                     v-on:click="copyToClipboardTg">https://t.me/anomaly_offline_bot?startapp={{ idEvent }}</span><br>
    <VaButton
      v-if="currentEvent.status=='wait'"
      class="mt-3"
      @click="changeEvent('start')"
    >Начать Сбор
    </VaButton>
    <VaButton
      v-if="currentEvent.status=='start'"
      class="mt-3"
      @click="onCreateGroup()"
    >
      Сформировать десятки
    </VaButton>
    <VaButton
      v-if="currentEvent.status=='generated'"
      class="mt-3 ml-3"
      @click="onResetGroup()"
    >Сбросить
    </VaButton>

    <VaForm ref="formRefCreateClient" class="flex form-create">
      <VaInput
        v-model="dataUserNew.name"
        class="my-6"
        :rules="[(value) => (value && value.length > 0) || 'Is required']"
        label="Имя"
      />
      <VaInput
        v-model="dataUserNew.age"
        class="my-6"
        type="number"
        :rules="[(value) => (value) || 'Is required']"
        label="Возраст"
      />
      <VaSelect
        v-model="dataUserNew.role_id"
        class="mb-6"
        :options="listRole"
        track-by="id"
        :rules="[(value) => (value) || 'Is required']"
        label="Роль"
        text-by="name"
        value-by="id"
      />
      <VaSelect
        v-model="dataUserNew.income_id"
        class="mb-6"
        :options="listIncome"
        track-by="id"
        :rules="[(value) => (value) || 'Is required']"
        label="Доход"
        text-by="name"
        value-by="id"
      />
      <VaSelect
        v-model="dataUserNew.specialty_id"
        class="mb-6"
        :options="listSpecialty"
        track-by="id"
        :rules="[(value) => (value) || 'Is required']"
        label="Ниша"
        text-by="name"
        value-by="id"
      />
      <VaButton
        class="mt-3"
        @click="saveNewClients"
      >
        Добавить
      </VaButton>
    </VaForm>
    
    <h4 class="va-h4 mt-5">Участники</h4>
    <VaDataTable
      v-if="listClients"
      class="table-crud"
      striped
      :items="listClients"
      :columns="columns"
    >
      <template #cell(name)="{ rowIndex, rowData }">
        <h6 class="va-h5">{{ rowData.name }}
          <template v-if="rowData.tg_id">
            (TG ИД - {{ rowData.tg_id }}:{{ rowData.tg_username }})
          </template>
          <template v-else>
            <span class="">(Web)</span>
          </template>
        </h6>
        <span v-if="rowData.is_leader">
                        <span class="">Капитан (размер группы: {{ rowData.count_group_current }})</span>
                    </span>

      </template>
      <template #cell(data)="{ rowIndex, rowData }">
        <span><b>Возраст:</b>  {{ rowData.age }}</span><br>
        <span><b>Ниша:</b>  {{ rowData.specialty_name }}</span><br>
        <span><b>Роль:</b>  {{ rowData.role_name }}</span><br>
        <span><b>Доход:</b> {{ rowData.income_name }}</span><br>
      </template>
      <template #cell(groups_number)="{ rowIndex, rowData }">
        <div class=" flex-group">
          <template v-if="rowData.groups_number==null">
            <span>не определена</span>
          </template>
          <template v-else>
            <VaChip size="large" color="success">
              {{ rowData.groups_number }}
            </VaChip>
          </template>

          <VaButton v-if="currentEvent.status=='generated'"
                    @click="onModalToEditItemById(rowData)"
          >
            Изменить группу
          </VaButton>
        </div>
      </template>
    </VaDataTable>

    <VaModal
      class="modal-crud"
      :model-value="!!editedItemId"
      title="Изменить группу"
      size="small"
      @ok="editItem"
      @cancel="resetEditedItem"
    >
      <VaSelect
        v-model="editedItem.groups_id"
        class="mb-6"
        :options="listGroups"
        track-by="id"
        label="Группа"
        text-by="number"
        value-by="id"
      />

    </VaModal>
  </div>
</template>

<script>
import eventsStore from '@/store/events'
import clientsStore from '@/store/clients'
import { useForm } from 'vuestic-ui'

export default {
  name: 'EventsOneDetail',
  props: {
    idEvent: {
      type: Number,
      required: true,
    },
  },
  data () {
    return {
      timer: null,
      dataUserNew: {
        tg_id: null,
        tg_username: null,
        name: null,
        age: null,
        link: null,
        specialty_id: null,
        income_id: null,
        role_id: null,
        role_id: null,
        is_leader: false,
        count_group_current: 0,
        event_id: null,
      },
      editedItem: null,
      editedItemId: null,
      columns: [
        {
          key: 'id',
          width: 20,
        },
        {
          key: 'name',
          label: 'Имя',
        },
        {
          key: 'data',
          label: 'Данные',
        },
        {
          key: 'groups_number',
          label: 'Группа',
        },
        {
          key: 'actions',
          name: 'actions',
          label: '  ',
          width: 80,
        },
      ],
    }
  },
  setup () {
    console.log('setup')
    const events = eventsStore()
    const clients = clientsStore()
    const { isValid, validate, reset, resetValidation } = useForm('formRefCreateClient')
    return {
      events, clients, isValid, validate, reset, resetValidation,
    }

  },
  async mounted () {
    await this.clients.getDic()
    await this.events.detail(this.idEvent)
    await this.getData()
    let vim = this
    this.timer = setInterval(async () => {
      await vim.getData()

    }, 2000)
  },
  async unmounted () {
    clearInterval(this.timer)
  },
  methods: {
    async getData () {
      await this.clients.getList({
        event_id: this.idEvent,
        _full: true,
      })
      await this.clients.getListGroups({ event_id: this.idEvent })
    },
    async copyToClipboardTg () {
      await navigator.clipboard.writeText('https://t.me/anomaly_offline_bot?startapp=' + this.idEvent)
    },
    async copyToClipboard () {
      await navigator.clipboard.writeText('https://anomalysquad.ru?event_id=' + this.idEvent)
    },
    async changeEvent (status) {
      await this.events.patch(this.idEvent, { status: status })
      await this.events.detail(this.idEvent)
    },
    async saveNewClients () {
      if (this.validate()) {
        this.dataUserNew.event_id = this.idEvent
        await this.clients.create(this.dataUserNew)
        await this.clients.getList({
          event_id: this.idEvent,
          _full: true,
        })
        await this.clients.getListGroups({ event_id: this.idEvent })
        this.reset()
        this.resetValidation()
      }

    },
    async onCreateGroup () {
      await this.events.createGroup(this.idEvent)

      await this.events.detail(this.idEvent)
      await this.clients.getList({
        event_id: this.idEvent,
        _full: true,
      })
      await this.clients.getListGroups({ event_id: this.idEvent })
    },
    async onResetGroup () {
      await this.events.resetGroup(this.idEvent)

      await this.events.detail(this.idEvent)
      await this.clients.getList({
        event_id: this.idEvent,
        _full: true,
      })
      await this.clients.getListGroups({ event_id: this.idEvent })
    },
    resetEditedItem () {
      this.editedItem = null
      this.editedItemId = null
    },
    async editItem () {
      await this.clients.patch(this.editedItemId, { groups_id: this.editedItem.groups_id })
      await this.clients.getList({
        event_id: this.idEvent,
        _full: true,
      })
      this.resetEditedItem()

    }
    ,
    onModalToEditItemById (raw) {
      this.editedItemId = raw.id
      this.editedItem = { ...raw }
    }
    ,
  },
  computed: {
    currentEvent () {
      return this.events.currentEvent
    },
    listClients () {
      return this.clients.items
    },
    listGroups () {
      return this.clients.groups
    },
    listIncome () {
      return this.clients.income
    },
    listSpecialty () {
      return this.clients.specialty
    },
    listRole () {
      return this.clients.role
    },

  },
}
</script>
