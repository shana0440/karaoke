<script lang="ts">
  import { onMount } from "svelte";

  export let loadMore: () => void;
  export let hasMore: boolean;

  let observer: IntersectionObserver;
  let loader: HTMLDivElement;

  $: {
    if (observer && hasMore) {
      observer.observe(loader);
    }
  }

  onMount(() => {
    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          loadMore();
        }
      });
    });

    return () => {
      observer.disconnect();
    };
  });
</script>

{#if hasMore}
  <div bind:this={loader}>
    <slot />
  </div>
{/if}
