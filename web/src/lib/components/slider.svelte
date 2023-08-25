<script lang="ts">
  import { onMount } from "svelte";
  import Thumb from "./thumb.svelte";

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

  let isMoving = false;
  let prevClientX = 0;
  const moveSlider = (e: MouseEvent) => {
    prevClientX = e.clientX;
    isMoving = true;
  };

  const handleMove = (e: MouseEvent) => {
    if (isMoving) {
      moveWindow(0)(e.clientX - prevClientX);
      moveWindow(1)(e.clientX - prevClientX);
      prevClientX = e.clientX;
    }
  };

  const handleDrop = (e: MouseEvent) => {
    if (isMoving) {
      moveWindow(0)(e.clientX - prevClientX);
      moveWindow(1)(e.clientX - prevClientX);
      prevClientX = e.clientX;
      isMoving = false;
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

  $: range = windows.sort();
</script>

<div bind:this={container} class="relative flex items-center py-2">
  <div class="w-full h-2 border bg-gunmetal border-cod-gray" />
  <button
    on:mousedown={moveSlider}
    style={`left: ${range[0] * 100}%; right: ${100 - range[1] * 100}%`}
    class={`absolute h-2 transition bg-purple-taupe hover:scale-y-150 ${
      isMoving ? "scale-y-150" : ""
    }`}
  />
  <Thumb offset={windows[0]} onChange={moveWindow(0)} onDropped={sortValue} />
  <Thumb offset={windows[1]} onChange={moveWindow(1)} onDropped={sortValue} />
</div>
