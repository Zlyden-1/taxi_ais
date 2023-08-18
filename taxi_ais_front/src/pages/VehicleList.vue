<template>
<base-header>Список ТС</base-header>
<base-dialog v-model:show="dialogVisible">
    <create-vehicle-form @create="createVehicle"/>
</base-dialog>
<div class="content">
    <div class="button__container">
        <base-button style="margin-left: auto;" @click="showDialog">Добавить ТС</base-button>
    </div>
    <div class="table__container">
        <vehicle-table :vehicleList="vehicleList" @delete="deleteVehicle"/>
    </div>
</div>
</template>

<script>
import requests from '@/api/api'
import VehicleTable from '@/components/VehicleTable';
import CreateVehicleForm from '@/components/CreateVehicleForm';

export default {
    components: {
        VehicleTable,
        CreateVehicleForm,
    },
    data() {
        return {
            vehicleList: [],
            dialogVisible: false,
            isVehiclesLoading: false,
        }
    },
    methods: {
        async fetchVehicles() {
            this.isVehiclesLoading = true;
            const responce = await requests.getVehicles();
            this.vehicleList = responce.data;
            this,this.isVehiclesLoading = false;
        },
        showDialog() {
            this.dialogVisible = true;
        },
        async createVehicle(vehicle) {
            this.isVehiclesLoading = true;
            this.dialogVisible = false;
            try{
                const newVehicle = (await requests.postCreateVehicle(vehicle)).data;
                this.vehicleList.push(newVehicle);
            } catch(e) {
                alert(e)
            }
            this.isDriversLoading = false;
        },
        async deleteVehicle(vehicleVIN) {
            this.isVehiclesLoading = true;
            try {
                await requests.deleteVehicle(vehicleVIN);
            } catch (e) {
                alert('Возникла ошибка! Попробуйте обновить страницу и сообщите об ошибке.')
            }
            this.fetchVehicles()
        }
    },
    beforeMount() {
        this.fetchVehicles();
    },
}
</script>

<style scoped>
.content {
    padding: 15px;
}

.button__container {
    display: flex;
    align-items: flex-end;
}

.table__container {
    margin-top: 15px;
}
</style>
