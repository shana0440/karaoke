<script lang="ts">
  import {
    mapViewDomainToRange,
    toTranslate,
    type Scale,
  } from "$lib/scale/scale";
  import { formatTime } from "$lib/time/time";
  import TimeFormat from "./time_format.svelte";

  export let value: number;
  export let scale: Scale;

  const getAxisRange = (value: number): [number, number] => {
    const range = mapViewDomainToRange(scale, [value, value]);
    // 32 is half of label width
    return [range[0] - 32, range[1] + 32];
  };
  $: axisRange = getAxisRange(value);
  $: labelOffset =
    axisRange[0] < scale.range[0]
      ? -axisRange[0]
      : axisRange[1] > scale.range[1]
      ? -(axisRange[1] - scale.range[1])
      : 0;
</script>

<div
  class={`absolute flex flex-col gap-1 w-16 items-center`}
  style={toTranslate(axisRange)}
>
  <span
    class="text-sm text-light-grey"
    style={`transform: translateX(${labelOffset}px)`}
  >
    <TimeFormat {value} />
  </span>
  <span
    class="w-[1px] h-4 text-sm bg-light-grey"
    data-time={formatTime(value)}
  />
</div>
