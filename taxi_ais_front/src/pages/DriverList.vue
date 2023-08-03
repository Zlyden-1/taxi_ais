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
import axios from 'axios';
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
            const data = await axios.get('http://127.0.0.1:8000/api/references/drivers/');
            this.drivers_list = data.data;
            this.isDriversLoading = false;
        },
        async createDriver(driver) {
            this.isDriversLoading = true;
            this.dialogVisible = false;
            const newDriver = (await axios.post('http://127.0.0.1:8000/api/references/drivers/create/', driver)).data;
            this.drivers_list.push(newDriver);
            this.isDriversLoading = false;
        },
        async deleteDriver(driver) {
            this.isDriversLoading = true;
            const response = await axios.delete(`http://127.0.0.1:8000/api/references/driver/${driver.id}`)
            if (response.status === 204) {
                this.drivers_list = this.drivers_list.filter(p => p.id !== driver.id)
            }
            else {
                alert('памагити')
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
