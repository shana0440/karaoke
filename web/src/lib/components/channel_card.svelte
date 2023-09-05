<script lang="ts">
  import type { Channel } from "$lib/domains/channel";

  export let channel: Channel;
</script>

<a
  href={`/channels/${channel.id}`}
  class="flex flex-col gap-2 p-4 transition-colors rounded-md group bg-dark-slate-grey hover:bg-charcoal"
>
  <div class="relative overflow-hidden">
    <img
      class="w-full rounded-md aspect-auto"
      src={channel.thumbnail_url}
      alt={channel.title}
    />
  </div>
  <p class="font-semibold text-alice-blue">{channel.title}</p>
  <p class="text-sm text-light-grey line-clamp-2">{channel.custom_url}</p>
</a>
