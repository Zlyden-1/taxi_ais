<template>
<base-table>
    <thead>
        <th/>
        <th v-for="name in columnNamesSet" :key="name">
            {{ name }}
        </th>
    </thead>
    <tr v-for="driver in Object.keys(formattedRentList)" :key="driver">
        <th>
            {{ driver }}
        </th>
        <td v-for="name in columnNamesSet" :key="name">
            <span v-if="formattedRentList[driver][name]">{{ formattedRentList[driver][name] }}</span>
            <span v-else>0</span>
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
        balances: {
            type: Array,
            required: true,
        },
    },
    setup(props) {
        const allDrivers = props.rents.map((rent) => rent.driver.name);
        const uniqueDrivers = new Set(allDrivers);
        const datesSet = new Set(props.rents.map((rent) => rent.payment_date));
        const columnNamesSet = datesSet.add("Итого").add("Баланс")
        const formattedRentList = {};
        const totalSumByDrivers = {};
        const totalSumByDays = {};
        for (const driver of uniqueDrivers) {
            formattedRentList[driver] = {};
            totalSumByDrivers[driver] = 0;
        }
        for (const date of datesSet) {
            totalSumByDays[date] = 0;
        }
        for (const rent of props.rents) {
            const driver = formattedRentList[rent.driver.name];
            if (Object.keys(driver).includes(rent.payment_date)) {
                driver[rent.payment_date] += rent.summ;
            }
            else {
                driver[rent.payment_date] = rent.summ;
            }
            totalSumByDrivers[rent.driver.name] += rent.summ;
            totalSumByDays[rent.payment_date] += rent.summ;
            totalSumByDays["Итого"] += rent.summ;
        }
        for (const driver of uniqueDrivers) {
            formattedRentList[driver]["Итого"] = totalSumByDrivers[driver];
            const balance = props.balances.find((el) => el.driver.name === driver);
            if (balance) {
                formattedRentList[driver]["Баланс"] = props.balances.find((el) => el.driver.name === driver).balance;
            }
        }
        formattedRentList["Итого"] = totalSumByDays;
        formattedRentList["Итого"]["Баланс"] = ' ';
        return { formattedRentList, columnNamesSet };
    }
}
</script>
    
<style scoped></style>