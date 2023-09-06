<script lang="ts">
  import { page } from "$app/stores";
  import { fetchChannelClips, fetchVideo, fetchVideoClips } from "$lib/api/api";
  import ClipItem from "$lib/components/clip_item.svelte";
  import InfiniteScroll from "$lib/components/infinite_scroll.svelte";
  import { addToast } from "$lib/components/toaster.svelte";
  import type { Clip } from "$lib/domains/clip";
  import { useApi } from "$lib/hooks/use_api";
  import { usePlayer } from "$lib/hooks/use_player";
  import { useQueue } from "$lib/hooks/use_queue";
  import { IconPlayerPlayFilled, IconPlaylistAdd } from "@tabler/icons-svelte";
  import { some, none, type Option, isSome } from "fp-ts/Option";
  import { dropLeft } from "fp-ts/lib/Array";
  import { onMount } from "svelte";
  import { hasMore as hasMorePage } from "$lib/domains/pagination";
  import Spinner from "$lib/components/spinner.svelte";
  import type { Video } from "$lib/domains/video";
  import Tooltip from "$lib/components/tooltip.svelte";

  const id = $page.params.video_id ?? "";
  const { add } = useQueue();
  const { play } = usePlayer();

  let video: Option<Video> = none;
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
    fetchVideo(apiClient, { videoId: id }).then((resp) => {
      video = some(resp);
    });
    fetchVideoClips(apiClient, { videoId: id, offset }).then((resp) => {
      clips = resp.data;
      hasMore = hasMorePage(resp);
      offset = resp.offset + resp.limit;
    });
  });
</script>

{#if isSome(video)}
  <div class="flex flex-col bg-dark-slate-grey">
    <div class="sticky inset-x-0 top-0">
      <img
        src={video.value.video_thumbnail}
        alt={video.value.title}
        class="object-cover w-full rounded-t-lg h-72"
      />
    </div>
    <div class="relative z-10 flex-1 p-2 px-10 bg-dark-slate-grey">
      <section class="flex items-end gap-6 -mt-20">
        <img
          src={video.value.channel.thumbnail_url}
          alt={video.value.title}
          class="w-40 shadow-xl shadow-gunmetal aspect-auto rounded-2xl"
        />
        <div class="flex-1 w-0">
          <div class="flex flex-col gap-2">
            <Tooltip
              class="w-full text-2xl truncate text-alice-blue hover:underline underline-offset-4"
              description={video.value.title}
            >
              <a
                href="https://www.youtube.com/watch?v={video.value.resource_id}"
                target="_blank"
              >
                {video.value.title}
              </a>
            </Tooltip>
            <p class="text-light-grey">{video.value.channel.title}</p>
          </div>
        </div>
        <div class="flex gap-4 pb-4">
          <button class="items-center px-6 py-2 btn" on:click={playAllClips}>
            <IconPlayerPlayFilled class="w-4 h-4 text-alice-blue" />
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
