<script lang="ts">
  import Youtube from "$lib/components/youtube.svelte";
  import { page } from "$app/stores";
  import { onMount } from "svelte";
  import type { YouTubePlayer } from "youtube-player/dist/types";
  import Timeline from "$lib/components/timeline.svelte";
  import type { Song } from "../../domains/song";

  const id = $page.url.searchParams.get("id") ?? "";
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

  const handlePredict = async () => {
    const url = await player.getVideoUrl();
    loading = true;
    fetch("http://localhost:3000/predict/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    })
      .then((res) => res.json())
      .then((res) => {
        songs = res.timeslots
          .filter((timeslot: [number, number]) => timeslot[0] < duration)
          .map((timeslot: [number, number]) => ({
            range: timeslot,
          }));
      })
      .finally(() => {
        loading = false;
      });
  };

  onMount(() => {
    if (!id) {
      window.location.href = "/";
    }
    player.on("stateChange", async (e) => {
      player.getDuration().then((value) => {
        duration = value;
      });
    });
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
</script>

<div class="flex flex-col w-screen overflow-hidden">
  <Youtube {id} bind:player />
  <button class="btn" on:click={handlePredict}
    >{loading ? "Loading..." : "Predict"}</button
  >
  {#if duration}
    <Timeline
      domain={[0, duration]}
      bind:songs
      {currentTime}
      onCurrentTimeChange={udpateYoutubeCurrentTime}
    />
  {/if}
</div>
