<template>
    <base-header>
        <h4>Добавить водителя</h4>
    </base-header>
    <div class="container">
        <form @submit.prevent>
            <fieldset style="margin-top: 0;">
                <legend>ФИО</legend>
                <base-input v-model="driver.second_name" required type="text" placeholder="Фамилия" />
                <base-input v-model="driver.first_name" required type="text" placeholder="Имя" />
                <base-input v-model="driver.patronimic" required type="text" placeholder="Отчество" />
                <base-input v-model="driver.name" required type="text" placeholder="ФИО" />
            </fieldset>
            <fieldset>
                <legend>Документы</legend>
                <fieldset>
                    <legend>Паспортные данные</legend>
                    <base-input v-model="driver.citizenship" required type="text" placeholder="Гражданство" />
                    <base-input v-model="driver.passport_id" required type="text" placeholder="Номер паспорта" />
                    <fieldset>
                        <legend>Дата выдачи паспорта</legend>
                        <base-input v-model="driver.passport_issue_date" required type="date" />
                    </fieldset>
                    <fieldset>
                        <legend>Дата рождения</legend>
                        <base-input v-model="driver.date_of_birth" required type="date" />
                    </fieldset>
                    <base-input v-model="driver.place_of_birth" required type="text" placeholder="Место рождения" />
                    <base-input v-model="driver.residence_place" required type="text" placeholder="Место жительства" />
                </fieldset>
                <fieldset>
                    <legend>Водительские права</legend>
                    <base-input v-model="driver.driving_license_id" required type="text" placeholder="Номер прав" />
                    <base-input v-model="driver.driving_license_category" required type="text"
                        placeholder="Категория прав" />
                    <fieldset>
                        <legend>Срок действия</legend>
                        <base-input v-model="driver.driving_license_validity_period" required type="date" />
                    </fieldset>
                </fieldset>
            </fieldset>
            <fieldset>
                <legend>Контакты</legend>
                <base-input v-model="driver.phone_number" required type="tel" placeholder="Номер телефона" />
                <base-input v-model="driver.telegram_id" required type="text" placeholder="Тег в telegram" />
            </fieldset>
            <fieldset>
                <legend>Прочее</legend>
                <base-input v-model.number="driver.deposit" required type="number" placeholder="Залог" />
                <base-select v-model="driver.status" required :options="driverStatusOptions" />
                <base-input v-model="driver.comment" required type="text" placeholder="Комментарий" />
            </fieldset>
            <base-button style="margin-top: 15px; align-self: flex-end;" @click="createDriver">
                Добавить
            </base-button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            driverStatusOptions: [
                { value: true, name: "Активен" },
                { value: false, name: "Неактивен" }
            ],
            driver: {
                second_name: '',
                first_name: '',
                patronimic: '',
                name: '',
                citizenship: '',
                passport_id: '',
                passport_issue_date: '',
                date_of_birth: '',
                place_of_birth: '',
                residence_place: '',
                phone_number: '',
                driving_license_id: '',
                driving_license_category: '',
                driving_license_validity_period: '',
                deposit: '',
                status: '',
                comment: '',
                telegram_id: ''
            }
        }
    },
    methods: {
        createDriver() {
            this.$emit('create', this.driver)
            this.driver = {
                second_name: '',
                first_name: '',
                patronimic: '',
                name_: '',
                citizenship: '',
                passport_id: '',
                passport_issue_date: '',
                date_of_birth: '',
                place_of_birth: '',
                residence_place: '',
                phone_number: '',
                driving_license_id: '',
                driving_license_category: '',
                driving_license_validity_period: '',
                deposit: '',
                status_: '',
                comment: '',
                telegram_id: ''
            }
        }
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