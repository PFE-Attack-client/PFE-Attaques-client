import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import { createWebHistory, createRouter } from "vue-router";
import About from "./components/About.vue";
import Contact from "./components/Contact.vue";
import Home from "./components/Home.vue";
import Login from "./components/Login.vue";
import Articles from "./components/Articles.vue";

const route = [
    {
      path: "/home",
      name: 'Home',
      component: Home,
    },
    {
      path: "/articles",
      name: 'Articles',
      component: Articles,
    },
    {
      path: "/about",
      name :'About',
      component: About,
    },
    {
      path: "/login",
      name :'Login',
      component: Login,
    },
    {
      path: "/contact",
      name :'Contact',
      component: Contact,
    },
  ];

const router = createRouter({
    history: createWebHistory(),
    routes : route,
  });

const app = createApp(App)

app.use(ElementPlus)
app.use(router)
app.mount('#app')
