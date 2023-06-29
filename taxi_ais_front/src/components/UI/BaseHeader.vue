<template>
    <div class="header">
        <h1 class="text">
            <slot></slot>
        </h1>
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
    justify-content: center;
    box-sizing: border-box;
    background-color: teal;
}
.text {
    color: white;
}
</style>