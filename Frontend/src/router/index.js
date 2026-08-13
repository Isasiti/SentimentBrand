import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import VerifyView from "../views/VerifyView.vue";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", name: "login", component: LoginView },
    { path: "/registro", name: "registro", component: RegisterView },
    { path: "/verificar", name: "verificar", component: VerifyView },
    {
      path: "/inicio",
      name: "home",
      component: HomeView,
      meta: { requiereSesion: true },
    },
  ],
});

// Guarda de navegación simple: si no hay sesión, siempre vuelve al login.
router.beforeEach((to) => {
  const haySesion = Boolean(localStorage.getItem("sb_token"));
  if (to.meta.requiereSesion && !haySesion) {
    return { name: "login" };
  }
  return true;
});

export default router;
