<script lang="ts">
  import "../app.css";
  import Player from "$lib/components/player.svelte";
  import FullscreenPlayer from "$lib/components/fullscreen_player.svelte";
  import FloatingYoutube from "$lib/components/floating_youtube.svelte";
  import Sidebar from "$lib/components/sidebar.svelte";

  let isFullScreenPlayerOpen: boolean = false;
</script>

<FloatingYoutube>
  <div class="flex flex-col h-screen gap-2 p-2">
    <div class="flex flex-1 gap-2">
      <Sidebar bind:isFullScreenPlayerOpen />
      <div class="flex-1 min-w-0">
        <slot />
      </div>
    </div>
    <Player bind:isFullScreenPlayerOpen />
    <FullscreenPlayer bind:isFullScreenPlayerOpen />
  </div>
</FloatingYoutube>
