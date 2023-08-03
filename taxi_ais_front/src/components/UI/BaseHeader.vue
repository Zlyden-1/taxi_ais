<template>
    <div class="header">
        <span class="home" @click="$router.push('/')">В меню</span>
        <h1 class="text">
            <slot></slot>
        </h1>
        <div class="placeholder"/>
    </div>
</template>

<script>
export default {
    name: 'base-header',
}
</script>

<style scoped>
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-sizing: border-box;
    background-color: teal;
    padding: 0 20px 0 20px;
}
.text {
    color: white;
    text-align: center;
    align-self: center;
}
.home {
    color: white;
    text-align: left;
    width: 33vw;
    cursor: pointer;
}
.placeholder {
    justify-self: stretch;
    width: 33vw;
    height: auto;
}
</style>