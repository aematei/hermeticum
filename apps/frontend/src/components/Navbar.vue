<template>
  <nav class="navbar">
    <div class="logo">Hermeticum</div>
    <div class="search">
      <input type="text" placeholder="Search..." />
    </div>
    <div class="profile">
      <span>Profile</span>
    </div>
  </nav>
</template>

<script setup>
// Component logic here
</script>

<style scoped>
.navbar {
  background-color: #2d325a;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-weight: bold;
  font-size: 1.2rem;
}
.search input {
  padding: 0.5rem;
  border-radius: 4px;
  border: none;
  background-color: #343b6b;
  color: white;
}
</style>
