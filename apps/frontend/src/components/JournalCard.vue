<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  date: {
    type: String,
    required: true
  },
  content: {
    type: String,
    default: "No content provided"
  }
});
</script>

<template>
  <div class="journal-card">
    <h3>{{ title }}</h3>
    <p>{{ content }}</p>
    <div class="date">{{ date }}</div>
  </div>
</template>

<style scoped>
.journal-card {
  background-color: #2d325a;
  padding: 1.5rem;
  border-radius: 8px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.journal-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

h3 {
  margin-bottom: 0.5rem;
  font-size: 1.2rem;
  color: #ffffff;
}

p {
  color: #ddddfb;
  margin-bottom: 1rem;
}

.date {
  margin-top: 1rem;
  color: #9fa8da;
  font-size: 0.85rem;
}
</style>
