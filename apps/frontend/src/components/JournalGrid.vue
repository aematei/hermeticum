<script setup>
import JournalCard from './JournalCard.vue';

const entries = [
  { date: "March 3, 2025", title: "AI GENERATED TITLE THAT DESCRIBES..." },
  { date: "March 3, 2025", title: "AI GENERATED TITLE THAT DESCRIBES..." },
  { date: "February 28, 2025", title: "REFLECTION ON PERSONAL GROWTH..." },
  { date: "February 25, 2025", title: "WEEKLY GUIDANCE FOR CREATIVE..." },
  { date: "February 21, 2025", title: "NAVIGATING RELATIONSHIP CHALLENGES..." }
];
</script>

<template>
  <div class="journal-grid">
    <JournalCard v-for="entry in entries" :key="entry.date" :entry="entry" />
    <div class="journal-card" v-for="i in 6" :key="i">
      <h3>Journal Entry {{i}}</h3>
      <p>This is a sample journal entry...</p>
      <div class="date">May {{i + 10}}, 2023</div>
    </div>
  </div>
</template>

<style scoped>
.journal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}
.journal-card {
  background-color: #2d325a;
  padding: 1.5rem;
  border-radius: 8px;
}
.date {
  margin-top: 1rem;
  color: #9fa8da;
  font-size: 0.85rem;
}
</style>
