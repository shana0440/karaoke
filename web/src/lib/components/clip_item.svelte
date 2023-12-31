<script lang="ts">
  import type { Clip } from "$lib/domains/clip";
  import TimeFormat from "./time_format.svelte";
  import {
    IconBrandYoutube,
    IconDots,
    IconPlayerPlayFilled,
    IconPlaylistAdd,
  } from "@tabler/icons-svelte";
  import { createDropdownMenu, melt } from "@melt-ui/svelte";
  import { useQueue } from "$lib/hooks/use_queue";
  import { usePlayer } from "$lib/hooks/use_player";
  import { fade, fly } from "svelte/transition";
  import { addToast } from "./toaster.svelte";
  import Playing from "./playing.svelte";

  export let clip: Clip;
  export let index: number;

  const {
    elements: { trigger, menu, item },
    states: { open },
  } = createDropdownMenu({
    forceVisible: true,
  });
  const { add } = useQueue();
  const { play, playingClip, isPlaying } = usePlayer();
</script>

<div
  class="flex items-center gap-2 px-4 py-2 transition-colors rounded-md group bg-charcoal hover:bg-cod-gray"
>
  <p class="flex items-center justify-center w-8 text-light-grey">
    {#if isPlaying($playingClip, clip)}
      <div transition:fade>
        <Playing />
      </div>
    {:else}
      <span class="transition-opacity group-hover:opacity-0">
        {index}
      </span>
      <button
        on:click={() => {
          play(clip);
        }}
        class="absolute transition-all opacity-0 group-hover:opacity-100 hover:scale-125"
      >
        <IconPlayerPlayFilled class="w-5 h-5 text-alice-blue" />
      </button>
    {/if}
  </p>
  <span class="flex flex-col flex-1 gap-1">
    <span>
      {clip.name}
    </span>
    <span class="text-xs text-light-grey">
      {clip.video.title}
    </span>
  </span>
  <span class="text-light-grey">
    <TimeFormat value={clip.end_at - clip.start_at} />
  </span>
  <button
    class="p-1 transition-colors rounded-md hover:bg-charcoal"
    use:melt={$trigger}
    on:click={(e) => e.stopPropagation()}
  >
    <IconDots class="stroke-light-grey" />
  </button>
</div>

{#if $open}
  <div class="menu" use:melt={$menu} transition:fly={{ duration: 150, y: -10 }}>
    <button
      class="item"
      use:melt={$item}
      on:click={() => {
        add(clip);
        addToast({
          data: {
            message: `Added to Queue`,
            intent: "success",
          },
        });
      }}
    >
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
