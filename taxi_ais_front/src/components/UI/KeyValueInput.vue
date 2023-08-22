<template>
<base-input :modelValue="value" :placeholder="placeholder" :type="type" @update:modelValue="updateValue"/>
</template>

<script>
export default {
    name: 'key-value-input',
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
        placeholder: {
            type: [String, Number],
            required: false,
        },
        type: {
            type: String,
            required: false,
            default: 'text',
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