<script lang="ts">
  import {
    IconPlayerPlay,
    IconPlayerSkipBack,
    IconPlayerSkipForward,
    IconPlayerPause,
    IconPhotoSensor,
    IconShare,
  } from "@tabler/icons-svelte";
  import { usePlayer } from "$lib/hooks/use_player";
  import { isNone } from "fp-ts/lib/Option";
  import TimeFormat from "./time_format.svelte";
  import ProgressBar from "./progress_bar.svelte";

  const { currentTime, playingClip, isPause } = usePlayer();

  export let isFullScreenPlayerOpen: boolean;
</script>

<div
  class="flex items-center w-full gap-10 px-4 py-2 rounded-lg bg-dark-slate-grey"
>
  {#if isNone($playingClip)}
    <div class="h-14" />
  {:else}
    <div class="flex w-64 gap-2">
      <img
        class="rounded h-14 aspect-auto"
        src={$playingClip.value.video.video_thumbnail}
        alt={$playingClip.value.video.title}
      />
      <div class="flex flex-col justify-around">
        <p class="font-semibold text-alice-blue">{$playingClip.value.name}</p>
        <p class="text-sm text-light-grey line-clamp-1">
          {$playingClip.value.video.channel.title}
        </p>
      </div>
    </div>
    <div class="flex items-center justify-center gap-2">
      <button class="p-2 rounded-full group">
        <IconPlayerSkipBack class="icon-btn-fill icon-btn-stroke" />
      </button>
      <button type="button" class="p-2 rounded-full bg-cod-gray group">
        {#if $isPause}
          <IconPlayerPlay class="icon-btn-fill icon-btn-stroke" />
        {:else}
          <IconPlayerPause class="icon-btn-fill icon-btn-stroke" />
        {/if}
      </button>
      <button class="p-2 rounded-full group">
        <IconPlayerSkipForward class="icon-btn-fill icon-btn-stroke" />
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
      <a
        href={`https://youtube.com/watch?v=${$playingClip.value.video.id}&t=${$playingClip.value.start_at}s"`}
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
