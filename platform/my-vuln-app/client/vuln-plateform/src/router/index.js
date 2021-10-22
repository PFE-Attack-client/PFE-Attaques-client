import { createWebHistory, createRouter } from "vue-router";
import Login from "../components/Login.vue";
import Home from "../components/Home.vue";

const route = [
  {
    path: "/home",
    component: Home,
  },
  {
    path: "/login",
    component: Login,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes : route,
});

export default router