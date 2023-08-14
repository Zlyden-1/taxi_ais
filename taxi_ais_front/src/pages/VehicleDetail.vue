<template>
    <base-header>{{ vehicle.vehicle_type.name }} {{ vehicle.license_plate }}</base-header>
    <div class="table__container" v-if="!isVehicleLoading">
        <vehicle-details-table
            :vehicle="vehicle"
            :verbose="fieldVerboseNames"
            :options="options"
            @updateVehicle="updateVehicle"
            @commit="commitVehicleChanges"
        />
    </div>
    <div v-else>
        Загрузка...
    </div>
    </template>
    
    <script>
    import requests from '@/api/api';
    import VehicleDetailsTable from '@/components/VehicleDetailsTable';
    
    export default {
        components: {
            VehicleDetailsTable,
        },
        data() {
            return {
                isVehicleLoading: false,
                changes: {},
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
                    driver: '',
                    usage_history: '',
                },
                fieldVerboseNames: {
                    VIN: 'VIN',
                    license_plate: 'Гос. номер',
                    registration_certificate_id: '№ СТС',
                    vehicle_passport_id: '№ ПТС',
                    engine_id: '№ двигателя',
                    color: 'Цвет',
                    leasing_contract_id: '№ ДЛ',
                    insurance_policy_series: 'Серия полиса',
                    insurance_policy_id: '№ полиса',
                    leasing_contract_date: 'Дата ДЛ',
                    lessor: 'Лизингодатель',
                    manufacture_year: 'Год выпуска',
                    rent_type: 'Тип аренды',
                    vehicle_type: 'Тип ТС',
                    status: 'Статус',
                    location: 'Место базирования',
                    driver: 'Водитель',
                    usage_history: 'История использования',
                },
                options: {
                    rent_type: [
                        { value: "А", name: "Аренда" },
                        { value: "В", name: "Выкуп" }
                    ],
                    vehicle_type: [],
                    status: [],
                    location: [],
                    driver: []
                }
            }
        },
        beforeMount() {
            this.fetchUsageHistory();
            this.fetchOptions();
            this.fetchVehicle();
        },
        methods: {
            async fetchVehicle() {
                this.isVehicleLoading = true;
                const responce = await requests.getVehicle(this.$route.params.VIN);
                const vehicle = responce.data;
                if (vehicle.rent_type) {
                    vehicle.rent_type = {value: vehicle.rent_type, name: ''};
                    const rent_type_name = this.options.rent_type.find((type) => type.value === vehicle.rent_type.value).name;
                    vehicle.rent_type.name = rent_type_name
                }
                for (const [key, value] of Object.entries(vehicle)) {
                    if (value == null) {
                        this.vehicle[key] = '';
                    }
                    else {
                        this.vehicle[key] = value;
                    }
                }
                this.isVehicleLoading = false;
            },
            updateVehicle(changedValue) {
                this.changes[changedValue.key_] = changedValue.value
            },
            async commitVehicleChanges() {
                this.isVehicleLoading = true;
                await requests.patchVehicle(this.$route.params.VIN, this.changes);
                await this.fetchVehicle();
                this.changes = {};
            },
            async fetchOptions() {
                const vehicleTypeRequest = requests.getVehicleTypeOptions();
                const statusRequest = requests.getVehicleStatusOptions();
                const locationRequest = requests.getVehicleLocationOptions();
                const driverRequest = requests.getDriverOptions();
                const responces = await Promise.allSettled([vehicleTypeRequest, statusRequest, locationRequest, driverRequest]);
                [this.options.vehicle_type, 
                this.options.status, 
                this.options.location,
                this.options.driver] = responces.map(responce => responce.value.data);
                this.options.driver.unshift({name: 'Нет', value: ''}, this.vehicle.driver);
            },
            async fetchUsageHistory() {
                this.vehicle.usage_history = (await requests.getVehicleHistory(this.$route.params.VIN)).data;
            }
        }
    }
    </script>
    
    <style scoped>
    .table__container {
        padding: 15px;
    }
    </style>