<script setup>
import { ref } from "vue";
import { useRouter, RouterLink } from "vue-router";
import BrandPanel from "../components/BrandPanel.vue";

const router = useRouter();
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const correo = ref("");
const password = ref("");
const mostrarPassword = ref(false);
const estado = ref("inicial"); // inicial | cargando | error
const mensajeError = ref("");
const cuentaSinVerificar = ref(false);

async function enviarLogin() {
  estado.value = "cargando";
  mensajeError.value = "";
  cuentaSinVerificar.value = false;

  try {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo: correo.value, password: password.value }),
    });

    const datos = await res.json().catch(() => ({}));

    if (!res.ok) {
      if (res.status === 403 && datos.codigo === "CUENTA_NO_VERIFICADA") {
        cuentaSinVerificar.value = true;
      }
      throw new Error(datos.detail ?? "No se pudo iniciar sesión.");
    }

    localStorage.setItem("sb_token", datos.access_token);
    router.push({ name: "home" });
  } catch (err) {
    estado.value = "error";
    mensajeError.value =
      err.message === "Failed to fetch"
        ? "No se pudo conectar con el servidor. Verifica que el backend esté corriendo."
        : err.message;
  }
}
</script>

<template>
  <div class="auth-page">
    <BrandPanel />

    <section class="auth-form">
      <div class="form-card">
        <p class="eyebrow">Bienvenido de nuevo</p>
        <h1>Inicia sesión</h1>
        <p class="subtitle">Usa tu correo y contraseña de la empresa.</p>

        <form @submit.prevent="enviarLogin">
          <label class="field">
            <span>Correo</span>
            <input
              v-model="correo"
              type="email"
              autocomplete="email"
              required
              placeholder="tu@empresa.com"
            />
          </label>

          <label class="field">
            <span>Contraseña</span>
            <div class="password-wrap">
              <input
                v-model="password"
                :type="mostrarPassword ? 'text' : 'password'"
                autocomplete="current-password"
                required
                placeholder="••••••••"
              />
              <button
                type="button"
                class="toggle-password"
                @click="mostrarPassword = !mostrarPassword"
              >
                {{ mostrarPassword ? "Ocultar" : "Ver" }}
              </button>
            </div>
          </label>

          <button type="submit" class="btn-primary" :disabled="estado === 'cargando'">
            {{ estado === "cargando" ? "Ingresando…" : "Iniciar sesión" }}
          </button>
        </form>

        <p v-if="estado === 'error'" class="status status--error" role="alert">
          {{ mensajeError }}
          <RouterLink v-if="cuentaSinVerificar" :to="{ name: 'verificar', query: { correo } }">
            Verificar mi cuenta
          </RouterLink>
        </p>

        <p class="hint">
          ¿No tienes cuenta?
          <RouterLink :to="{ name: 'registro' }">Regístrate aquí</RouterLink>
        </p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1.1fr 1fr;
}

@media (max-width: 860px) {
  .auth-page {
    grid-template-columns: 1fr;
  }
}

.auth-form {
  background: var(--paper);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2.5rem;
}

.form-card {
  width: 100%;
  max-width: 380px;
}

.eyebrow {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--teal);
  margin: 0 0 0.75rem;
}

.form-card h1 {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 2rem;
  margin: 0 0 0.5rem;
  color: var(--text-ink);
}

.subtitle {
  font-size: 0.95rem;
  color: var(--text-secondary);
  margin: 0 0 2rem;
  line-height: 1.5;
}

.field {
  display: block;
  margin-bottom: 1.1rem;
  font-size: 0.85rem;
  color: var(--text-secondary);
}

.field > span {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 500;
}

.field input {
  width: 100%;
  padding: 0.65rem 0.8rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 0.95rem;
  color: var(--text-ink);
  background: var(--paper-2);
}

.field input:focus {
  border-color: var(--teal);
}

.password-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.password-wrap input {
  padding-right: 3.5rem;
}

.toggle-password {
  position: absolute;
  right: 0.6rem;
  background: none;
  border: none;
  font-size: 0.78rem;
  color: var(--text-secondary);
  cursor: pointer;
}

.toggle-password:hover {
  color: var(--teal);
}

.btn-primary {
  width: 100%;
  padding: 0.7rem;
  margin-top: 0.5rem;
  background: var(--ink);
  color: var(--text-on-dark);
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-primary:hover:not(:disabled) {
  background: var(--ink-2);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: default;
}

.status {
  font-size: 0.85rem;
  margin: 1rem 0 0;
  line-height: 1.5;
}

.status--error {
  color: var(--coral);
  background: color-mix(in srgb, var(--coral) 10%, transparent);
  border: 1px solid color-mix(in srgb, var(--coral) 30%, transparent);
  border-radius: 8px;
  padding: 0.6rem 0.75rem;
}

.status--error a {
  display: inline-block;
  margin-top: 0.35rem;
  color: var(--coral);
  font-weight: 600;
}

.hint {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 1.5rem;
  text-align: center;
}

.hint a {
  color: var(--teal);
  font-weight: 500;
  text-decoration: none;
}

.hint a:hover {
  text-decoration: underline;
}
</style>
