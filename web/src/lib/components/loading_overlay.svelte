<script lang="ts" context="module">
  import { writable } from "svelte/store";
  import Spinner from "./spinner.svelte";

  let isShow = writable(false);

  export function showLoadingOverlay() {
    isShow.set(true);
  }
  export function hideLoadingOverlay() {
    isShow.set(false);
  }
</script>

{#if $isShow}
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-cod-gray/50"
  >
    <Spinner />
  </div>
{/if}
