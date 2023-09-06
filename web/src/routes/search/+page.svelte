<script lang="ts">
  import {
    fetchChannels,
    searchChannels,
    searchClips,
    searchVideos,
  } from "$lib/api/api";
  import ChannelCard from "$lib/components/channel_card.svelte";
  import type { Channel } from "$lib/domains/channel";
  import { useApi } from "$lib/hooks/use_api";
  import { IconSearch } from "@tabler/icons-svelte";
  import { onMount } from "svelte";
  import { page } from "$app/stores";
  import { debounce } from "lodash";
  import { none, type Option, some, isSome } from "fp-ts/Option";
  import type { Clip } from "$lib/domains/clip";
  import type { Video } from "$lib/domains/video";
  import ClipItem from "$lib/components/clip_item.svelte";
  import { isHTMLInputElement } from "@melt-ui/svelte/internal/helpers";
  import type { FormEventHandler } from "svelte/elements";
  import VideoCard from "$lib/components/video_card.svelte";

  const apiClient = useApi();

  let channels: Channel[] = [];
  let searchResult: Option<{
    clips: Clip[];
    videos: Video[];
    channels: Channel[];
  }> = none;

  const inputSearch = debounce<FormEventHandler<HTMLInputElement>>((e) => {
    if (isHTMLInputElement(e.target)) {
      $page.url.searchParams.set("q", e.target.value);
      history.replaceState(history.state, "", $page.url);
      search(e.target.value);
    }
  }, 300);

  const search = (_search: string) => {
    const search = _search.trim();
    if (!search) {
      searchResult = none;
      return;
    }
    Promise.all([
      searchChannels(apiClient, { search, limit: 5 }),
      searchVideos(apiClient, { search, limit: 5 }),
      searchClips(apiClient, { search, limit: 5 }),
    ]).then(([channelsResp, videosResp, clipsResp]) => {
      searchResult = some({
        clips: clipsResp.data,
        videos: videosResp.data,
        channels: channelsResp.data,
      });
    });
  };

  onMount(() => {
    fetchChannels(apiClient, {}).then((resp) => {
      channels = resp.data;
    });
    const _search = $page.url.searchParams.get("q");
    if (_search) {
      search(_search);
    }
  });
</script>

<div class="flex flex-col gap-4 p-2">
  <div class="input w-[448px]">
    <IconSearch />
    <input
      placeholder="What do you want to listen to?"
      class="text-alice-blue placeholder:text-light-grey"
      on:input={inputSearch}
      value={$page.url.searchParams.get("q")}
    />
  </div>
  {#if isSome(searchResult)}
    <section class="flex flex-col gap-4">
      <h1 class="text-2xl font-semibold">Songs</h1>
      <div class="flex flex-col gap-2">
        {#each searchResult.value.clips as clip, i (clip)}
          <ClipItem {clip} index={i + 1} />
        {/each}
      </div>
    </section>
    <section class="flex flex-col gap-4">
      <h1 class="text-2xl font-semibold">Channels</h1>
      <div class="grid gap-6 lg:grid-cols-5 md:grid-cols-3">
        {#each searchResult.value.channels as channel (channel)}
          <ChannelCard {channel} />
        {/each}
      </div>
    </section>
    <section class="flex flex-col gap-4">
      <h1 class="text-2xl font-semibold">Videos</h1>
      <div class="grid gap-6 lg:grid-cols-5 md:grid-cols-3">
        {#each searchResult.value.videos as video (video)}
          <VideoCard {video} />
        {/each}
      </div>
    </section>
  {:else}
    <section class="flex flex-col gap-4">
      <h1 class="text-2xl font-semibold">Channels</h1>
      <div class="grid gap-6 lg:grid-cols-5 md:grid-cols-3">
        {#each channels as channel (channel)}
          <ChannelCard {channel} />
        {/each}
      </div>
    </section>
  {/if}
</div>
