<script lang="ts">
  import {
    IconPlayerPlayFilled,
    IconDots,
    IconBrandYoutube,
    IconTrash,
  } from "@tabler/icons-svelte";
  import { createDialog, createDropdownMenu, melt } from "@melt-ui/svelte";
  import { fly } from "svelte/transition";
  import type { Mv } from "$lib/domains/mv";
  import TimeFormat from "./time_format.svelte";
  import YoutubeDialog from "./youtube_dialog.svelte";

  const {
    elements: { trigger, menu, item },
    states: { open },
  } = createDropdownMenu({
    forceVisible: true,
  });

  export let mv: Mv;
  export let onRemove: (mv: Mv) => void;
</script>

<YoutubeDialog {mv}>
  <div
    role="button"
    tabindex="-1"
    on:keydown={() => {}}
    class="flex flex-col gap-2 p-4 transition-colors rounded-md group bg-dark-slate-grey hover:bg-charcoal"
  >
    <div class="relative overflow-hidden">
      <img
        class="w-full rounded-md aspect-auto"
        src={mv.thumbnail_url}
        alt={mv.title}
      />
      <time
        class="absolute px-1 text-xs rounded-sm right-1 bottom-1 bg-cod-gray"
      >
        <TimeFormat value={mv.duration} />
      </time>
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
    <p class="font-semibold text-alice-blue">{mv.title}</p>
    <p class="text-sm text-light-grey line-clamp-2">{mv.channel_title}</p>
  </div>
</YoutubeDialog>

{#if $open}
  <div class="menu" use:melt={$menu} transition:fly={{ duration: 150, y: -10 }}>
    <button class="item" use:melt={$item} on:click={() => onRemove(mv)}>
      <IconTrash class="w-6 h-6" />
      Remove
    </button>
    <a
      href={`https://youtube.com/watch?v=${mv.id}`}
      target="_blank"
      class="item"
      use:melt={$item}
    >
      <IconBrandYoutube class="w-6 h-6" />
      Open on YouTube
    </a>
  </div>
{/if}
