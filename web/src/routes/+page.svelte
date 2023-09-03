<script lang="ts">
  import Clip from "$lib/components/clip.svelte";
</script>

<div class="flex flex-col gap-8 p-2">
  <section class="flex flex-col gap-4">
    <h1 class="text-2xl font-semibold">New</h1>
    <ul class="grid grid-cols-6 gap-6">
      <li><Clip /></li>
      <li><Clip /></li>
      <li><Clip /></li>
      <li><Clip /></li>
      <li><Clip /></li>
      <li><Clip /></li>
    </ul>
  </section>
  <section class="flex flex-col gap-4">
    <h1 class="text-2xl font-semibold">Hot</h1>
    <ul class="grid grid-cols-6 gap-6">
      <li><Clip /></li>
      <li><Clip /></li>
      <li><Clip /></li>
      <li><Clip /></li>
      <li><Clip /></li>
      <li><Clip /></li>
    </ul>
  </section>
</div>
