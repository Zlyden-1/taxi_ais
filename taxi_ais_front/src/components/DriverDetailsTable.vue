<template>
<form @submit.prevent>
    <base-table>
        <tr 
            v-for="key in Object.keys(driver)"
            :key="key"
        >
            <th>{{ verbose[key] }}</th>
            <td v-if="key === 'id'">
                <base-input
                    disabled
                    :modelValue="driver[key]"
                    style="margin-top: 0;"
                />
            </td>
            <td
                v-else-if="selectFields.includes(key)"
            >
                <key-value-select
                    @update="updateField"
                    :key_="key"
                    :modelValue="driver[key]"
                    :options="driverStatusOptions"
                    style="margin-top: 0;"
                />
            </td>
            <td v-else-if="dateFields.includes(key)">
                <key-value-input
                    @update="updateField"
                    :key_="key"
                    :modelValue="driver[key]"
                    style="margin-top: 0;"
                    :type="'date'"
                />
            </td>
            <td v-else-if="numberFields.includes(key)">
                <key-value-input
                    @update="updateField"
                    :key_="key"
                    :modelValue="driver[key]"
                    style="margin-top: 0;"
                    :type="'number'"
                />
            </td>
            <td v-else>
                <key-value-input
                    @update="updateField"
                    :key_="key"
                    :modelValue="driver[key]"
                    style="margin-top: 0;"
                    :type="'text'"
                />
            </td>
        </tr> 
    </base-table>
    <div style="display: flex; align-items: end;">
        <base-button 
            @click="$emit('commit')"
            style="margin-top: 15px; margin-left: auto;"
        >
            Сохранить изменения
        </base-button>
    </div>
</form>
</template>

<script>
export default {
    props: {
        driver: {
            type: Object,
            required: true
        },
        verbose: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            dateFields: ['passport_issue_date', 'date_of_birth', 'driving_license_validity_period'],
            numberFields: ['deposit'],
            selectFields: ['status'],
            driverStatusOptions: [
                {value: true, name: "Активен"},
                {value: false, name: "Неактивен"}
            ],
        }
    },
    methods: {
        updateField(event) {
            this.$emit('updateDriver', event)
        }
    }
}
</script>

<style scoped>

</style>