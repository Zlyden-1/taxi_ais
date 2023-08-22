<template>
<base-header>Аренда</base-header>
<base-dialog v-model:show="dialogVisible">
    <add-rent-form @create="createRent"/>
</base-dialog>
<div class="content">
    <div class="button__container">
        <base-button style="margin-left: auto;" @click="showDialog">Добавить выплату</base-button>
    </div>
    <div class="dates__container">
        <h4 style="text-align: center;">
            Данные по аренде с 
            <inline-input v-model="startDate" :max="endDate" type="date"/> 
            по 
            <inline-input v-model="endDate" :min="startDate" type="date"/>
        </h4>
    </div>
    <div class="table__container" 
        v-if="!isRentsLoading"
    >
        <rent-table
            :rents="rentList"
            :balances="balanceList"
        />
    </div>
    <div v-else>
        Загрузка...
    </div>
</div>
</template>

<script>
import requests from '@/api/api.js';
import RentTable from '@/components/RentTable.vue';
import AddRentForm from '@/components/AddRentForm.vue';

export default {
    components: {
        RentTable,
        AddRentForm,
    },
    data() {
        return {
            startDate: '',
            endDate: '',
            rentList: [],
            balanceList: [],
            isRentsLoading: false,
            dialogVisible: false,
        }
    },
    methods: {
        async fetchRent(startDate, endDate) {
            this.isRentsLoading = true;
            this.rentList = (await requests.getRents(startDate, endDate)).data;
            this.isRentsLoading = false;
        },
        async createRent(rentData) {
            this.isRentsLoading = true;
            await requests.postCreateRent(rentData);
            await this.fetchRent();
        },
        async fetchBalances(startDate, endDate) {
            this.isRentsLoading = true;
            this.balanceList = (await requests.getBalances(startDate, endDate)).data;
            this.isRentsLoading = false;
        },
        showDialog() {
            this.dialogVisible = true;
        },
    },
    watch: { // eslint-disable-next-line
        startDate(newDate, oldDate) {
            this.fetchRent(newDate, this.endDate);
        }, // eslint-disable-next-line
        endDate(newDate, oldDate) {
            this.fetchRent(this.startDate, newDate);
        },
    },
    async beforeMount() {
        await this.fetchRent();
        await this.fetchBalances();
        const firstDate = new Date(this.rentList[0].payment_date);
        const secondDate = new Date(this.rentList.at(-1).payment_date);
        firstDate.setDate(firstDate.getDate() - firstDate.getDay() + 1);
        secondDate.setDate(firstDate.getDate() - firstDate.getDay() + 7);
        this.startDate = firstDate.toLocaleDateString('en-ca');
        this.endDate = secondDate.toLocaleDateString('en-ca');
    }
}
</script>

<style scoped>
.content {
    padding: 15px;
}
.button__container{
    display: flex;
    align-items: flex-end;
}
.dates__container {
    display: flex;
    align-items: center;
    justify-content: space-around;
}
.table__container {
    margin-top: 15px;
}
</style>
