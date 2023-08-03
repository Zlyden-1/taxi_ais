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
        <vehicle-table :vehicleList="vehicleList" />
    </div>
</div>
</template>

<script>
import axios from 'axios';
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
            const responce = await axios.get('http://127.0.0.1:8000/api/references/vehicles/');
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
                const newVehicle = (await axios.post('http://127.0.0.1:8000/api/references/vehicles/create/', vehicle)).data;
                this.vehicleList.push(newVehicle);
            } catch(e) {
                console.log(e)
            }
            this.isDriversLoading = false;
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
