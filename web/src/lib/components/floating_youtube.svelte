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
  import { isNone, isSome, match } from "fp-ts/lib/Option";
  import { pipe } from "fp-ts/lib/function";

  const {
    playingClip,
    tick,
    onPlay,
    onPause,
    onSyncToProgressBar,
    syncToProgressBar,
    pause,
    isPause,
    play,
  } = usePlayer();
  let ytPlayer: YouTubePlayer;
  let ytBox: HTMLDivElement;
  let currentTime: number = 0;

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

  $: {
    tick(currentTime);
  }

  const controlVideo = (e: KeyboardEvent) => {
    const element = e.target as HTMLElement;
    if (
      element.tagName.toLowerCase() === "input" ||
      element.hasAttribute("contenteditable")
    ) {
      return;
    }

    pipe(
      $playingClip,
      match(
        () => {},
        (clip) => {
          if (e.key === "ArrowLeft") {
            e.preventDefault();
            syncToProgressBar(Math.max(currentTime - 5, clip.start_at));
          }
          if (e.key === "ArrowRight") {
            e.preventDefault();
            syncToProgressBar(Math.min(currentTime + 5, clip.end_at));
          }
          if (e.key === " ") {
            e.preventDefault();
            if ($isPause) {
              play();
            } else {
              pause();
            }
          }
        }
      )
    );
  };

  onMount(() => {
    const unsubscribePlay = onPlay(() => {
      ytPlayer.playVideo();
    });
    const unsubscribePause = onPause(() => {
      ytPlayer.pauseVideo();
    });
    const unsubscribeSync = onSyncToProgressBar((time) => {
      setTimeout(() => {
        // FIXME: remove listener after trigger
        // youtube player api didn't provide unsubscribe method
        ytPlayer.on("apiChange", () => {
          ytPlayer.seekTo(time, true);
        });
        ytPlayer.seekTo(time, true);
      }, 0);
    });
    window.addEventListener("keydown", controlVideo);
    return () => {
      unsubscribePause();
      unsubscribePlay();
      unsubscribeSync();
      window.removeEventListener("keydown", controlVideo);
    };
  });
</script>

<slot />
<div
  class="absolute z-20 overflow-hidden rounded-lg"
  bind:this={ytBox}
  class:invisible={isNone($playingClip)}
>
  <Youtube
    id={isSome($playingClip) ? $playingClip.value.video.resource_id : ""}
    bind:player={ytPlayer}
    bind:currentTime
  />
</div>
