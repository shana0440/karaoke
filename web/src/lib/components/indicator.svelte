<script lang="ts">
  import {
    mapViewDomainToRange,
    toTranslate,
    type Scale,
  } from "../../scale/scale";

  export let scale: Scale;
  export let value: number;

  const getAxisRange = (value: number): [number, number] => {
    const range = mapViewDomainToRange(scale, [value, value]);
    // 8 is half of indicator width
    return [range[0] - 8, range[1] + 8];
  };
  $: range = getAxisRange(value);
</script>

<div
  class="absolute z-10 flex flex-col items-center h-full mt-5"
  style={toTranslate(range)}
>
  <button
    class={`bg-white rounded h-4 w-4 outline-dodger-blue outline-offset-1`}
  />
  <div class="w-1 h-full bg-dodger-blue" />
</div>
