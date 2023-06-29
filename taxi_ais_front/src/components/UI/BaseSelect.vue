<template>
<select :value="modelValue" @change="changeOption">
    <option disabled selected hidden value="">Выберите из списка</option>
    <option 
        v-for="option in options" 
        :key="option.value" 
        :value="option.value"
    >
        {{ option.name }}
    </option>
</select>
</template>

<script>
export default {
    name: "base-select",
    props: {
        modelValue: {
            type: String,
        }, 
        options: {
            type: Array,
            default: () => [],
        }
    },
    methods: {
        changeOption(event) {
            this.$emit('update', event.target.value)
        }
    }
}
</script>

<style scoped>
</style>