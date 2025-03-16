<template>
  <aside class="sidebar">
    <ul>
      <li>Dashboard</li>
      <li>Journals</li>
      <li>Readings</li>
      <li>Settings</li>
    </ul>
  </aside>
</template>

<script setup>
// Component logic here
</script>

<style scoped>
.sidebar {
  width: 200px;
  background-color: #262a4c;
  padding: 1rem;
}
ul {
  list-style: none;
}
li {
  padding: 0.75rem 0;
  cursor: pointer;
}
li:hover {
  color: #9fa8da;
}
</style>
