<template>
    <div class="apps">
       

        <main-screen v-if="currentStep==0"></main-screen>
        <is-leader :EventId="EventId"  v-if="currentStep==1"></is-leader>
        <data-user-screen :EventId="EventId"  v-if="currentStep==2"></data-user-screen>
        <await-screen :EventId="EventId"  v-if="currentStep==3"></await-screen>
        <number-screen :EventId="EventId"  v-if="currentStep==4"></number-screen>
        <clients-list-screen :EventId="EventId"  v-if="currentStep==5"></clients-list-screen>
    </div>
</template>

<script>
    import {useRoute} from 'vue-router'
    import  stepsStore  from "@/store/step";
    import  mainScreen  from "@/components/mainScreen";
    import  dataUserScreen  from "@/components/dataUserScreen";
    import  awaitScreen  from "@/components/awaitScreen";
    import  numberScreen  from "@/components/numberScreen";
    import  clientsListScreen  from "@/components/clientsListScreen";
    import  isLeader  from "@/components/isLeader";
    import { useTelegram } from '@/services/telegram'
    export default {
        name: 'HomeView',
        components:{mainScreen,dataUserScreen,awaitScreen,numberScreen,clientsListScreen, isLeader},
        data() {
            return {

            }
        },
        setup() {
            const route = useRoute()
            const steps = stepsStore();
            console.log(route.query)
            let EventId = null;
            if (route.query.event_id) {
                 EventId = route.query.event_id

            }
            const { tg } = useTelegram()
            return {EventId, steps, tg}
        },
        async mounted(){
            await this.steps.getDic()
            if (this.tg) {

                if (this.tg.initDataUnsafe.start_param)
                    this.EventId = this.tg.initDataUnsafe?.start_param
            }
            console.log(this.EventId)
            if (this.EventId) {
                console.log('mounted',this.EventId)
                await this.steps.detailEvents(this.EventId)


                 await this.steps.detailUsers(this.EventId)
            }
        },
        computed:{
            currentStep(){
                return this.steps.step
            },
            getVisibleSelect() {
                return this.steps.visibleSelect;
            },
            getVisibleSelectTg() {
                return this.steps.visibleSelectTg;
            }
        },
        methods:{
            onClose(){
                if (this.tg) {
                    this.tg.close();
                }
            },
            onChangeStep(){
                if (this.getVisibleSelectTg) {
                    this.steps.setVisibleSelectTg(false)
                    return
                }
                if (this.getVisibleSelect) {
                    this.steps.setVisibleSelect(false)
                } else

                    this.steps.decrimentStep()


            }
        }

    }
</script>
