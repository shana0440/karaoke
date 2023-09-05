<script lang="ts">
  import { page } from "$app/stores";
  import { fetchChannel, fetchChannelClips } from "$lib/api/api";
  import ClipItem from "$lib/components/clip_item.svelte";
  import InfiniteScroll from "$lib/components/infinite_scroll.svelte";
  import { addToast } from "$lib/components/toaster.svelte";
  import { sizeBanner, type ChannelWithBanner } from "$lib/domains/channel";
  import type { Clip } from "$lib/domains/clip";
  import { useApi } from "$lib/hooks/use_api";
  import { usePlayer } from "$lib/hooks/use_player";
  import { useQueue } from "$lib/hooks/use_queue";
  import { IconPlayerPlay, IconPlaylistAdd } from "@tabler/icons-svelte";
  import { some, none, type Option, isSome } from "fp-ts/Option";
  import { dropLeft } from "fp-ts/lib/Array";
  import { onMount } from "svelte";
  import { hasMore as hasMorePage } from "$lib/domains/pagination";
  import Spinner from "$lib/components/spinner.svelte";

  const id = $page.params.channel_id ?? "";
  const { add } = useQueue();
  const { play } = usePlayer();

  let channel: Option<ChannelWithBanner> = none;
  let clips: Clip[] = [];
  let hasMore = true;
  let offset = 0;
  let loading = false;

  const playAllClips = () => {
    play(clips[0]);
    dropLeft(1)(clips).forEach(add);
  };

  const addAllClipsToQueue = () => {
    clips.forEach(add);
    addToast({
      data: {
        message: `Added to Queue`,
        intent: "success",
      },
    });
  };

  const apiClient = useApi();
  const loadMoreClips = () => {
    if (loading) {
      return;
    }
    loading = true;
    fetchChannelClips(apiClient, { channelId: id, offset })
      .then((resp) => {
        clips = [...clips, ...resp.data];
        hasMore = hasMorePage(resp);
        offset = resp.offset + resp.limit;
      })
      .finally(() => {
        loading = false;
      });
  };

  onMount(() => {
    fetchChannel(apiClient, { channelId: id }).then((resp) => {
      channel = some(resp);
    });
    fetchChannelClips(apiClient, { channelId: id, offset }).then((resp) => {
      clips = resp.data;
      hasMore = hasMorePage(resp);
      offset = resp.offset + resp.limit;
    });
  });
</script>

{#if isSome(channel)}
  <div class="flex flex-col bg-dark-slate-grey">
    <div class="sticky inset-x-0 top-0">
      <img
        src={sizeBanner(channel.value.banner_url, 1707)}
        alt={channel.value.title}
        class="object-cover w-full rounded-t-lg h-72"
      />
    </div>
    <div class="relative z-10 flex-1 p-2 px-10 bg-dark-slate-grey">
      <section class="flex items-end gap-6 -mt-20">
        <img
          src={channel.value.thumbnail_url}
          alt={channel.value.title}
          class="w-40 aspect-auto rounded-2xl"
        />
        <div class="flex-1">
          <div class="flex flex-col gap-2 w-max">
            <a
              href="https://www.youtube.com/{channel.value.custom_url}"
              target="_blank"
              class="flex items-center gap-2 text-2xl text-alice-blue hover:underline underline-offset-4"
            >
              {channel.value.title}
            </a>
            <p class="text-light-grey">{channel.value.custom_url}</p>
          </div>
        </div>
        <div class="flex gap-4 pb-4">
          <button class="items-center px-6 py-2 btn" on:click={playAllClips}>
            <IconPlayerPlay class="w-4 h-4 fill-alice-blue stroke-alice-blue" />
            Play
          </button>
          <button
            class="items-center px-6 py-2 btn"
            on:click={addAllClipsToQueue}
          >
            <IconPlaylistAdd />
            Add to Queue
          </button>
        </div>
      </section>
      <section class="py-4">
        <ul class="flex flex-col gap-2">
          {#each clips as clip, i (clip)}
            <li>
              <ClipItem {clip} index={i + 1} />
            </li>
          {:else}
            <li>Channel is Empty</li>
          {/each}
          <InfiniteScroll {hasMore} loadMore={loadMoreClips}>
            <Spinner />
          </InfiniteScroll>
        </ul>
      </section>
    </div>
  </div>
{/if}
