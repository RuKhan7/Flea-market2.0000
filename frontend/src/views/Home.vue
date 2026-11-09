<template>
  <div>
    <h1>Товары</h1>
    <div v-for="product in products" :key="product.id" class="product-card">
      <img v-if="product.images.length" :src="product.images[0].image" width="150" />
      <h3>{{ product.title }}</h3>
      <p>{{ product.price }} ₽</p>
      <router-link :to="`/product/${product.id}`">Подробнее</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';

const products = ref([]);

onMounted(async () => {
  const response = await api.get('/products/');
  products.value = response.data.results; // DRF возвращает пагинированный ответ
});
</script>