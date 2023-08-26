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

  let moving: Option<0 | 1> = none;

  const { drag: _drag } = useDrag(
    (delta) => {
      if (isSome(moving)) {
        moveWindow(moving.value)(delta);
      }
    },
    () => {
      moving = none;
    }
  );

  const drag = (index: 0 | 1) => (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    moving = some(index);
    _drag(e);
  };

  const moveWindow = (index: 0 | 1) => (delta: number) => {
    const newValue = domain[index] + calculateViewDomainDelta(scale, delta);
    domain[index] = constrainDomain(scale, newValue);
    domain = [...domain];
  };

  $: range = mapViewDomainToRange(scale, domain);
</script>

<div class="track relative py-1 border border-light-grey -mt-[1px]">
  <div
    style={`${toTranslate(range)}${toWidth(range)}`}
    class="flex w-10 gap-1 bg-red-500 rounded"
  >
    <button class="p-1 cursor-col-resize" on:mousedown={drag(0)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
    <span class="flex-1 h-10 py-2 truncate">{name ?? ""}</span>
    <button class="p-1 cursor-col-resize" on:mousedown={drag(1)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
  </div>
</div>
