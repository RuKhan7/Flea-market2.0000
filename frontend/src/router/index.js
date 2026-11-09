import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import ProductDetail from '../views/ProductDetail.vue';
import ProductCreate from '../views/ProductCreate.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/product/:id', component: ProductDetail },
  { path: '/create', component: ProductCreate, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;