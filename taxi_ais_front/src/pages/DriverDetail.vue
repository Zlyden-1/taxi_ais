<template>
<base-header>Водитель {{ driver.name }} </base-header>
<div class="table__container">
    <driver-details-table
        :driver="driver"
        :verbose="fieldVerboseNames"
        @updateDriver="updateDriver"
        @commit="commitDriverChanges"
    />
</div>
</template>

<script>
import requests from '@/api/api'
import DriverDetailsTable from '@/components/DriverDetailsTable';

export default {
    components: {
        DriverDetailsTable,
    },
    data() {
        return {
            isDriverLoading: false,
            changes: {},
            driver: {
                id: "",
                second_name: "",
                patronimic: "",
                first_name: "",
                citizenship: "",
                name: "",
                passport_issue_date: "",
                passport_id: "",
                place_of_birth: "",
                date_of_birth: "",
                phone_number: "",
                residence_place: "",
                driving_license_category: "",
                driving_license_id: "",
                deposit: "",
                driving_license_validity_period: "",
                comment: "",
                telegram_id: "",
                status: "",
            },
            fieldVerboseNames: {
                id: "id",
                second_name: "Фамилия",
                patronimic: "Отчество",
                first_name: "Имя",
                citizenship: "Гражданство",
                name: "ФИО",
                passport_issue_date: "Дата выдачи паспорта",
                passport_id: "Номер паспорта",
                place_of_birth: "Место рождения",
                date_of_birth: "Дата рождения",
                phone_number: "Номер телефона",
                residence_place: "Место жительста",
                driving_license_category: "Категория прав",
                driving_license_id: "Номер прав",
                deposit: "Залог",
                driving_license_validity_period: "Срок действия прав",
                comment: "Комментарий",
                telegram_id: "Тег в telegram",
                status: "Статус",
            },
        }
    },
    beforeMount() {
        this.fetchDriver()
    },
    methods: {
        async fetchDriver() {
            this.isDriverLoading = true;
            const responce = await requests.getDriver(this.$route.params.id);
            this.driver = responce.data;
            this.isDriverLoading = false;
        },
        updateDriver(changedValue) {
            this.changes[changedValue.key_] = changedValue.value
        },
        async commitDriverChanges() {
            this.isDriverLoading = true;
            await requests.patchDriver(this.$route.params.id, this.changes);
            await this.fetchDriver();
        }
    }
}
</script>

<style scoped>
.table__container {
    padding: 15px;
}
</style>