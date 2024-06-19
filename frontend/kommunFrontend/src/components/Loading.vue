<template>
  <div class="loader">
        <li class="ball bg-green-300"></li>
        <li class="ball bg-indigo-400"></li>
        <li class="ball bg-blue-600"></li>
    </div>
</template>

<script>
export default {
    name:'loadingDots'
}
</script>

<style>
.loader {
  width: 60px;
  display: flex;
  justify-content: space-evenly;
}

.ball {
  list-style: none;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.ball:nth-child(1) {
  animation: bounce-1 1.7s ease-in-out infinite;
}

@keyframes bounce-1 {
  50% {
    transform: translateY(-90px);
    scale: 0.3;
  }
}

.ball:nth-child(2) {
  animation: bounce-3 1.7s ease-in-out 0.3s infinite;
}

@keyframes bounce-2 {
  50% {
    transform: translateY(-90px);
    scale: 0.3;
  }
}

.ball:nth-child(3) {
  animation: bounce-3 1.7s ease-in-out 0.6s infinite;
}

@keyframes bounce-3 {
  50% {
    transform: translateY(-90px);
    scale: 0.3;
  }
}
</style>