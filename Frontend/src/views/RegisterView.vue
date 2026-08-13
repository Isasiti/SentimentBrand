<script setup>
import { ref, computed } from "vue";
import { useRouter, RouterLink } from "vue-router";
import BrandPanel from "../components/BrandPanel.vue";

const router = useRouter();
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const nombre = ref("");
const empresa = ref("");
const correo = ref("");
const password = ref("");
const confirmarPassword = ref("");
const mostrarPassword = ref(false);
const estado = ref("inicial"); // inicial | cargando | error
const mensajeError = ref("");

const passwordsCoinciden = computed(
  () => !confirmarPassword.value || password.value === confirmarPassword.value
);
const passwordValida = computed(() => password.value.length === 0 || password.value.length >= 8);

async function enviarRegistro() {
  if (password.value !== confirmarPassword.value) {
    estado.value = "error";
    mensajeError.value = "Las contraseñas no coinciden.";
    return;
  }
  if (password.value.length < 8) {
    estado.value = "error";
    mensajeError.value = "La contraseña debe tener al menos 8 caracteres.";
    return;
  }

  estado.value = "cargando";
  mensajeError.value = "";

  try {
    const res = await fetch(`${API_URL}/auth/registro`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        nombre: nombre.value,
        empresa: empresa.value,
        correo: correo.value,
        password: password.value,
      }),
    });

    const datos = await res.json().catch(() => ({}));

    if (!res.ok) {
      throw new Error(datos.detail ?? "No se pudo completar el registro.");
    }

    router.push({ name: "verificar", query: { correo: correo.value } });
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
    <BrandPanel caption="Crea la cuenta de tu empresa y empieza a analizar comentarios en minutos." />

    <section class="auth-form">
      <div class="form-card">
        <p class="eyebrow">Nueva cuenta</p>
        <h1>Regístrate</h1>
        <p class="subtitle">Te enviaremos un código de verificación a tu correo.</p>

        <form @submit.prevent="enviarRegistro">
          <label class="field">
            <span>Nombre completo</span>
            <input v-model="nombre" type="text" autocomplete="name" required placeholder="Ana Torres" />
          </label>

          <label class="field">
            <span>Nombre de la empresa</span>
            <input
              v-model="empresa"
              type="text"
              autocomplete="organization"
              required
              placeholder="Mi Empresa S.A.S."
            />
          </label>

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
                autocomplete="new-password"
                required
                minlength="8"
                placeholder="Mínimo 8 caracteres"
              />
              <button
                type="button"
                class="toggle-password"
                @click="mostrarPassword = !mostrarPassword"
              >
                {{ mostrarPassword ? "Ocultar" : "Ver" }}
              </button>
            </div>
            <span v-if="!passwordValida" class="field-error">Debe tener al menos 8 caracteres.</span>
          </label>

          <label class="field">
            <span>Confirmar contraseña</span>
            <input
              v-model="confirmarPassword"
              :type="mostrarPassword ? 'text' : 'password'"
              autocomplete="new-password"
              required
              placeholder="Repite tu contraseña"
            />
            <span v-if="!passwordsCoinciden" class="field-error">Las contraseñas no coinciden.</span>
          </label>

          <button type="submit" class="btn-primary" :disabled="estado === 'cargando'">
            {{ estado === "cargando" ? "Creando cuenta…" : "Crear cuenta" }}
          </button>
        </form>

        <p v-if="estado === 'error'" class="status status--error" role="alert">
          {{ mensajeError }}
        </p>

        <p class="hint">
          ¿Ya tienes cuenta?
          <RouterLink :to="{ name: 'login' }">Inicia sesión</RouterLink>
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

.field > span:first-child {
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

.field-error {
  display: block;
  margin-top: 0.35rem;
  color: var(--coral);
  font-size: 0.78rem;
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
