<script setup>
defineProps({
  caption: {
    type: String,
    default:
      "Lee miles de comentarios y te dice qué piensan tus usuarios, sin que tengas que leerlos uno por uno.",
  },
});

// Patrón fijo del "pulso de sentimiento": mayoría positivo/neutro, algo de negativo.
const categorias = [
  "teal", "teal", "neutral", "teal", "coral", "teal", "neutral", "teal",
  "teal", "neutral", "teal", "coral", "teal", "teal", "neutral", "teal",
  "coral", "teal", "neutral", "teal", "teal", "neutral", "coral", "teal",
  "teal", "neutral", "teal", "teal", "coral", "neutral", "teal", "teal",
];
const barras = categorias.map((categoria, i) => ({
  categoria,
  alturaBase: 0.35 + ((i * 37) % 60) / 100,
  duracion: 1.8 + ((i * 13) % 9) / 10,
  retraso: ((i * 7) % 20) / 10,
}));
</script>

<template>
  <section class="brand-panel">
    <div class="brand">
      <span class="brand-mark">SentimentBrand</span>
    </div>

    <div class="pulse" aria-hidden="true">
      <span
        v-for="(barra, i) in barras"
        :key="i"
        class="pulse-bar"
        :class="`pulse-bar--${barra.categoria}`"
        :style="{
          '--altura-base': barra.alturaBase,
          '--duracion': `${barra.duracion}s`,
          '--retraso': `${barra.retraso}s`,
        }"
      />
    </div>

    <p class="visual-caption">{{ caption }}</p>
  </section>
</template>

<style scoped>
.brand-panel {
  background: var(--ink);
  color: var(--text-on-dark);
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 4rem 3.5rem;
  position: relative;
  overflow: hidden;
  min-height: 100%;
}

@media (max-width: 860px) {
  .brand-panel {
    padding: 3rem 1.75rem 2rem;
  }
}

.brand-mark {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.15rem;
  letter-spacing: 0.01em;
}

.pulse {
  display: flex;
  align-items: flex-end;
  gap: 5px;
  height: 140px;
  margin: 2.75rem 0 2rem;
}

.pulse-bar {
  flex: 1;
  min-width: 4px;
  max-width: 10px;
  border-radius: 3px 3px 0 0;
  transform-origin: bottom;
  transform: scaleY(var(--altura-base));
  animation: pulso var(--duracion) ease-in-out var(--retraso) infinite;
}

.pulse-bar--teal {
  background: var(--teal);
}
.pulse-bar--coral {
  background: var(--coral);
}
.pulse-bar--neutral {
  background: var(--neutral);
}

@keyframes pulso {
  0%,
  100% {
    transform: scaleY(var(--altura-base));
  }
  50% {
    transform: scaleY(1);
  }
}

.visual-caption {
  font-family: var(--font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-on-dark-secondary);
  max-width: 30ch;
}
</style>
