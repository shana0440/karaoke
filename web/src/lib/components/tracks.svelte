<script lang="ts">
  import { onMount } from "svelte";
  import { IconPlayerPlayFilled } from "@tabler/icons-svelte";
  import {
    makeScale,
    reScale,
    mapRangeToViewDomain,
    reRange,
  } from "$lib/scale/scale";
  import Slider from "./slider.svelte";
  import TrackView from "./track.svelte";
  import XAxis from "./x_axis.svelte";
  import TimeFormat from "./time_format.svelte";
  import Indicator from "./indicator.svelte";
  import { useVideoEditor } from "$lib/hooks/use_video_editor";
  import type { Track } from "$lib/domains/track";
  import { isSome, match, some } from "fp-ts/Option";
  import { pipe } from "fp-ts/lib/function";
  import TimeEditable from "./time_editable.svelte";

  export let domain: [number, number];
  export let currentTime: number;
  export let onCurrentTimeChange: (time: number) => void;

  const {
    tracks,
    scale,
    mergeTracks: _mergeTracks,
    splitTracks: _splitTracks,
  } = useVideoEditor();

  let container: HTMLDivElement;

  const playSong = (track: Track) => () => {
    onCurrentTimeChange(track.range[0]);
  };

  const moveSlider = (deltaX: number) => {
    scale.update((prev) =>
      pipe(
        prev,
        match(
          () => prev,
          (scale) => {
            const newStart = scale.viewDomain[0] + deltaX;
            const newEnd = scale.viewDomain[1] + deltaX;
            const newWindows = [newStart, newEnd] as [number, number];
            return some(reScale(scale, newWindows));
          }
        )
      )
    );
  };

  const scaleTimeline = (deltaY: number, scaleTo: number) => {
    scale.update((prev) => {
      return pipe(
        prev,
        match(
          () => prev,
          (scale) => {
            const [scaleToDomain, _] = mapRangeToViewDomain(scale, [
              scaleTo,
              scaleTo,
            ]);
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
            return some(scale);
          }
        )
      );
    });
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

  const changeScaleRange = () => {
    scale.update((prev) =>
      pipe(
        prev,
        match(
          () => prev,
          (scale) => some(reRange(scale, [0, container.clientWidth]))
        )
      )
    );
  };

  onMount(() => {
    scale.set(some(makeScale(domain, [0, container.clientWidth])));
    window.addEventListener("resize", changeScaleRange);
    return () => {
      window.removeEventListener("resize", changeScaleRange);
    };
  });
</script>

<div class="relative h-full">
  <div class="absolute inset-0 flex pointer-events-none">
    <div class="pointer-events-none w-96" />
    <div class="relative flex-1 overflow-hidden">
      {#if isSome($scale)}
        <Indicator
          scale={$scale.value}
          value={currentTime}
          {onCurrentTimeChange}
        />
      {/if}
    </div>
  </div>
  <div class="flex flex-col h-full overflow-hidden">
    <div class="flex">
      <div class="h-10 w-96" />
      <div class="flex-1" bind:this={container}>
        {#if isSome($scale)}
          <XAxis
            scale={$scale.value}
            {onCurrentTimeChange}
            onWheel={scaleOrMoveTimeline}
          />
        {/if}
      </div>
    </div>
    <div class="flex-grow min-h-0 overflow-y-auto basis-0">
      <div>
        {#if isSome($scale)}
          {#each $tracks as track}
            <div class="flex border border-light-grey">
              <div
                class="h-[50px] px-2 py-1 flex gap-2 items-center w-96 border-r border-light-grey"
              >
                <button on:click={playSong(track)}>
                  <IconPlayerPlayFilled class="w-6 h-6" />
                </button>
                <div>
                  <input
                    class="bg-transparent"
                    bind:value={track.name}
                    placeholder="Unknown"
                  />
                  <div class="text-sm text-light-grey">
                    <TimeEditable bind:time={track.range[0]} />
                    ~
                    <TimeEditable bind:time={track.range[1]} />
                    (<TimeFormat value={track.range[1] - track.range[0]} />)
                  </div>
                </div>
              </div>
              <div
                class="flex-1 overflow-hidden"
                on:wheel={scaleOrMoveTimeline}
              >
                <TrackView bind:track bind:scale={$scale.value} {currentTime} />
              </div>
            </div>
          {/each}
        {/if}
      </div>
    </div>
    {#if isSome($scale)}
      <div class="flex">
        <div class="w-96" />
        <div class="flex-1">
          <Slider
            bind:value={$scale.value.viewDomain}
            min={domain[0]}
            max={domain[1]}
          />
        </div>
      </div>
    {/if}
  </div>
</div>
