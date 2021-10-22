import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
// import router from './router'
// import VueRouter from 'vue-router'
// import vue from '@vitejs/plugin-vue'
import { createWebHistory, createRouter } from "vue-router";
import About from "./components/About.vue";
import Home from "./components/Home.vue";


// export default {
//   plugins: [
//     vue({
//       template: {
//         compilerOptions: {
//           // ...
//         }
//       }
//     })
//   ]
// }

const route = [
    {
      path: "/",
      name: 'Home',
      component: Home,
    },
    {
      path: "/about",
      name :'About',
      component: About,
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


// app.config.compilerOptions.isCustomElement = tag => tag.startsWith('router')

// const routes = [
//     {
//       path: "/home",
//       name: "Home",
//       component: Home,
//     },
//   ];

//   const router = new VueRouter({
//     routes,
//   });

//   export default {router};