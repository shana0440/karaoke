<script lang="ts">
  import type { Clip } from "$lib/domains/clip";
  import { usePlayer } from "$lib/hooks/use_player";
  import {
    IconPlayerPlayFilled,
    IconDots,
    IconPlaylistAdd,
    IconBrandYoutube,
  } from "@tabler/icons-svelte";
  import { createDropdownMenu, melt } from "@melt-ui/svelte";
  import { fly } from "svelte/transition";
  import { useQueue } from "$lib/hooks/use_queue";

  const { add } = useQueue();
  const { play } = usePlayer();
  const {
    elements: { trigger, menu, item },
    states: { open },
  } = createDropdownMenu({
    forceVisible: true,
  });

  export let clip: Clip;
</script>

<div
  role="button"
  tabindex="-1"
  on:click={() => play(clip)}
  on:keydown={() => {}}
  class="flex flex-col gap-2 p-4 transition-colors rounded-md group bg-dark-slate-grey hover:bg-charcoal"
>
  <div class="relative overflow-hidden">
    <img
      class="w-full rounded-md aspect-auto"
      src={clip.video.video_thumbnail}
      alt={clip.video.title}
    />
    <button
      class="absolute z-10 p-1 transition-all rounded-full opacity-0 top-1 right-1 hover:bg-charcoal group-hover:opacity-100"
      on:click={(e) => e.stopPropagation()}
      use:melt={$trigger}
    >
      <IconDots class="stroke-light-grey" />
    </button>
    <div
      class="absolute inset-0 flex items-center justify-center transition-all opacity-0 translate-y-1/3 group-hover:translate-y-0 group-hover:opacity-100"
    >
      <div class="p-3 rounded-full bg-cod-gray/80">
        <IconPlayerPlayFilled class="w-6 h-6 fill-alice-blue" />
      </div>
    </div>
  </div>
  <p class="font-semibold text-alice-blue">{clip.name}</p>
  <p class="text-sm text-light-grey line-clamp-2">{clip.video.channel.title}</p>
</div>

{#if $open}
  <div class="menu" use:melt={$menu} transition:fly={{ duration: 150, y: -10 }}>
    <button class="item" use:melt={$item} on:click={() => add(clip)}>
      <IconPlaylistAdd class="w-6 h-6" />
      Add to Queue
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
