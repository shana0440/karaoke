<script lang="ts">
  import {
    IconPlayerPlay,
    IconDots,
    IconPlaylistX,
    IconBrandYoutube,
  } from "@tabler/icons-svelte";
  import { createDropdownMenu, melt } from "@melt-ui/svelte";
  import { fly } from "svelte/transition";
  import { useQueue } from "$lib/hooks/use_queue";
  import type { Clip } from "$lib/domains/clip";
  import TimeFormat from "./time_format.svelte";

  export let index: number;
  export let clip: Clip;
  const {
    elements: { trigger, menu, item },
    states: { open },
  } = createDropdownMenu({
    forceVisible: true,
  });
  const { remove } = useQueue();
</script>

<div
  role="button"
  class="flex items-center gap-4 px-4 py-2 transition-colors rounded-lg group hover:bg-cod-gray"
>
  <p class="relative flex items-center justify-center">
    <span class="transition-opacity group-hover:opacity-0">
      {index}
    </span>
    <IconPlayerPlay
      class="absolute w-5 h-5 transition-opacity opacity-0 group-hover:opacity-100 fill-alice-blue stroke-alice-blue"
    />
  </p>
  <p class="flex-1 w-0 truncate">{clip.name}</p>
  <time>
    <TimeFormat value={clip.end_at - clip.start_at} />
  </time>
  <div class="relative">
    <button
      class="p-1 transition-colors rounded-md hover:bg-charcoal"
      use:melt={$trigger}
    >
      <IconDots class="stroke-light-grey" />
    </button>
  </div>
</div>
{#if $open}
  <div class="menu" use:melt={$menu} transition:fly={{ duration: 150, y: -10 }}>
    <button class="item" use:melt={$item} on:click={() => remove(clip)}>
      <IconPlaylistX class="w-6 h-6" />
      Remove from Queue
    </button>
    <a
      href="https://youtube.com/watch?v=u6ftrRfR5Nw&t=300s"
      target="_blank"
      class="item"
      use:melt={$item}
    >
      <IconBrandYoutube class="w-6 h-6" />
      Open on YouTube
    </a>
  </div>
{/if}

<style lang="postcss">
  .menu {
    @apply z-10 flex flex-col shadow-lg p-1;
    @apply rounded-md bg-bastille border border-outer-space;
  }
  .item {
    @apply flex items-center gap-2 px-4 py-2 rounded text-sm hover:bg-charcoal;
  }
</style>
