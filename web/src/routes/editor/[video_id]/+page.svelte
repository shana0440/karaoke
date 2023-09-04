<script lang="ts">
  import Youtube from "$lib/components/youtube.svelte";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import type { YouTubePlayer } from "youtube-player/dist/types";
  import Timeline from "$lib/components/timeline.svelte";
  import type { Song } from "$lib/domains/song";
  import MostLikeComment from "$lib/components/most_like_comment.svelte";
  import { IconCloudUp, IconLoader3 } from "@tabler/icons-svelte";
  import { useApi } from "$lib/hooks/use_api";
  import { predict, saveClips } from "$lib/api/api";

  const id = $page.params.video_id ?? "";
  let player: YouTubePlayer;
  let duration: number = 0;
  let currentTime: number = 0;
  let songs: Song[] = [];
  let loading = false;

  const udpateYoutubeCurrentTime = (time: number) => {
    // update current time directly to avoid the jitter
    currentTime = time;
    player.seekTo(time, true);
  };

  const apiClient = useApi();
  const handlePredict = async () => {
    const url = await player.getVideoUrl();
    loading = true;
    predict(apiClient, { url })
      .then((resp) => {
        songs = resp.timeslots
          .filter((timeslot: [number, number]) => timeslot[0] < duration)
          .map((timeslot: [number, number]) => ({
            range: timeslot,
            selected: false,
          }));
      })
      .finally(() => {
        loading = false;
      });
  };

  const saveSongs = async () => {
    saveClips(apiClient, {
      videoUrl: await player.getVideoUrl(),
      clips: songs.map((song) => ({
        name: song.name,
        startAt: song.range[0],
        endAt: song.range[1],
      })),
    });
  };

  onMount(() => {
    player.on("stateChange", async (e) => {
      player.getDuration().then((value) => {
        duration = value;
      });
    });
  });
</script>

<div class="flex flex-col overflow-hidden">
  <div class="flex gap-2">
    <div class="w-96">
      <h2>Most Like Comment</h2>
      <MostLikeComment videoId={id} />
    </div>
    <div class="flex flex-col flex-1 gap-2">
      <div class="flex-1 aspect-video">
        <Youtube {id} bind:player bind:currentTime />
      </div>
      <div class="grid grid-cols-3">
        <div />
        <div class="flex items-center justify-center">01:10</div>
        <div class="flex justify-end gap-2">
          <button class="btn" on:click={handlePredict}>
            <IconLoader3 />
            Predict
          </button>
          <button class="btn" on:click={saveSongs}>
            <IconCloudUp />
            Save
          </button>
        </div>
      </div>
    </div>
  </div>
  {#if duration}
    <Timeline
      domain={[0, duration]}
      bind:songs
      {currentTime}
      onCurrentTimeChange={udpateYoutubeCurrentTime}
    />
  {/if}
</div>
