<template>
<table class="table">
<slot></slot>
</table>
</template>

<script>
export default {
    name: "base-table",
}
</script>

<style>
.table {
    width: 100%;
    border: 1px solid;
    border-collapse: collapse; 
}
.table th {
    font-weight: bold;
    padding: 5px;
    background: #00a0a0;
    border: 1px solid teal;
    color: white;
}
    .table td {
    border: 1px solid teal;
    padding: 5px;
    box-sizing: border-box;
}
.action__buttons {
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}
</style>