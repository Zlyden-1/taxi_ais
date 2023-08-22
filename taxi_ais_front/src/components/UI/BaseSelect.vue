<template>
<select :value="modelValue" @change="changeOption">
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
            this.$emit('update:modelValue', event.target.value)
        }
    }
}
</script>

<style scoped>
select {
    width: 100%;
    border: 4px solid teal;
    padding: 10px 15px;
    margin-top: 15px;
}
</style>