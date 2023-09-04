<script lang="ts">
  import { onMount } from "svelte";
  import YoutubePlayer from "youtube-player";

  export let id: string;
  export let player: ReturnType<typeof YoutubePlayer>;

  onMount(() => {
    player = YoutubePlayer("player");
    player.loadVideoById(id);
  });

  $: {
    if (id && player) {
      player.loadVideoById(id);
    }
  }
</script>

<div class="yt-player" id="player" />
