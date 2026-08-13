<script setup>
import { ref } from "vue";
import { useRoute, useRouter, RouterLink } from "vue-router";
import BrandPanel from "../components/BrandPanel.vue";

const route = useRoute();
const router = useRouter();
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

const correo = ref(route.query.correo ?? "");
const codigo = ref("");
const estado = ref("inicial"); // inicial | cargando | error | exito
const mensajeError = ref("");
const reenviando = ref(false);
const mensajeReenvio = ref("");

async function verificarCodigo() {
  estado.value = "cargando";
  mensajeError.value = "";

  try {
    const res = await fetch(`${API_URL}/auth/verificar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo: correo.value, codigo: codigo.value }),
    });

    const datos = await res.json().catch(() => ({}));

    if (!res.ok) {
      throw new Error(datos.detail ?? "No se pudo verificar el código.");
    }

    estado.value = "exito";
    setTimeout(() => router.push({ name: "login" }), 1800);
  } catch (err) {
    estado.value = "error";
    mensajeError.value =
      err.message === "Failed to fetch"
        ? "No se pudo conectar con el servidor. Verifica que el backend esté corriendo."
        : err.message;
  }
}

async function reenviarCodigo() {
  reenviando.value = true;
  mensajeReenvio.value = "";
  try {
    const res = await fetch(`${API_URL}/auth/reenviar-codigo`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ correo: correo.value }),
    });
    if (!res.ok) throw new Error();
    mensajeReenvio.value = "Nuevo código enviado. Revisa tu correo.";
  } catch {
    mensajeReenvio.value = "No se pudo reenviar el código. Intenta de nuevo en un momento.";
  } finally {
    reenviando.value = false;
  }
}
</script>

<template>
  <div class="auth-page">
    <BrandPanel caption="Un último paso: confirma tu correo para activar tu cuenta." />

    <section class="auth-form">
      <div class="form-card">
        <p class="eyebrow">Verificación</p>
        <h1>Revisa tu correo</h1>
        <p class="subtitle">
          Enviamos un código de 6 dígitos a
          <strong>{{ correo || "tu correo" }}</strong>. Vence en 15 minutos.
        </p>

        <form @submit.prevent="verificarCodigo">
          <label class="field">
            <span>Correo</span>
            <input v-model="correo" type="email" required placeholder="tu@empresa.com" />
          </label>

          <label class="field">
            <span>Código de verificación</span>
            <input
              v-model="codigo"
              type="text"
              inputmode="numeric"
              pattern="[0-9]{6}"
              maxlength="6"
              required
              placeholder="000000"
              class="codigo-input"
            />
          </label>

          <button
            type="submit"
            class="btn-primary"
            :disabled="estado === 'cargando' || estado === 'exito'"
          >
            {{ estado === "cargando" ? "Verificando…" : "Verificar cuenta" }}
          </button>
        </form>

        <p v-if="estado === 'exito'" class="status status--exito">
          Cuenta verificada. Redirigiendo a inicio de sesión…
        </p>
        <p v-else-if="estado === 'error'" class="status status--error" role="alert">
          {{ mensajeError }}
        </p>

        <p class="hint">
          ¿No te llegó?
          <button type="button" class="link-button" :disabled="reenviando" @click="reenviarCodigo">
            {{ reenviando ? "Enviando…" : "Reenviar código" }}
          </button>
        </p>
        <p v-if="mensajeReenvio" class="status status--info">{{ mensajeReenvio }}</p>

        <p class="hint">
          <RouterLink :to="{ name: 'login' }">Volver a inicio de sesión</RouterLink>
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

.subtitle strong {
  color: var(--text-ink);
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

.codigo-input {
  font-family: var(--font-mono);
  letter-spacing: 0.4em;
  font-size: 1.1rem;
  text-align: center;
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

.status--exito {
  color: var(--teal);
  background: color-mix(in srgb, var(--teal) 12%, transparent);
  border: 1px solid color-mix(in srgb, var(--teal) 30%, transparent);
  border-radius: 8px;
  padding: 0.6rem 0.75rem;
}

.status--info {
  color: var(--text-secondary);
}

.hint {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-top: 1.25rem;
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

.link-button {
  background: none;
  border: none;
  padding: 0;
  color: var(--teal);
  font-weight: 500;
  font-size: 0.85rem;
  cursor: pointer;
}

.link-button:hover:not(:disabled) {
  text-decoration: underline;
}

.link-button:disabled {
  color: var(--text-muted);
  cursor: default;
}
</style>
