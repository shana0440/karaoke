<script lang="ts">
  import { onMount } from "svelte";
  import YoutubePlayer from "youtube-player";

  export let id: string;
  export let player: ReturnType<typeof YoutubePlayer>;
  export let currentTime;

  const elementId = `yt-${Date.now()}`;

  onMount(() => {
    player = YoutubePlayer(elementId);
    player.loadVideoById(id);
    const subscribeCurrentTimeUpdated = (e: MessageEvent<string>) => {
      try {
        const data = JSON.parse(e.data);
        // "{\"event\":\"infoDelivery\",\"info\":{\"currentTime\":3850.575187,\"videoBytesLoaded\":0.6524905538441726,\"videoLoadedFraction\":0.6524905538441726,\"currentTimeLastUpdated_\":1692837082.604,\"playbackRate\":1,\"mediaReferenceTime\":3850.575541},\"id\":6,\"channel\":\"widget\"}"
        if (data.info.currentTime) {
          currentTime = data.info.currentTime;
        }
      } catch (e) {
        // ignore error, becuase not every message is come from youtube iframe
      }
    };
    window.addEventListener("message", subscribeCurrentTimeUpdated);
    return () => {
      window.removeEventListener("message", subscribeCurrentTimeUpdated);
    };
  });

  $: {
    if (id && player) {
      player.loadVideoById(id);
    }
  }
</script>

<div class="yt-player" id={elementId} />
