<script lang="ts">
  import { createSlider, melt } from "@melt-ui/svelte";
  import { writable } from "svelte/store";

  export let value: [number, number];
  export let min: number;
  export let max: number;

  let valuePipe = writable<number[]>(value);

  const {
    elements: { root, range, thumb },
    options: { max: slideMax, min: slideMin },
    states: { value: slideValue },
  } = createSlider({
    defaultValue: [20, 80],
    step: 1,
    value: valuePipe,
  });

  $: {
    slideMax.set(max);
    slideMin.set(min);
  }

  $: {
    value = $slideValue as [number, number];
  }

  $: {
    valuePipe.set(value);
  }
</script>

<span use:melt={$root} class="relative flex h-[20px] items-center">
  <span class="block h-2 w-full bg-gunmetal">
    <span use:melt={$range} class="h-2 bg-purple-taupe" />
  </span>

  {#each $slideValue as _}
    <span
      use:melt={$thumb()}
      class="block h-5 w-5 rounded-full bg-alice-blue focus:ring-4 focus:ring-cod-gray/40"
    />
  {/each}
</span>
