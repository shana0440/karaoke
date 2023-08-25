<script lang="ts">
  import { range } from "fp-ts/lib/NonEmptyArray";
  import {
    type Scale,
    calculateGap,
    mapRangeToViewDomain,
  } from "../../scale/scale";
  import AxisLabel from "./axis_label.svelte";

  export let scale: Scale;
  export let onCurrentTimeChange: (time: number) => void;

  let axis: HTMLDivElement;

  const updateCurrentTime = (e: MouseEvent) => {
    const target = e.target as HTMLElement;
    const offset = axis.getBoundingClientRect().left;
    if (axis.contains(target)) {
      const [currentTime, _] = mapRangeToViewDomain(scale, [
        e.clientX - offset,
        e.clientX - offset,
      ]);
      onCurrentTimeChange(currentTime);
    }
  };

  $: gap = calculateGap(scale);
  $: interval = range(
    Math.floor(scale.viewDomain[0]),
    Math.floor(scale.viewDomain[1])
  ).filter((value, _) => {
    return Math.floor(value) % gap === 0;
  });
</script>

<div
  role="button"
  tabindex="-1"
  class="flex w-full h-10"
  on:mousedown={updateCurrentTime}
  bind:this={axis}
>
  {#each interval as value}
    <AxisLabel {scale} {value} />
  {/each}
</div>
