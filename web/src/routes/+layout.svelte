<script lang="ts">
  import "../app.css";
  import Player from "$lib/components/player.svelte";
  import FullscreenPlayer from "$lib/components/fullscreen_player.svelte";
  import FloatingYoutube from "$lib/components/floating_youtube.svelte";
  import Sidebar from "$lib/components/sidebar.svelte";
  import Toaster from "$lib/components/toaster.svelte";
  import LoadingOverlay from "$lib/components/loading_overlay.svelte";

  let isFullScreenPlayerOpen: boolean = false;
</script>

<Toaster />
<LoadingOverlay />
<FloatingYoutube>
  <div class="flex flex-col h-screen gap-2 p-2">
    <div class="flex flex-1 gap-2 overflow-hidden">
      <Sidebar bind:isFullScreenPlayerOpen />
      <div class="flex-1 min-w-0 overflow-auto rounded-lg">
        <slot />
      </div>
    </div>
    <Player bind:isFullScreenPlayerOpen />
    <FullscreenPlayer bind:isFullScreenPlayerOpen />
  </div>
</FloatingYoutube>
