<template>
<base-select :modelValue="value" :options="options" @update:modelValue="updateValue"/>
</template>

<script>
export default {
    name: 'key-value-select',
    props: {
        key_: {
            type: String,
            required: true
        },
        value: {
            type: [String, Number, Date],
            required: false,
            default: '',
        },
        options: {
            type: Array,
            required: false,
            default: () => [],
        }
    },
    methods: {
        updateValue(value) {
            const key_ = this.key_;
            this.$emit('update', {key_, value});
        }
    }
}
</script>

<style scoped>
</style>