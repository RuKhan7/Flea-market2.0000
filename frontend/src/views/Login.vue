<template>
  <div style="max-width: 400px; margin: 50px auto;">
    <h2>Вход в систему</h2>
    <form @submit.prevent="handleLogin">
      <div style="margin-bottom: 10px;">
        <label>Имя пользователя</label>
        <input v-model="username" type="text" required style="width: 100%; padding: 8px;" />
      </div>
      <div style="margin-bottom: 10px;">
        <label>Пароль</label>
        <input v-model="password" type="password" required style="width: 100%; padding: 8px;" />
      </div>
      <button type="submit" style="padding: 10px 20px; cursor: pointer;">Войти</button>
      <p v-if="error" style="color: red;">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const error = ref('');
const authStore = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  try {
    await authStore.login(username.value, password.value);
    router.push('/'); // Перенаправляем на главную после успешного входа
  } catch (err) {
    error.value = 'Неверное имя пользователя или пароль';
    console.error(err);
  }
};
</script>