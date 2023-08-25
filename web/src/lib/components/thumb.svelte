<script lang="ts">
  import { onMount } from "svelte";

  export let offset: number;
  export let onChange: (delta: number) => void;
  export let onDropped: () => void;

  let isMoving = false;
  let prevClientX = 0;
  const handleMove = (e: MouseEvent) => {
    if (isMoving) {
      onChange(e.clientX - prevClientX);
      prevClientX = e.clientX;
    }
  };

  const handleDrop = (e: MouseEvent) => {
    if (isMoving) {
      onChange(e.clientX - prevClientX);
      prevClientX = e.clientX;
      isMoving = false;
      onDropped();
    }
  };

  const startDrag = (e: MouseEvent) => {
    prevClientX = e.clientX;
    isMoving = true;
  };

  onMount(() => {
    window.addEventListener("mousemove", handleMove);
    window.addEventListener("mouseup", handleDrop);

    return () => {
      window.removeEventListener("mousemove", handleMove);
      window.removeEventListener("mouseup", handleDrop);
    };
  });
</script>

<button
  on:mousedown={startDrag}
  style={`left: calc(${offset * 100}% + (${-16 * offset}px))`}
  class={`absolute bg-white rounded h-4 w-4 outline-dodger-blue outline-offset-1 ${
    isMoving ? "outline" : ""
  }`}
/>
