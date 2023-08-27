<script lang="ts">
  import {
    toTranslate,
    mapViewDomainToRange,
    type Scale,
    calculateViewDomainDelta,
    constrainDomain,
    toWidth,
  } from "../../scale/scale";
  import { type Option, none, some, isSome } from "fp-ts/Option";
  import { useDrag } from "$lib/hooks/use_drag";
  import { useContextMenu } from "$lib/hooks/use_contextmenu";
  import type { Song } from "../../domains/song";

  export let scale: Scale;
  export let song: Song;
  type Movable = 0 | 1 | "both";
  let moving: Option<Movable> = none;

  const moveWindow = (index: 0 | 1) => (delta: number) => {
    const newValue = song.range[index] + calculateViewDomainDelta(scale, delta);
    song.range[index] = constrainDomain(scale, newValue);
    song.range = [...song.range];
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
      song.selected = !song.selected;
    }
  };

  const { open } = useContextMenu();

  $: range = mapViewDomainToRange(scale, song.range);
</script>

<div class="track relative py-1 border border-light-grey -mt-[1px]">
  <div
    style={`${toTranslate(range)}${toWidth(range)}`}
    class={`flex gap-1 rounded ${
      song.selected ? "bg-dodger-blue" : "bg-purple-taupe"
    }`}
  >
    <button class="h-10 p-1 cursor-col-resize" on:mousedown={drag(0)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
    <button
      on:click={selectThumb}
      on:contextmenu={open(song)}
      on:mousedown={drag("both")}
      class="flex-1 h-10 py-2 truncate"
    >
      {song.name ?? ""}
    </button>
    <button class="h-10 p-1 cursor-col-resize" on:mousedown={drag(1)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
  </div>
</div>
