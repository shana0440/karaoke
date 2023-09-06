<script lang="ts">
  import { createTooltip, melt } from "@melt-ui/svelte";
  import { fade } from "svelte/transition";

  export let description: string;

  const {
    elements: { trigger, content, arrow },
    states: { open },
  } = createTooltip({
    positioning: {
      placement: "top",
    },
    openDelay: 500,
    closeOnPointerDown: false,
    forceVisible: true,
  });
</script>

<span class={$$restProps.class} use:melt={$trigger}>
  <slot />
</span>

{#if $open}
  <div use:melt={$content} transition:fade={{ duration: 100 }} class="menu">
    <div use:melt={$arrow} />
    <p class="px-2 py-1 text-alice-blue">{description}</p>
  </div>
{/if}
