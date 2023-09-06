<script lang="ts">
  import {
    IconPlayerPlayFilled,
    IconDots,
    IconPlaylistX,
    IconBrandYoutube,
  } from "@tabler/icons-svelte";
  import { createDropdownMenu, melt } from "@melt-ui/svelte";
  import { fly } from "svelte/transition";
  import { useQueue } from "$lib/hooks/use_queue";
  import type { Clip } from "$lib/domains/clip";
  import TimeFormat from "./time_format.svelte";
  import { usePlayer } from "$lib/hooks/use_player";
  import { slide } from "svelte/transition";

  export let index: number;
  export let clip: Clip;
  const {
    elements: { trigger, menu, item },
    states: { open },
  } = createDropdownMenu({
    forceVisible: true,
  });
  const { remove } = useQueue();
  const { play } = usePlayer();
</script>

<div
  transition:slide={{ duration: 300 }}
  class="flex items-center gap-4 px-4 py-2 transition-colors rounded-lg group hover:bg-cod-gray"
>
  <p class="relative flex items-center justify-center">
    <span class="transition-opacity group-hover:opacity-0">
      {index}
    </span>
    <button
      on:click={() => {
        play(clip);
        remove(clip);
      }}
      class="absolute transition-all opacity-0 group-hover:opacity-100 hover:scale-125"
    >
      <IconPlayerPlayFilled class="w-5 h-5 text-alice-blue" />
    </button>
  </p>
  <p class="flex-1 w-0 truncate">{clip.name}</p>
  <time>
    <TimeFormat value={clip.end_at - clip.start_at} />
  </time>
  <div class="relative">
    <button
      class="p-1 transition-colors rounded-md hover:bg-charcoal"
      use:melt={$trigger}
      on:click={(e) => e.stopPropagation()}
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
      href={`https://youtube.com/watch?v=${clip.video.resource_id}&t=${clip.start_at}s`}
      target="_blank"
      class="item"
      use:melt={$item}
    >
      <IconBrandYoutube class="w-6 h-6" />
      Open on YouTube
    </a>
  </div>
{/if}
