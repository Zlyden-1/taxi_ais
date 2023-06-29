<template>
<base-header>Список водителей</base-header>
<div>
    
</div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            drivers_list: [],
        }
    },
    methods: {
        async fetchDrivers() {
            this.drivers_list = await axios.get('');
        }
    },
    mounted() {
        this.fetchDrivers();
    }
}
</script>

<style scoped>
</style>
