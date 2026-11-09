<template>
  <div v-if="product">
    <h1>{{ product.title }}</h1>
    <img v-if="product.images && product.images.length" :src="product.images[0].image" width="300" style="border-radius: 8px;" />
    <h2 style="color: blue;">{{ product.price }} ₽</h2>
    <p><strong>Город:</strong> {{ product.city }}</p>
    <p><strong>Категория:</strong> {{ product.category_name }}</p>
    <p><strong>Описание:</strong></p>
    <p>{{ product.description }}</p>
    
    <div style="margin-top: 20px; padding: 15px; background: #f0f0f0; border-radius: 8px;">
      <h3>Продавец</h3>
      <p>Имя: {{ product.seller?.username || 'Неизвестно' }}</p>
      <p>Телефон: {{ product.seller?.phone || 'Не указан' }}</p>
    </div>
  </div>
  <div v-else>
    <p>Загрузка товара...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '../api';

const route = useRoute();
const product = ref(null);

onMounted(async () => {
  try {
    // Получаем ID товара из адресной строки
    const productId = route.params.id; 
    const response = await api.get(`/products/${productId}/`);
    product.value = response.data;
  } catch (error) {
    console.error('Ошибка при загрузке товара:', error);
  }
});
</script>