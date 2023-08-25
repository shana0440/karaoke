<script lang="ts">
  import Youtube from "$lib/components/youtube.svelte";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import type { YouTubePlayer } from "youtube-player/dist/types";
  import Timeline from "$lib/components/timeline.svelte";

  const id = $page.url.searchParams.get("id") ?? "";
  let player: YouTubePlayer;
  let duration: number = 0;
  let currentTime: number = 0;

  const udpateYoutubeCurrentTime = (time: number) => {
    player.seekTo(time, true);
  };

  onMount(() => {
    if (!id) {
      window.location.href = "/";
    }
    player.on("stateChange", async (e) => {
      console.log("stateChange");
      player.getDuration().then((value) => {
        duration = value;
      });
    });
    const updateCurrentTime = (e: MessageEvent<string>) => {
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
    window.addEventListener("message", updateCurrentTime);
    return () => {
      window.removeEventListener("message", updateCurrentTime);
    };
  });
</script>

<div class="flex flex-col w-screen h-screen overflow-hidden">
  <Youtube {id} bind:player />
  {#if duration}
    <Timeline
      domain={[0, duration]}
      {currentTime}
      onCurrentTimeChange={udpateYoutubeCurrentTime}
    />
  {/if}
</div>
