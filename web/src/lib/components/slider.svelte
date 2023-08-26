<script lang="ts">
  import Thumb from "./thumb.svelte";
  import { useDrag } from "$lib/hooks/use_drag";

  export let value: [number, number];
  export let min: number;
  export let max: number;

  let container: HTMLDivElement;

  $: windows = [(value[0] - min) / max, (value[1] - min) / max];

  const moveWindow = (index: 0 | 1) => (delta: number) => {
    const newValue =
      value[index] + (delta / container.clientWidth) * (max - min);
    value[index] = Math.min(Math.max(newValue, min), max);
    value = [...value];
  };

  const sortValue = () => {
    if (value[0] > value[1]) {
      value = [value[1], value[0]];
    }
  };

  const { moving, drag } = useDrag((delta) => {
    moveWindow(0)(delta);
    moveWindow(1)(delta);
  });

  $: range = windows.sort();
</script>

<div bind:this={container} class="relative flex items-center py-2">
  <div class="w-full h-2 border bg-gunmetal border-cod-gray" />
  <button
    on:mousedown={drag}
    style={`left: ${range[0] * 100}%; right: ${100 - range[1] * 100}%`}
    class={`absolute h-2 transition bg-purple-taupe hover:scale-y-150 ${
      $moving ? "scale-y-150" : ""
    }`}
  />
  <Thumb offset={windows[0]} onChange={moveWindow(0)} onDropped={sortValue} />
  <Thumb offset={windows[1]} onChange={moveWindow(1)} onDropped={sortValue} />
</div>
