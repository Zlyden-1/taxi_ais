<template>
<base-table>
    <thead>
        <th/>
        <th v-for="date in datesSet" :key="date">
            {{ date }}
        </th>
    </thead>
    <tr v-for="driver in Object.keys(formattedRentList)" :key="driver">
        <th>
            {{ driver }}
        </th>
        <td v-for="date in Object.keys(formattedRentList[driver])" :key="date">
            {{ formattedRentList[driver][date] }}
        </td>
    </tr>
</base-table>
</template>
    
<script>
export default {
    props: {
        rents: {
            type: Array,
            required: true,
        },
    },
    setup(props) {
        const allDrivers = props.rents.map((rent) => rent.driver.name);
        const uniqueDrivers = new Set(allDrivers);
        const formattedRentList = {};
        for (const driver of uniqueDrivers) {
            formattedRentList[driver] = {};
        }
        for (const rent of props.rents) {
            const driver = formattedRentList[rent.driver.name];
            if (Object.keys(driver).includes(rent.payment_date)) {
                driver[rent.payment_date] += rent.summ;
            }
            else {
                driver[rent.payment_date] = rent.summ;
            }
        }
        const datesSet = new Set(props.rents.map((rent) => rent.payment_date));
        return { formattedRentList, datesSet };
    }
}
</script>
    
<style scoped></style>