<script lang="ts">
  import { createDialog, melt } from "@melt-ui/svelte";
  import { fly } from "svelte/transition";
  import Youtube from "./youtube.svelte";
  import { IconArrowLeft } from "@tabler/icons-svelte";
  import type { Mv } from "$lib/domains/mv";
  import Tooltip from "./tooltip.svelte";
  const {
    elements: {
      close,
      trigger,
      overlay,
      title,
      content,
      description,
      portalled,
    },
    states: { open },
  } = createDialog({});

  export let mv: Mv;
</script>

<div use:melt={$trigger} class={$$restProps.class}>
  <slot />
</div>
<div use:melt={$portalled}>
  {#if $open}
    <div
      use:melt={$overlay}
      class="fixed inset-0 z-10 bg-transparent-black backdrop-blur-lg"
    />
    <button class="fixed z-20 p-4 top-10 left-10" use:melt={$close}>
      <IconArrowLeft class="stroke-light-grey" />
    </button>
    <div class="fixed inset-0 z-10 flex flex-col items-center w-full p-8">
      <div
        use:melt={$content}
        class="flex flex-col w-full max-w-4xl gap-4 py-4 outline-none"
        transition:fly={{
          duration: 150,
          y: 8,
        }}
      >
        <Tooltip description={mv.title}>
          <h2 use:melt={$title} class="text-2xl font-medium truncate">
            {mv.title}
          </h2>
        </Tooltip>
        <p use:melt={$description} class="text-lg" />
        <div class="w-full overflow-hidden aspect-video rounded-2xl">
          <Youtube id={mv.id} />
        </div>
      </div>
    </div>
  {/if}
</div>
