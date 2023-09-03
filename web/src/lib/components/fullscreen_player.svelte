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
  import { createSlider, melt } from "@melt-ui/svelte";
  import { useQueue } from "$lib/hooks/use_queue";
  import { usePlayer } from "$lib/hooks/use_player";
  import { isSome } from "fp-ts/lib/Option";
  import TimeFormat from "./time_format.svelte";

  export let isFullScreenPlayerOpen: boolean;

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

{#if isSome($player)}
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
              src={$player.value.clip.video.video_thumbnail}
              alt={$player.value.clip.video.title}
            />
          </div>
          <div class="flex flex-col gap-2">
            <p class="font-semibold text-alice-blue">
              {$player.value.clip.name}
            </p>
            <p class="text-sm text-light-grey line-clamp-1">
              {$player.value.clip.video.channel.title}
            </p>
            <p class="text-sm text-light-grey line-clamp-1">
              {$player.value.clip.video.title}
            </p>
          </div>

          <div class="flex items-center justify-center gap-2">
            <button class="p-4 rounded-full group">
              <IconPlayerSkipBack class="icon-btn-fill icon-btn-stroke" />
            </button>
            <button type="button" class="p-4 rounded-full bg-cod-gray group">
              {#if $player.value.isPause}
                <IconPlayerPlay class="icon-btn-fill icon-btn-stroke" />
              {:else}
                <IconPlayerPause class="icon-btn-fill icon-btn-stroke" />
              {/if}
            </button>
            <button class="p-4 rounded-full group">
              <IconPlayerSkipForward class="icon-btn-fill icon-btn-stroke" />
            </button>
          </div>
        </div>
        <div class="self-start w-[600px] flex flex-col gap-4">
          <h2 class="text-2xl font-semibold">Queue</h2>
          <div class="relative flex-1 overflow-auto">
            <ul class="flex flex-col gap-2">
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
          <IconX class="icon-btn-stroke" />
        </button>
      </div>
    </div>
  </div>
{/if}
