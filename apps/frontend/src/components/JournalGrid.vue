<script setup>
import JournalCard from './JournalCard.vue';

// Sample data - this would eventually come from your API
const entries = [
  { id: 1, date: "March 3, 2025", title: "AI GENERATED TITLE THAT DESCRIBES...", content: "This is the first journal entry." },
  { id: 2, date: "March 3, 2025", title: "AI GENERATED TITLE THAT DESCRIBES...", content: "Another interesting journal entry." },
  { id: 3, date: "February 28, 2025", title: "REFLECTION ON PERSONAL GROWTH...", content: "Thoughts on my recent progress." },
  { id: 4, date: "February 25, 2025", title: "WEEKLY GUIDANCE FOR CREATIVE...", content: "Creative insights from this week." },
  { id: 5, date: "February 21, 2025", title: "NAVIGATING RELATIONSHIP CHALLENGES...", content: "How I'm handling current relationship dynamics." }
];
</script>

<template>
  <div class="journal-grid">
    <JournalCard 
      v-for="entry in entries" 
      :key="entry.id" 
      :title="entry.title"
      :date="entry.date"
      :content="entry.content" 
    />
  </div>
</template>

<style scoped>
.journal-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
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
