<template>
    <base-header>
        <h4>Добавить ТС</h4>
    </base-header>
    <div class="container">
        <form @submit.prevent>
            <fieldset style="margin-top: 0;">
                <legend>Номера</legend>
                <fieldset>
                    <legend>VIN</legend>
                    <base-input v-model="vehicle.VIN" required type="text" placeholder="VIN" />
                </fieldset>
                <fieldset>
                    <legend>Гос. номер</legend>
                    <base-input v-model="vehicle.license_plate" required type="text" placeholder="Гос. номер" />
                </fieldset>
                <fieldset>
                    <legend>Серия полиса</legend>
                    <base-input v-model="vehicle.insurance_policy_series" required type="text" placeholder="Серия полиса" />
                </fieldset>
                <fieldset>
                    <legend>Номер полиса</legend>
                    <base-input v-model="vehicle.insurance_policy_id" required type="text" placeholder="Номер полиса" />
                </fieldset>
                <fieldset>
                    <legend>№ СТС</legend>
                    <base-input v-model="vehicle.registration_certificate_id" required type="text" placeholder="№ СТС" />
                </fieldset>
                <fieldset>
                    <legend>№ ПТС</legend>
                    <base-input v-model="vehicle.vehicle_passport_id" required type="text" placeholder="№ ПТС" />
                </fieldset>
                <fieldset>
                    <legend>№ двигателя</legend>
                    <base-input v-model="vehicle.engine_id" required type="text" placeholder="№ двигателя" />
                </fieldset>
            </fieldset>
            <fieldset>
                <legend>Общая информация о машине</legend>
                <fieldset>
                    <legend>Водитель (если есть)</legend>
                    <base-select v-model="vehicle.driver" :options="driverOptions"/>
                </fieldset>
                <fieldset>
                    <legend>Цвет</legend>
                    <base-input v-model="vehicle.color" required type="text" placeholder="Цвет" />
                </fieldset>
                <fieldset>
                    <legend>Тип ТС</legend>
                    <base-select v-model="vehicle.vehicle_type" :options="vehicleTypeOptions"/>
                </fieldset>
                <fieldset>
                    <legend>Год выпуска</legend>
                    <base-input v-model="vehicle.manufacture_year" required type="number" placeholder="Год выпуска"/>
                </fieldset>
                <fieldset>
                    <legend>Статус</legend>
                    <base-select v-model="vehicle.status" :options="statusOptions"/>
                </fieldset>
                <fieldset>
                    <legend>Место базирования</legend>
                    <base-select v-model="vehicle.location" :options="locationOptions"/>
                </fieldset>
                <fieldset>
                    <legend>Тип использования</legend>
                    <base-select v-model="vehicle.rent_type" :options="rentTypeOptions"/>
                </fieldset>
            </fieldset>
            <fieldset>
                <legend>Лизинг</legend>
                <fieldset>
                    <legend>Лизингодатель</legend>
                    <base-input v-model="vehicle.lessor" required type="text" placeholder="№ ДЛ" />
                </fieldset>
                <fieldset>
                    <legend>№ ДЛ</legend>
                    <base-input v-model="vehicle.leasing_contract_id" required type="text" placeholder="№ ДЛ" />
                </fieldset>
                <fieldset>
                    <legend>Дата ДЛ</legend>
                    <base-input v-model="vehicle.leasing_contract_date" required type="date" placeholder="Дата ДЛ" />
                </fieldset>
            </fieldset>
            <base-button style="margin-top: 15px; align-self: flex-end;" @click="createVehicle">
                Добавить
            </base-button>
        </form>
    </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            vehicle: {
                VIN: '',
                license_plate: '',
                registration_certificate_id: '',
                vehicle_passport_id: '',
                engine_id: '',
                color: '',
                leasing_contract_id: '',
                insurance_policy_series: '',
                insurance_policy_id: '',
                leasing_contract_date: '',
                lessor: '',
                manufacture_year: '',
                rent_type: '',
                vehicle_type: '',
                status: '',
                location: '',
                driver: ''
            },
            rentTypeOptions: [{value: "А", name: "Аренда"}, {value: "В", name: "Выкуп"}],
            vehicleTypeOptions: [],
            statusOptions: [],
            locationOptions: [],
            driverOptions: [],
        }
    },
    methods: {
        createVehicle() {
            this.$emit('create', this.vehicle);
            console.log(this.vehicle);
            this.vehicle = {
                VIN: '',
                license_plate: '',
                registration_certificate_id: '',
                vehicle_passport_id: '',
                engine_id: '',
                color: '',
                leasing_contract_id: '',
                insurance_policy_series: '',
                insurance_policy_id: '',
                leasing_contract_date: '',
                lessor: '',
                manufacture_year: '',
                rent_type: '',
                vehicle_type: '',
                status: '',
                location: '',
                driver: ''
            };
        },
        async fetchOptions() {
            const vehicleTypeRequest = axios.get('http://127.0.0.1:8000/api/references/vehicles/types/');
            const statusRequest = axios.get('http://127.0.0.1:8000/api/references/vehicles/statuses/');
            const locationRequest = axios.get('http://127.0.0.1:8000/api/references/vehicles/locations/');
            const driverRequest = axios.get('http://127.0.0.1:8000/api/references/drivers/options/');
            const responces = await Promise.allSettled([vehicleTypeRequest, statusRequest, locationRequest, driverRequest]);
            [this.vehicleTypeOptions, 
            this.statusOptions, 
            this.locationOptions, 
            this.driverOptions] = responces.map(responce => responce.value.data);
        }
    },
    mounted() {
        this.fetchOptions()
    }
}
</script>

<style scoped>
form {
    display: flex;
    flex-direction: column;
}
fieldset {
    padding: 0 15px 15px 15px;
    border-color: teal;
    margin-top: 10px;
}
legend {
    color: teal;
}
.container {
    padding: 10px;
}
</style>