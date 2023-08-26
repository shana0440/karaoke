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

  export let scale: Scale;
  export let domain: [number, number];
  export let name: string | undefined;
  export let selected = false;
  type Movable = 0 | 1 | "both";
  let moving: Option<Movable> = none;

  const moveWindow = (index: 0 | 1) => (delta: number) => {
    const newValue = domain[index] + calculateViewDomainDelta(scale, delta);
    domain[index] = constrainDomain(scale, newValue);
    domain = [...domain];
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
      selected = !selected;
    }
  };

  $: range = mapViewDomainToRange(scale, domain);
</script>

<div class="track relative py-1 border border-light-grey -mt-[1px]">
  <div
    style={`${toTranslate(range)}${toWidth(range)}`}
    class={`flex gap-1 rounded ${
      selected ? "bg-dodger-blue" : "bg-purple-taupe"
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
      {name ?? ""}
    </button>
    <button class="h-10 p-1 cursor-col-resize" on:mousedown={drag(1)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
  </div>
</div>
