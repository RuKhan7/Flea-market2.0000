<template>
  <form @submit.prevent="createProduct" enctype="multipart/form-data">
    <input v-model="form.title" placeholder="Название" required />
    <textarea v-model="form.description" placeholder="Описание"></textarea>
    <input v-model="form.price" type="number" placeholder="Цена" required />
    <select v-model="form.category">
      <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
    </select>
    <input v-model="form.city" placeholder="Город" required />
    <input type="file" multiple @change="onFileChange" />
    <button type="submit">Создать</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../api';
import { useRouter } from 'vue-router';

const router = useRouter();
const categories = ref([]);
const form = ref({
  title: '',
  description: '',
  price: '',
  category: '',
  city: '',
  uploaded_images: [],
});

const onFileChange = (e) => {
  form.value.uploaded_images = Array.from(e.target.files);
};

const createProduct = async () => {
  const formData = new FormData();
  formData.append('title', form.value.title);
  formData.append('description', form.value.description);
  formData.append('price', form.value.price);
  formData.append('category', form.value.category);
  formData.append('city', form.value.city);
  form.value.uploaded_images.forEach((file, index) => {
    formData.append(`uploaded_images[${index}]`, file);
  });

  try {
    await api.post('/products/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    router.push('/');
  } catch (error) {
    console.error(error.response?.data);
  }
};

onMounted(async () => {
  const response = await api.get('/categories/');
  categories.value = response.data.results;
});
</script>