<script lang="ts">
  import {
    IconPlayerSkipBack,
    IconPlayerSkipForward,
    IconPlayerPause,
    IconPlayerPlay,
    IconShare,
    IconX,
  } from "@tabler/icons-svelte";
  import { getContext } from "svelte";
  import type { FloatingYoutubeContext } from "./floating_youtube.svelte";
  import QueueItem from "./queue_item.svelte";
  import { useQueue } from "$lib/hooks/use_queue";
  import { usePlayer } from "$lib/hooks/use_player";
  import { isSome } from "fp-ts/lib/Option";
  import TimeFormat from "./time_format.svelte";
  import ProgressBar from "./progress_bar.svelte";
  import autoAnimate from "@formkit/auto-animate";

  export let isFullScreenPlayerOpen: boolean;

  const { playingClip, isPause, currentTime, play, pause, playNext, playPrev } =
    usePlayer();
  const { queue } = useQueue();

  const { move } = getContext<FloatingYoutubeContext>("floating-yt");
  let ytContainer: HTMLDivElement;

  $: {
    if (isFullScreenPlayerOpen && ytContainer) {
      // TODO: add animation to moving
      setTimeout(() => {
        move(ytContainer.getBoundingClientRect());
      }, 300);
    }
  }
</script>

{#if isSome($playingClip)}
  <div
    class={`fixed inset-0 flex flex-col backdrop-blur-2xl transition-all z-10 p-2 ${
      isFullScreenPlayerOpen
        ? "translate-y-0 opacity-100"
        : "pointer-events-none translate-y-1/3 opacity-0"
    }`}
  >
    <div class="flex items-center justify-center flex-1">
      <div class="flex justify-center gap-10 h-[600px]">
        <div
          class="flex flex-col gap-10 px-6 py-10 rounded-3xl bg-cod-gray/30 w-[450px]"
        >
          <div
            class="relative overflow-hidden rounded-2xl aspect-video"
            bind:this={ytContainer}
          >
            <img
              class="absolute z-0 w-full h-full"
              src={$playingClip.value.video.video_thumbnail}
              alt={$playingClip.value.video.title}
            />
          </div>
          <div class="flex flex-col gap-2">
            <p class="font-semibold text-alice-blue">
              {$playingClip.value.name}
            </p>
            <p class="text-sm text-light-grey line-clamp-1">
              {$playingClip.value.video.channel.title}
            </p>
            <p class="text-sm text-light-grey line-clamp-1">
              {$playingClip.value.video.title}
            </p>
          </div>

          <div class="flex items-center justify-center gap-2">
            <button class="p-4 rounded-full group" on:click={playPrev}>
              <IconPlayerSkipBack class="icon-btn-fill icon-btn-stroke" />
            </button>
            <button
              type="button"
              class="p-4 rounded-full bg-cod-gray group"
              on:click={() => ($isPause ? play() : pause())}
            >
              {#if $isPause}
                <IconPlayerPlay class="icon-btn-fill icon-btn-stroke" />
              {:else}
                <IconPlayerPause class="icon-btn-fill icon-btn-stroke" />
              {/if}
            </button>
            <button class="p-4 rounded-full group" on:click={playNext}>
              <IconPlayerSkipForward class="icon-btn-fill icon-btn-stroke" />
            </button>
          </div>
        </div>
        <div class="self-start w-[600px] h-full flex flex-col gap-4">
          <h2 class="text-2xl font-semibold">Queue</h2>
          <div class="relative flex-1 overflow-auto">
            <ul class="flex flex-col gap-2" use:autoAnimate>
              {#each $queue as clip, i}
                <li>
                  <QueueItem index={i + 1} {clip} />
                </li>
              {:else}
                <li>Queue is Empty</li>
              {/each}
            </ul>
            <div
              class="pointer-events-none absolute -inset-x-2.5 -bottom-2.5 h-1/3 bg-gradient-to-t from-jet to-jet/0"
            />
          </div>
        </div>
      </div>
    </div>
    <div
      class="flex items-center w-full gap-10 px-4 py-2 rounded-lg bg-dark-slate-grey"
    >
      <div class="flex gap-2 w-72">
        <img
          class="rounded h-14 aspect-auto"
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
          <IconX class="icon-btn-stroke" />
        </button>
      </div>
    </div>
  </div>
{/if}
