<script lang="ts">
  import { fetchChannels } from "$lib/api/api";
  import ChannelCard from "$lib/components/channel_card.svelte";
  import type { Channel } from "$lib/domains/channel";
  import { useApi } from "$lib/hooks/use_api";
  import { IconSearch } from "@tabler/icons-svelte";
  import { onMount } from "svelte";

  const apiClient = useApi();

  let channels: Channel[] = [];

  onMount(() => {
    fetchChannels(apiClient, {}).then((resp) => {
      channels = resp.data;
    });
  });
</script>

<div class="flex flex-col gap-4 p-2">
  <div class="input w-[448px]">
    <IconSearch />
    <input
      placeholder="What do you want to listen to?"
      class="text-alice-blue placeholder:text-light-grey"
    />
  </div>
  <section class="flex flex-col gap-4">
    <h1 class="text-2xl font-semibold">Channel</h1>
    <div class="grid gap-6 lg:grid-cols-5 md:grid-cols-3">
      {#each channels as channel (channel)}
        <ChannelCard {channel} />
      {/each}
    </div>
  </section>
</div>
