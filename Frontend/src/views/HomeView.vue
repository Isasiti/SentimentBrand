<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

function cerrarSesion() {
  localStorage.removeItem("sb_token");
  router.push({ name: "login" });
}
</script>

<template>
  <div class="home">
    <header>
      <span class="brand-mark">SentimentBrand</span>
      <button class="link-button" @click="cerrarSesion">Cerrar sesión</button>
    </header>
    <main>
      <p class="eyebrow">Sesión iniciada</p>
      <h1>Pega tu texto para analizarlo</h1>
      <p class="subtitle">
        Este es un placeholder. Aquí construiremos el área de texto y la vista
        de resultados (% positivo/negativo + preguntas frecuentes).
      </p>
    </main>
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
  background: var(--paper);
}

header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 2rem;
  border-bottom: 1px solid var(--border);
  background: var(--paper-2);
}

.brand-mark {
  font-family: var(--font-display);
  font-weight: 600;
  color: var(--text-ink);
}

.link-button {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: 0.85rem;
  cursor: pointer;
}

.link-button:hover {
  color: var(--coral);
}

main {
  max-width: 640px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.eyebrow {
  font-family: var(--font-mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--teal);
  margin: 0 0 0.75rem;
}

h1 {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.9rem;
  margin: 0 0 0.75rem;
  color: var(--text-ink);
}

.subtitle {
  color: var(--text-secondary);
  line-height: 1.6;
}
</style>
