<script lang="ts">
  import { page } from "$app/stores";
  import { fetchChannel, fetchChannelClips } from "$lib/api/api";
  import ClipItem from "$lib/components/clip_item.svelte";
  import TimeFormat from "$lib/components/time_format.svelte";
  import { sizeBanner, type ChannelWithBanner } from "$lib/domains/channel";
  import type { Clip } from "$lib/domains/clip";
  import { useApi } from "$lib/hooks/use_api";
  import { some, none, type Option, isSome } from "fp-ts/Option";
  import { onMount } from "svelte";

  const id = $page.params.channel_id ?? "";

  let channel: Option<ChannelWithBanner> = none;
  let clips: Clip[] = [];

  const apiClient = useApi();
  onMount(() => {
    fetchChannel(apiClient, { channelId: id }).then((resp) => {
      channel = some(resp);
    });
    fetchChannelClips(apiClient, { channelId: id }).then((resp) => {
      clips = resp.data;
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
        <div class="flex flex-col gap-2">
          <a
            href="https://www.youtube.com/{channel.value.custom_url}"
            target="_blank"
            class="flex items-center gap-2 text-2xl text-alice-blue hover:underline underline-offset-4"
          >
            {channel.value.title}
          </a>
          <p class="text-light-grey">{channel.value.custom_url}</p>
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
        </ul>
      </section>
    </div>
  </div>
{/if}
