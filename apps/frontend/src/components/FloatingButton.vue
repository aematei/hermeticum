<template>
  <button class="floating-button">+</button>
</template>

<script setup>
// Component logic here
</script>

<style scoped>
.floating-button {
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background-color: #7f5af0;
  color: white;
  font-size: 2rem;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}
.floating-button:hover {
  background-color: #6a4ec2;
}
</style>
