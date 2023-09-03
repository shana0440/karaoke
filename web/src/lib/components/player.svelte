<script lang="ts">
  import {
    IconPlayerPlay,
    IconPlayerSkipBack,
    IconPlayerSkipForward,
    IconPlayerPause,
    IconPhotoSensor,
    IconShare,
  } from "@tabler/icons-svelte";
  import { createSlider, melt } from "@melt-ui/svelte";
  import { usePlayer } from "$lib/hooks/use_player";
  import { isNone } from "fp-ts/lib/Option";
  import TimeFormat from "./time_format.svelte";
  const {
    elements: { root, range, thumb },
    states: { value },
  } = createSlider({
    defaultValue: [100],
    max: 500,
    step: 1,
    onValueChange({ curr, next }) {
      return next;
    },
  });
  const { player } = usePlayer();

  export let isFullScreenPlayerOpen: boolean;
</script>

<div
  class="flex items-center w-full gap-10 px-4 py-2 rounded-lg bg-dark-slate-grey"
>
  {#if isNone($player)}
    <div class="h-14" />
  {:else}
    <div class="flex w-64 gap-2">
      <img
        class="rounded h-14 aspect-auto"
        src={$player.value.clip.video.video_thumbnail}
        alt={$player.value.clip.video.title}
      />
      <div class="flex flex-col justify-around">
        <p class="font-semibold text-alice-blue">{$player.value.clip.name}</p>
        <p class="text-sm text-light-grey line-clamp-1">
          {$player.value.clip.video.channel.title}
        </p>
      </div>
    </div>
    <div class="flex items-center justify-center gap-2">
      <button class="p-2 rounded-full group">
        <IconPlayerSkipBack class="icon-btn-fill icon-btn-stroke" />
      </button>
      <button type="button" class="p-2 rounded-full bg-cod-gray group">
        {#if $player.value.isPause}
          <IconPlayerPlay class="icon-btn-fill icon-btn-stroke" />
        {:else}
          <IconPlayerPause class="icon-btn-fill icon-btn-stroke" />
        {/if}
      </button>
      <button class="p-2 rounded-full group">
        <IconPlayerSkipForward class="icon-btn-fill icon-btn-stroke" />
      </button>
    </div>
    <div class="flex items-center flex-1 gap-2">
      <time class="text-light-grey">
        <TimeFormat value={$player.value.currentTime} />
      </time>
      <span use:melt={$root} class="relative flex items-center flex-1">
        <span class="block w-full h-1 bg-gunmetal">
          <span use:melt={$range} class="h-1 bg-alice-blue" />
        </span>
        <span
          use:melt={$thumb()}
          class="block w-5 h-5 rounded-full outline-none bg-alice-blue focus:ring-4 focus:ring-cod-gray/40"
        />
      </span>
      <time class="text-light-grey">
        <TimeFormat
          value={$player.value.clip.end_at - $player.value.clip.start_at}
        />
      </time>
    </div>
    <div class="flex items-center justify-end gap-4">
      <a
        href={`https://youtube.com/watch?v=${$player.value.clip.video.id}&t=${$player.value.clip.start_at}s"`}
        target="_blank"
        class="group"
      >
        <IconShare class="icon-btn-stroke" />
      </a>
      <button
        class="group"
        on:click={() => (isFullScreenPlayerOpen = !isFullScreenPlayerOpen)}
      >
        <IconPhotoSensor class="icon-btn-stroke" />
      </button>
    </div>
  {/if}
</div>
