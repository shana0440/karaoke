<script lang="ts">
  import {
    toTranslate,
    mapViewDomainToRange,
    type Scale,
    calculateViewDomainDelta,
    constrainDomain,
    toWidth,
  } from "$lib/scale/scale";
  import { type Option, none, some, isSome } from "fp-ts/lib/Option";
  import { useDrag } from "$lib/hooks/use_drag";
  import type { Track } from "$lib/domains/track";
  import { createContextMenu, melt } from "@melt-ui/svelte";
  import { useVideoEditor } from "$lib/hooks/use_video_editor";

  const {
    elements: { menu, item, trigger },
  } = createContextMenu();

  export let scale: Scale;
  export let track: Track;
  export let currentTime: number;
  export let index: number;

  type Movable = 0 | 1 | "both";
  let moving: Option<Movable> = none;

  const { removeTrack, expandTimeline, addTrackToNext, addTrackToPrev } =
    useVideoEditor();

  const moveWindow = (index: 0 | 1) => (delta: number) => {
    const newValue =
      track.range[index] + calculateViewDomainDelta(scale, delta);
    track.range[index] = constrainDomain(scale, newValue);
    track.range = [...track.range];
  };

  const { isMoved, drag: _drag } = useDrag(
    (delta) => {
      if (isSome(moving)) {
        if (moving.value === "both") {
          moveWindow(0)(delta);
          moveWindow(1)(delta);
        } else {
          moveWindow(moving.value)(delta);
        }
      }
    },
    () => {
      moving = none;
    }
  );

  const drag = (index: Movable) => (e: MouseEvent) => {
    moving = some(index);
    _drag(e);
  };

  const selectThumb = (e: MouseEvent) => {
    if (!$isMoved) {
      track.selected = !track.selected;
    }
  };

  $: range = mapViewDomainToRange(scale, track.range);
</script>

<div class="track-container relative py-1" use:melt={$trigger}>
  <div
    style={`${toTranslate(range)}${toWidth(range)}`}
    data-index={index}
    class={`flex gap-1 rounded track ${
      track.selected ? "bg-dodger-blue" : "bg-purple-taupe"
    }`}
  >
    <button class="h-10 p-1 cursor-col-resize" on:mousedown={drag(0)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
    <button
      on:click={selectThumb}
      on:mousedown={drag("both")}
      class="flex-1 h-10 py-2 truncate"
    >
      {track.name ?? ""}
    </button>
    <button class="h-10 p-1 cursor-col-resize" on:mousedown={drag(1)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
  </div>
</div>

<div use:melt={$menu} class="menu">
  <button on:click={() => expandTimeline(track)} class="item" use:melt={$item}>
    Expand timeline
  </button>
  <button
    on:click={() => {
      track.range[0] = currentTime;
    }}
    class="item"
    use:melt={$item}
  >
    Start at current time
  </button>
  <button
    on:click={() => {
      track.range[1] = currentTime;
    }}
    class="item"
    use:melt={$item}
  >
    End at current time
  </button>
  <button on:click={() => addTrackToPrev(track)} class="item" use:melt={$item}>
    Add track to prev
  </button>
  <button on:click={() => addTrackToNext(track)} class="item" use:melt={$item}>
    Add track to next
  </button>
  <button on:click={() => removeTrack(track)} class="item" use:melt={$item}>
    Remove track
  </button>
</div>
