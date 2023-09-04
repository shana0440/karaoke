<script lang="ts">
  import { fetchClips } from "$lib/api/api";
  import ClipCard from "$lib/components/clip.svelte";
  import type { Clip } from "$lib/domains/clip";
  import { useApi } from "$lib/hooks/use_api";
  import { onMount } from "svelte";

  const apiClient = useApi();
  let clips: Clip[] = [];

  onMount(() => {
    fetchClips(apiClient, { limit: 5 }).then((resp) => {
      clips = resp.data;
    });
  });
</script>

<div class="flex flex-col gap-8 p-2">
  <section class="flex flex-col gap-4">
    <h1 class="text-2xl font-semibold">New</h1>
    <ul class="grid gap-6 lg:grid-cols-5 md:grid-cols-3">
      {#each clips as clip}
        <li><ClipCard {clip} /></li>
      {/each}
    </ul>
  </section>
  <section class="flex flex-col gap-4">
    <h1 class="text-2xl font-semibold">Hot</h1>
    <ul class="grid gap-6 lg:grid-cols-5 md:grid-cols-3">
      {#each clips as clip}
        <li><ClipCard {clip} /></li>
      {/each}
    </ul>
  </section>
</div>
