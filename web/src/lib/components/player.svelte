<script lang="ts">
  import {
    IconPlayerPlayFilled,
    IconPlayerSkipBackFilled,
    IconPlayerSkipForwardFilled,
    IconPlayerPauseFilled,
    IconPhotoSensor,
    IconBrandYoutube,
    IconRepeatOnce,
  } from "@tabler/icons-svelte";
  import { usePlayer } from "$lib/hooks/use_player";
  import { isNone } from "fp-ts/lib/Option";
  import TimeFormat from "./time_format.svelte";
  import ProgressBar from "./progress_bar.svelte";

  const {
    currentTime,
    playingClip,
    isPause,
    isRepeatOnce,
    playNext,
    playPrev,
    play,
    pause,
  } = usePlayer();

  export let isFullScreenPlayerOpen: boolean;
</script>

<div
  class="flex items-center w-full gap-10 px-4 py-2 rounded-lg bg-dark-slate-grey"
>
  {#if isNone($playingClip)}
    <div class="h-14" />
  {:else}
    <div class="flex gap-2 w-72">
      <img
        class="object-cover rounded h-14 aspect-auto"
        src={$playingClip.value.video.video_thumbnail}
        alt={$playingClip.value.video.title}
      />
      <div class="flex flex-col justify-around">
        <p class="font-semibold text-alice-blue line-clamp-1">
          {$playingClip.value.name}
        </p>
        <p class="text-sm text-light-grey line-clamp-1">
          {$playingClip.value.video.channel.title}
        </p>
      </div>
    </div>
    <div class="flex items-center justify-center gap-2">
      <button class="p-2 rounded-full group" on:click={playPrev}>
        <IconPlayerSkipBackFilled class="icon-btn-fill" />
      </button>
      <button
        type="button"
        class="p-2 rounded-full bg-cod-gray group"
        on:click={() => ($isPause ? play() : pause())}
      >
        {#if $isPause}
          <IconPlayerPlayFilled class="icon-btn-fill" />
        {:else}
          <IconPlayerPauseFilled class="icon-btn-fill" />
        {/if}
      </button>
      <button class="p-2 rounded-full group" on:click={playNext}>
        <IconPlayerSkipForwardFilled class="icon-btn-fill" />
      </button>
    </div>
    <div class="flex items-center flex-1 gap-5">
      <time class="text-light-grey">
        <TimeFormat value={$currentTime[0] - $playingClip.value.start_at} />
      </time>
      <ProgressBar />
      <time class="text-light-grey">
        <TimeFormat
          value={$playingClip.value.end_at - $playingClip.value.start_at}
        />
      </time>
    </div>
    <div class="flex items-center justify-end gap-4">
      <button
        class="icon-btn-stroke"
        class:active={$isRepeatOnce}
        on:click={() => isRepeatOnce.update((prev) => !prev)}
      >
        <IconRepeatOnce />
      </button>
      <a
        href={`https://youtube.com/watch?v=${$playingClip.value.video.resource_id}&t=${$playingClip.value.start_at}s"`}
        target="_blank"
        class="icon-btn-stroke"
      >
        <IconBrandYoutube />
      </a>
      <button
        class="icon-btn-stroke"
        on:click={() => (isFullScreenPlayerOpen = !isFullScreenPlayerOpen)}
      >
        <IconPhotoSensor />
      </button>
    </div>
  {/if}
</div>
