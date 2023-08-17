<template>
<base-header>Аренда</base-header>
<base-dialog v-model:show="dialogVisible">
    <add-rent-form/>
</base-dialog>
<div class="content">
    <div class="button__container">
        <base-button style="margin-left: auto;" @click="showDialog">Добавить выплату</base-button>
    </div>
    <div class="table__container" 
        v-if="!isRentsLoading"
    >
        <rent-table
            :rents="rentList"
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
        showDialog() {
            this.dialogVisible = true;
        },
    },
    mounted() {
        this.fetchRent();
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
.table__container {
    margin-top: 15px;
}
</style>
