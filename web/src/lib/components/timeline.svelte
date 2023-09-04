<script lang="ts">
  import { onMount } from "svelte";
  import {
    IconPlayerPlay,
    IconCirclesRelation,
    IconPlus,
    IconSpacingHorizontal,
  } from "@tabler/icons-svelte";
  import {
    makeScale,
    type Scale,
    reScale,
    mapRangeToViewDomain,
  } from "$lib/scale/scale";
  import Slider from "./slider.svelte";
  import Track from "./track.svelte";
  import XAxis from "./x_axis.svelte";
  import TimeFormat from "./time_format.svelte";
  import Indicator from "./indicator.svelte";
  import { makeEmptySong, type Song } from "$lib/domains/song";
  import ContextMenu from "./context_menu.svelte";

  export let domain: [number, number];
  export let currentTime: number;
  export let onCurrentTimeChange: (time: number) => void;
  export let songs: Song[];

  let container: HTMLDivElement;
  let scale: Scale;

  const playSong = (song: Song) => () => {
    onCurrentTimeChange(song.range[0]);
  };

  const mergeTracks = () => {
    const selectedSongs = songs.filter((song) => song.selected);
    if (selectedSongs.length > 1) {
      let name = selectedSongs
        .map((song) => song.name)
        .filter((name) => name !== "")
        .join("-");
      let minStart = Math.min(...selectedSongs.map((song) => song.range[0]));
      let maxEnd = Math.max(...selectedSongs.map((song) => song.range[1]));
      let mergedSong: Song = {
        name,
        range: [minStart, maxEnd],
        selected: true,
      };
      let firstSelectedSongIndex = songs.findIndex((song) => song.selected);
      songs = songs.filter((song) => !song.selected);
      songs.splice(firstSelectedSongIndex, 0, mergedSong);
    }
  };

  const splitTracks = () => {
    const selectedSongs = songs.filter((song) => song.selected);
    selectedSongs.forEach((song) => {
      if (currentTime > song.range[0] && currentTime < song.range[1]) {
        let firstHalf: Song = {
          name: song.name ? song.name + "-1" : "",
          range: [song.range[0], currentTime],
          selected: true,
        };
        let secondHalf: Song = {
          name: song.name ? song.name + "-2" : "",
          range: [currentTime, song.range[1]],
          selected: true,
        };
        let originalIndex = songs.findIndex((s) => s === song);
        songs = songs.filter((s) => s !== song);
        songs.splice(originalIndex, 0, firstHalf, secondHalf);
      }
    });
  };

  const moveSlider = (deltaX: number) => {
    const newStart = scale.viewDomain[0] + deltaX;
    const newEnd = scale.viewDomain[1] + deltaX;
    const newWindows = [newStart, newEnd] as [number, number];
    scale = reScale(scale, newWindows);
  };

  const scaleTimeline = (deltaY: number, scaleTo: number) => {
    const [scaleToDomain, _] = mapRangeToViewDomain(scale, [scaleTo, scaleTo]);
    const newStart = scale.viewDomain[0] - deltaY;
    const newEnd = scale.viewDomain[1] + deltaY;
    const newWindows = [newStart, newEnd] as [number, number];
    const newScale = reScale(scale, newWindows);
    const [newScaleToDomain, __] = mapRangeToViewDomain(newScale, [
      scaleTo,
      scaleTo,
    ]);

    if (newScaleToDomain !== scaleToDomain) {
      const delta = scaleToDomain - newScaleToDomain;
      scale = reScale(scale, [newStart + delta, newEnd + delta]);
    } else {
      scale = reScale(scale, newWindows);
    }
  };

  const scaleOrMoveTimeline = (e: WheelEvent) => {
    e.preventDefault();
    if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {
      return moveSlider(e.deltaX);
    } else {
      const scaleTo = e.clientX - container.getBoundingClientRect().left;
      return scaleTimeline(e.deltaY, scaleTo);
    }
  };

  const addTrack = () => {
    songs = [...songs, makeEmptySong(scale.viewDomain, true)];
  };

  onMount(() => {
    scale = makeScale(domain, [0, container.clientWidth]);
  });
</script>

<ContextMenu bind:songs bind:scale>
  <div class="overflow-hidden">
    <div class="flex items-center gap-2">
      <button class="btn" on:click={addTrack}>
        <IconPlus />
        Add track
      </button>
      <button class="btn" on:click={mergeTracks}>
        <IconCirclesRelation />
        Merge
      </button>
      <button class="btn" on:click={splitTracks}>
        <IconSpacingHorizontal />
        Split
      </button>
    </div>
    <div class="flex">
      <div>
        <div class="h-10 w-96" />
        {#each songs as song}
          <div
            class="h-[50px] px-2 py-1 -mt-[1px] border border-light-grey flex gap-2 items-center"
          >
            <button on:click={playSong(song)}>
              <IconPlayerPlay class="w-6 h-6" />
            </button>
            <div>
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
          </div>
        {/each}
      </div>
      <div class="relative flex-1 overflow-hidden" bind:this={container}>
        {#if scale}
          <Indicator {scale} value={currentTime} {onCurrentTimeChange} />
          <XAxis {scale} {onCurrentTimeChange} onWheel={scaleOrMoveTimeline} />
          <div on:wheel={scaleOrMoveTimeline}>
            {#each songs as song}
              <Track bind:song bind:scale />
            {/each}
          </div>
          <Slider
            bind:value={scale.viewDomain}
            min={domain[0]}
            max={domain[1]}
          />
        {/if}
      </div>
    </div>
  </div>
</ContextMenu>
