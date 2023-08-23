<template>
<input :value="modelValue" :type="type" :placeholder="placeholder" @input="updateInput" class="input">
</template>

<script>
export default {
    name: "base-input",
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
    margin-top: 15px;
    width: 100%;
    border: 4px solid teal;
    padding: 10px 15px;
  }
</style>