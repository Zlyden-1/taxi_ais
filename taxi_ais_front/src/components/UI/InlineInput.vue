<template>
<input :value="modelValue" :type="type" :placeholder="placeholder" @input="updateInput" class="input">
</template>

<script>
export default {
    name: "inline-input",
    props: {
      modelValue: {
        type: [String, Number, Date],
        required: true,
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
      updateInput(event) {
        this.$emit('update:modelValue', event.target.value)
      }
    }
}
</script>

<style scoped>
.input {
  border-radius: 5px;
  border: 1px solid teal;
  padding: 5px 5px;
}
</style>