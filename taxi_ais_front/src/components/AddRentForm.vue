<template>
<base-header>
    <h4>Внести выплату</h4>
</base-header>
<div class="container">
    <form @submit.prevent>
        <fieldset>
            <legend>Водитель</legend>
            <base-select v-model="rent.driver" :options="driverOptions" required/>
        </fieldset>
        <base-input v-model="rent.summ" required type="number" placeholder="Сумма выплаты"/>
        <base-input v-model="rent.comment" required type="text" placeholder="Комментарий"/>
        <base-button style="margin-top: 15px; align-self: flex-end;" @click="createRent">
                Добавить
        </base-button>
    </form>
</div>
</template>
    
<script>
import requests from '@/api/api';

export default {
    data() {
        return {
            driverOptions: [],
            rent: {
                driver: '',
                summ: '',
                comment: ''
            }
        }
    },
    methods: {
        async fetchOptions() {
            const responce = await requests.getDriverOptionsForRents();
            this.driverOptions = responce.data;
        },
        async createRent() {
            
        }
    },
    mounted() {
        this.fetchOptions(); 
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