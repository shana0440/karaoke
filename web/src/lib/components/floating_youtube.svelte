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
  import { onMount, setContext } from "svelte";
  import Youtube from "./youtube.svelte";
  import type { YouTubePlayer } from "youtube-player/dist/types";
  import { usePlayer } from "$lib/hooks/use_player";
  import { isSome } from "fp-ts/lib/Option";

  const { playingClip, updateTime, onPlay, onPause, onSyncToProgressBar } =
    usePlayer();
  let ytPlayer: YouTubePlayer;
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

  onMount(() => {
    const unsubscribePlay = onPlay(() => {
      ytPlayer.playVideo();
    });
    const unsubscribePause = onPause(() => {
      ytPlayer.pauseVideo();
    });
    const unsubscribeSync = onSyncToProgressBar((time) => {
      ytPlayer.seekTo(time, true);
    });
    const subscribeCurrentTimeUpdated = (e: MessageEvent<string>) => {
      try {
        const data = JSON.parse(e.data);
        // "{\"event\":\"infoDelivery\",\"info\":{\"currentTime\":3850.575187,\"videoBytesLoaded\":0.6524905538441726,\"videoLoadedFraction\":0.6524905538441726,\"currentTimeLastUpdated_\":1692837082.604,\"playbackRate\":1,\"mediaReferenceTime\":3850.575541},\"id\":6,\"channel\":\"widget\"}"
        if (data.info.currentTime) {
          updateTime(data.info.currentTime);
        }
      } catch (e) {
        // ignore error, becuase not every message is come from youtube iframe
      }
    };
    window.addEventListener("message", subscribeCurrentTimeUpdated);
    return () => {
      window.removeEventListener("message", subscribeCurrentTimeUpdated);
      unsubscribePause();
      unsubscribePlay();
      unsubscribeSync();
    };
  });
</script>

<slot />
{#if isSome($playingClip)}
  <div class="absolute z-20 overflow-hidden rounded-lg" bind:this={ytBox}>
    <Youtube id={$playingClip.value.video.resource_id} bind:player={ytPlayer} />
  </div>
{/if}
