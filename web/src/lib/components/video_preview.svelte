<script lang="ts">
  import Youtube from "$lib/components/youtube.svelte";
  import {
    IconCloudUp,
    IconLoader3,
    IconPlus,
    IconCirclesRelation,
    IconSpacingHorizontal,
  } from "@tabler/icons-svelte";
  import type { YouTubePlayer } from "youtube-player/dist/types";
  import { useApi } from "$lib/hooks/use_api";
  import { predict, saveClips } from "$lib/api/api";
  import { useVideoEditor } from "$lib/hooks/use_video_editor";
  import Tooltip from "./tooltip.svelte";

  export let player: YouTubePlayer;
  export let duration: number;
  export let id: string;
  export let currentTime: number;

  const {
    tracks,
    addTrack,
    mergeTracks: _mergeTracks,
    splitTracks: _splitTracks,
  } = useVideoEditor();

  const apiClient = useApi();
  const handlePredict = async () => {
    const url = await player.getVideoUrl();
    predict(apiClient, { url })
      .then((resp) => {
        tracks.set(
          resp.timeslots
            .filter((timeslot: [number, number]) => timeslot[0] < duration)
            .map((timeslot: [number, number]) => ({
              range: timeslot,
              selected: false,
            }))
        );
      })
      .finally(() => {});
  };

  const saveTracks = async () => {
    saveClips(apiClient, {
      videoUrl: await player.getVideoUrl(),
      clips: $tracks.map((song) => ({
        name: song.name,
        startAt: song.range[0],
        endAt: song.range[1],
      })),
    });
  };

  const mergeTracks = () => {
    const selectedTracks = $tracks.filter((it) => it.selected);
    _mergeTracks(selectedTracks);
  };

  const splitTracks = () => {
    const selectedTracks = $tracks.filter((it) => it.selected);
    _splitTracks(selectedTracks, currentTime);
  };
</script>

<div class="flex-1 aspect-video">
  <Youtube {id} bind:player bind:currentTime />
</div>
<div class="grid grid-cols-3">
  <div class="flex gap-2">
    <Tooltip description="Add new Track">
      <button class="btn" on:click={addTrack}>
        <IconPlus />
      </button>
    </Tooltip>
    <Tooltip description="Merge Selected Tracks">
      <button class="btn" on:click={mergeTracks}>
        <IconCirclesRelation />
      </button>
    </Tooltip>
    <Tooltip description="Split Selected Tracks">
      <button class="btn" on:click={splitTracks}>
        <IconSpacingHorizontal />
      </button>
    </Tooltip>
  </div>
  <div class="flex items-center justify-center">01:10</div>
  <div class="flex justify-end gap-2">
    <Tooltip description="Predict Tracks">
      <button class="btn" on:click={handlePredict}>
        <IconLoader3 />
      </button>
    </Tooltip>
    <Tooltip description="Save Tracks">
      <button class="btn" on:click={saveTracks}>
        <IconCloudUp />
      </button>
    </Tooltip>
  </div>
</div>
