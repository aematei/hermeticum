<script setup>
import Navbar from './components/Navbar.vue';
import Sidebar from './components/Sidebar.vue';
import JournalGrid from './components/JournalGrid.vue';
import FloatingButton from './components/FloatingButton.vue';
</script>

<template>
  <div class="app-container">
    <Navbar />
    <div class="main-container">
      <Sidebar />
      <main class="content">
        <JournalGrid />
      </main>
    </div>
    <FloatingButton />
  </div>
</template>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.main-container {
  display: flex;
  flex-grow: 1;
}
.content {
  flex-grow: 1;
  overflow-y: auto;
  padding: 30px;
  background-color: #1B1F3B;
}
</style>
