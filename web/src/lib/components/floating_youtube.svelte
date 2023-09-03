<script lang="ts" context="module">
  export type FloatingYoutubeContext = {
    move: (rect: {
      top: number;
      height: number;
      left: number;
      width: number;
    }) => void;
  };
</script>

<script lang="ts">
  import { setContext } from "svelte";

  import Youtube from "./youtube.svelte";
  import type { YouTubePlayer } from "youtube-player/dist/types";

  let player: YouTubePlayer;
  let ytBox: HTMLDivElement;

  setContext<FloatingYoutubeContext>("floating-yt", {
    move: ({ top, height, left, width }) => {
      if (ytBox) {
        ytBox.style.top = `${top}px`;
        ytBox.style.height = `${height}px`;
        ytBox.style.left = `${left}px`;
        ytBox.style.width = `${width}px`;
      }
    },
  });
</script>

<slot />
<div class="absolute z-20 overflow-hidden rounded-lg" bind:this={ytBox}>
  <Youtube id="JQyRUVvusuY" bind:player />
</div>
