<template>
    <base-header>Меню</base-header>
    <div class="link__container">
        <base-button 
            @click="$router.push('/references/drivers')"
        >
            Водители
        </base-button>
        <base-button 
            @click="$router.push('/references/vehicles')"
            style="margin-top: 15px;"
        >
            Транспортные средства
        </base-button>
        <base-button 
            @click="$router.push('/accounting/rent')"
            style="margin-top: 15px;"
        >
            Аренда
        </base-button>
    </div>
</template>

<script>
export default {
    
}
</script>

<style>
.link__container {
    padding: 15px;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}
</style>