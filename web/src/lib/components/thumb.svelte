<script lang="ts">
  import { useDrag } from "$lib/hooks/use_drag";

  export let offset: number;
  export let onChange: (delta: number) => void;
  export let onDropped: () => void;

  const { moving, drag } = useDrag(onChange, onDropped);
</script>

<button
  on:mousedown={drag}
  style={`left: calc(${offset * 100}% + (${-16 * offset}px))`}
  class={`absolute bg-white rounded h-4 w-4 outline-dodger-blue outline-offset-1 ${
    $moving ? "outline" : ""
  }`}
/>
