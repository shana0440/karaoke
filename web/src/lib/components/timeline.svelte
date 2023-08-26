<script lang="ts">
  import { onMount } from "svelte";
  import { makeScale, type Scale, reScale } from "../../scale/scale";
  import Slider from "./slider.svelte";
  import Track from "./track.svelte";
  import XAxis from "./x_axis.svelte";
  import TimeFormat from "./time_format.svelte";
  import Indicator from "./indicator.svelte";
  import type { Song } from "../../domains/song";

  export let domain: [number, number];
  export let currentTime: number;
  export let windows: [number, number] = [...domain];
  export let onCurrentTimeChange: (time: number) => void;
  export let songs: Song[];

  let container: HTMLDivElement;
  let scale: Scale;

  $: {
    if (scale) {
      scale = reScale(scale, windows);
    }
  }

  onMount(() => {
    scale = makeScale(windows, [0, container.clientWidth]);
  });
</script>

<div class="overflow-hidden">
  <div class="flex">
    <div>
      <div class="h-10 w-96" />
      {#each songs as song}
        <div class="h-[50px] px-2 py-1 -mt-[1px] border border-light-grey">
          <input
            class="bg-transparent"
            bind:value={song.name}
            placeholder="Unknown"
          />
          <div class="text-sm text-light-grey">
            <TimeFormat value={song.range[0]} />
            ~
            <TimeFormat value={song.range[1]} />
            (<TimeFormat value={song.range[1] - song.range[0]} />)
          </div>
        </div>
      {/each}
    </div>
    <div
      tabindex="-1"
      class="relative flex-1 overflow-hidden"
      bind:this={container}
    >
      {#if scale}
        <Indicator {scale} value={currentTime} />
        <XAxis {scale} {onCurrentTimeChange} />
        {#each songs as song}
          <Track bind:domain={song.range} {scale} name={song.name} />
        {/each}
        <Slider bind:value={windows} min={domain[0]} max={domain[1]} />
      {/if}
    </div>
  </div>
</div>
