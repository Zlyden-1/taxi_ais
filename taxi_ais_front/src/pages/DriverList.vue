<template>
<base-header>Список водителей</base-header>
<base-dialog v-model:show="dialogVisible">
    <create-driver-form @create="createDriver"/>
</base-dialog>
<div class="content">
    <div class="button__container">
        <base-button style="margin-left: auto;" @click="showDialog">Добавить водителя</base-button>
    </div>
    <div class="table__container" 
        v-if="!isDriversLoading"
    >
        <drivers-table
            :drivers_list="drivers_list"
            @delete="deleteDriver"
        />
    </div>
    <div v-else>
        Загрузка...
    </div>
</div>
</template>

<script>
import requests from '@/api/api';
import CreateDriverForm from '@/components/CreateDriverForm';
import DriversTable from "@/components/DriversTable";

export default {
    components: {
        CreateDriverForm,
        DriversTable,
    },
    data() {
        return {
            drivers_list: [],
            isDriversLoading: false,
            dialogVisible: false,
        }
    },
    methods: {
        async fetchDrivers() { 
            this.isDriversLoading = true;
            const data = await requests.getDrivers();
            this.drivers_list = data.data;
            this.isDriversLoading = false;
        },
        async createDriver(driver) {
            this.isDriversLoading = true;
            this.dialogVisible = false;
            const response = await requests.postCreateDriver(driver);
            const newDriver = response.data;
            this.drivers_list.push(newDriver);
            this.isDriversLoading = false;
        },
        async deleteDriver(driver) {
            this.isDriversLoading = true;
            const response = await requests.deleteDriver(driver.id);
            if (response.status === 204) {
                this.drivers_list = this.drivers_list.filter(p => p.id !== driver.id);
            }
            else {
                alert('Ошибка при удалении. Обновите страницу или сообщите об ошибке.');
            }
            this.isDriversLoading = false;
        },
        showDialog() {
            this.dialogVisible = true;
        },
    },
    beforeMount() {
        this.fetchDrivers();
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
