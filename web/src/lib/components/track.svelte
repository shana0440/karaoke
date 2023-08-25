<script lang="ts">
  import { onMount } from "svelte";
  import {
    toTranslate,
    mapViewDomainToRange,
    type Scale,
    calculateViewDomainDelta,
    constrainDomain,
    toWidth,
  } from "../../scale/scale";
  import { type Option, none, some, isSome } from "fp-ts/Option";

  export let scale: Scale;
  export let domain: [number, number];
  export let name: string | undefined;

  let moving: Option<0 | 1> = none;
  let prevClientX = 0;
  const dragDomain = (index: 0 | 1) => (e: MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    moving = some(index);
    prevClientX = e.clientX;
  };

  const moveWindow = (index: 0 | 1) => (delta: number) => {
    const newValue = domain[index] + calculateViewDomainDelta(scale, delta);
    domain[index] = constrainDomain(scale, newValue);
    domain = [...domain];
  };

  const handleMove = (e: MouseEvent) => {
    if (isSome(moving)) {
      moveWindow(moving.value)(e.clientX - prevClientX);
      prevClientX = e.clientX;
    }
  };

  const handleDrop = (e: MouseEvent) => {
    if (isSome(moving)) {
      moveWindow(moving.value)(e.clientX - prevClientX);
      prevClientX = e.clientX;
      moving = none;
    }
  };

  onMount(() => {
    window.addEventListener("mousemove", handleMove);
    window.addEventListener("mouseup", handleDrop);

    return () => {
      window.removeEventListener("mousemove", handleMove);
      window.removeEventListener("mouseup", handleDrop);
    };
  });

  $: range = mapViewDomainToRange(scale, domain);
</script>

<div class="track relative py-1 border border-light-grey -mt-[1px]">
  <div
    style={`${toTranslate(range)}${toWidth(range)}`}
    class="flex w-10 gap-1 bg-red-500 rounded"
  >
    <button class="p-1 cursor-col-resize" on:mousedown={dragDomain(0)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
    <span class="flex-1 h-10 py-2 truncate">{name ?? ""}</span>
    <button class="p-1 cursor-col-resize" on:mousedown={dragDomain(1)}>
      <div class="w-1 h-full rounded-full bg-white/60" />
    </button>
  </div>
</div>
