<template>
<base-table v-if="drivers_list.length > 0">
    <thead>
        <tr>
            <th>id</th>
            <th>Фамилия</th>
            <th>Имя</th>
            <th>Отчество</th>
            <th>ФИО</th>
            <th>Статус</th>
            <th>Действия</th>
        </tr>
    </thead>
    <tbody>
        <tr 
            v-for="driver in drivers_list"
            :key="driver.id"
        >
            <td
                v-for="value in Object.values(driver)"
                :key="value"
            >
                <div v-if="value === true">Активен</div>
                <div v-else-if="value === false">Неактивен</div>
                <div v-else>{{ value }}</div> 
            </td>
            <td>
                <div class="action__buttons">
                    <base-button
                        @click="$router.push(`/references/driver/${driver.id}`)"
                    >
                        Подробности
                    </base-button>
                    <base-button 
                        @click="$emit('delete', driver)"
                        style="margin-top: 5px;"
                    >
                        Удалить
                    </base-button>
                </div>
            </td>
        </tr>
    </tbody>
</base-table>
<div 
    v-else
    style="display: flex;"
>
    <h3 style="align-self: center; margin: auto;">Водителей пока нет</h3>
</div>
</template>

<script>
export default {
    props: {
        drivers_list: {
            type: Array,
            required: true
        }
    }
}
</script>

<style>

</style>