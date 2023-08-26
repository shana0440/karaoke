<script lang="ts">
  import {
    mapViewDomainToRange,
    toTranslate,
    type Scale,
    mapRangeToViewDomain,
  } from "../../scale/scale";
  import { useDrag } from "$lib/hooks/use_drag";

  export let scale: Scale;
  export let value: number;
  export let onCurrentTimeChange: (time: number) => void;

  // this value is used to separate real value and temp value for drag and drop
  let internalValue: number;

  const getIndicatorRange = (value: number): [number, number] => {
    const range = mapViewDomainToRange(scale, [value, value]);
    // 8 is half of indicator width
    return [range[0] - 8, range[1] + 8];
  };
  $: range = getIndicatorRange(internalValue);

  const { moving, drag } = useDrag(
    (delta) => {
      const [position, _] = mapRangeToViewDomain(scale, [
        range[0] + delta + 8,
        range[1] + delta - 8,
      ]);
      internalValue = position;
    },
    () => {
      onCurrentTimeChange(internalValue);
    }
  );

  $: {
    if (!$moving) {
      internalValue = value;
    }
  }
</script>

<button
  class="absolute z-10 flex flex-col items-center h-full mt-5"
  style={toTranslate(range)}
  on:mousedown={drag}
>
  <div
    class={`bg-white rounded h-4 w-4 outline-dodger-blue outline-offset-1`}
  />
  <div class="w-1 h-full bg-dodger-blue" />
</button>
