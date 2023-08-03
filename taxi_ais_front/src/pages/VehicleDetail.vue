<template>
    <base-header>{{ driver.name }} </base-header>
    <div class="table__container">
        <driver-details-table
            :driver="driver"
            :verbose="fieldVerboseNames"
            @updateVehicle="updateVehicle"
            @commit="commitVehicleChanges"
        />
    </div>
    </template>
    
    <script>
    import axios from 'axios';
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
                    driver: ''
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
                    driver: 'Водитель'
                },
            }
        },
        beforeMount() {
            this.fetchVehicle()
        },
        methods: {
            async fetchVehicle() {
                this.isVehicleLoading = true;
                const responce = await axios.get(`http://127.0.0.1:8000/api/references/driver/${this.$route.params.id}`);
                this.driver = responce.data;
                this.isVehicleLoading = false;
            },
            updateVehicle(changedValue) {
                this.changes[changedValue.key_] = changedValue.value
            },
            async commitVehicleChanges() {
                this.isVehicleLoading = true;
                await axios.patch(`http://127.0.0.1:8000/api/references/driver/${this.$route.params.id}`, this.changes);
                await this.fetchVehicle();
            }
        }
    }
    </script>
    
    <style scoped>
    .table__container {
        padding: 15px;
    }
    </style>