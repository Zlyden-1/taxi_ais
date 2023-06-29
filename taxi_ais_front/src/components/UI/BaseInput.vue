<template>
<input :value="value" @input="updateInput" class="input" type="text">
</template>

<script>
export default {
    name: "base-input",
    props: {
      value: [String, Number]
    },
    methods: {
      updateInput(event) {
        this.$emit('update:value', event.target.value)
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