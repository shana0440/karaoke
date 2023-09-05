<script lang="ts">
  import { page } from "$app/stores";
  import { fetchChannel } from "$lib/api/api";
  import { sizeBanner, type ChannelWithBanner } from "$lib/domains/channel";
  import { useApi } from "$lib/hooks/use_api";
  import { some, none, type Option, isSome } from "fp-ts/Option";
  import { onMount } from "svelte";

  const id = $page.params.channel_id ?? "";

  let channel: Option<ChannelWithBanner> = none;

  const apiClient = useApi();
  onMount(() => {
    fetchChannel(apiClient, { channelId: id }).then((resp) => {
      channel = some(resp);
    });
  });
</script>

{#if isSome(channel)}
  <div
    class="flex flex-col h-full overflow-hidden rounded-lg bg-dark-slate-grey"
  >
    <div class="relative">
      <img
        src={sizeBanner(channel.value.banner_url, 1707)}
        alt={channel.value.title}
        class="object-cover w-full h-72"
      />
    </div>
    <div class="relative z-10 flex-1 p-2">
      <section class="flex items-end gap-6 px-4 -mt-20">
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
      <section class="p-4">
        <ul>
          <li>song1</li>
        </ul>
      </section>
    </div>
  </div>
{/if}
