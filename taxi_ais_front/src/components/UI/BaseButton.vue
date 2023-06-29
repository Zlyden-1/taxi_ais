<template>
    <button class="button">
        <slot></slot>
    </button>
</template>

<script>
export default {
    name: "base-button"
}
</script>

<style scoped>
.button {
    padding: 10px 15px;
    background: none;
    color: teal;
    border: 4px solid teal;
}
</style>