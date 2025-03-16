<script setup>
defineProps(['entry']);
</script>

<template>
  <div class="journal-card">
    <div class="card-overlay">
      <div class="card-date">{{ entry.date }}</div>
      <h3 class="card-title">{{ entry.title }}</h3>
    </div>
  </div>
</template>

<style scoped>
.journal-card {
  background-color: rgba(109, 89, 122, 0.2);
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.3s, box-shadow 0.3s;
}
.journal-card:hover {
  transform: translateY(-5px);
}
</style>
