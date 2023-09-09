<script lang="ts">
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import type { YouTubePlayer } from "youtube-player/dist/types";
  import Tracks from "$lib/components/tracks.svelte";
  import MostLikeComment from "$lib/components/most_like_comment.svelte";
  import VideoEditor from "$lib/components/video_editor.svelte";
  import VideoPreview from "$lib/components/video_preview.svelte";

  const id = $page.params.video_id ?? "";
  let player: YouTubePlayer;
  let duration: number = 0;
  let currentTime: number = 0;

  const udpateYoutubeCurrentTime = (time: number) => {
    // update current time directly to avoid the jitter
    currentTime = time;
    player.seekTo(time, true);
  };

  onMount(() => {
    player.on("stateChange", async (e) => {
      player.getDuration().then((value) => {
        duration = value;
      });
    });
  });
</script>

<VideoEditor>
  <div class="flex flex-col w-full h-full">
    <div class="flex gap-2 h-[400px] overflow-hidden">
      <div class="flex flex-col h-full gap-2 w-96">
        <h2 class="text-xl">Most Like Comment</h2>
        <div class="flex-1 min-h-0 border border-transparent-red overflow-auto">
          <MostLikeComment videoId={id} />
        </div>
      </div>
      <div class="flex flex-col flex-1 gap-2">
        <VideoPreview bind:player bind:duration {id} bind:currentTime />
      </div>
    </div>
    <div class="flex-1">
      {#if duration}
        <Tracks
          domain={[0, duration]}
          {currentTime}
          onCurrentTimeChange={udpateYoutubeCurrentTime}
        />
      {/if}
    </div>
  </div>
</VideoEditor>
