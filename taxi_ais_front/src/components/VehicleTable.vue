<template>
<base-table v-if="vehicleList.length>0">
    <thead>
        <th>VIN</th>
        <th>Марка</th>
        <th>Модель</th>
        <th>Номер</th>
        <th>Статус ТС</th>
        <th>Локация</th>
        <th>Водитель</th>
        <th>Добавить выплату по аренде</th>
        <th>Действия</th>
    </thead>
    <tbody>
        <tr v-for="vehicle in vehicleList" :key="vehicle.VIN">
            <td>{{ vehicle.VIN }}</td>
            <td>{{ vehicle.vehicle_type.brand }}</td>
            <td>{{ vehicle.vehicle_type.model }}</td>
            <td>{{ vehicle.license_plate }}</td>
            <td>{{ vehicle.status.name }}</td>
            <td>{{ vehicle.location.place }}</td>
            <td v-if="vehicle.driver !== null && vehicle.driver !== undefined">{{ vehicle.driver.name }}</td>
            <td v-else>Водитель не назначен</td>
            <td>Тут будет аренда...</td>
            <td>
                <div class="action__buttons">
                    <base-button
                        @click="$router.push(`/references/vehicle/${vehicle.VIN}`)"
                    >
                        Подробности
                    </base-button>
                    <base-button
                        style="margin-top: 5px;"
                        @click="$emit('delete', vehicle.VIN)"
                    >
                        Удалить
                    </base-button>
                </div>
            </td>
        </tr>
    </tbody>
</base-table>
<h4 v-else>Транспортных средств пока нет...</h4>
</template>
    
<script>
export default {
    props: {
        vehicleList: {
            type: Array,
            default: () => []
        }
    },
}
</script>
    
<style scoped>

</style> 