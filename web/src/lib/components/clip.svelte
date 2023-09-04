<script lang="ts">
  import type { Clip } from "$lib/domains/clip";
  import { usePlayer } from "$lib/hooks/use_player";
  import { IconPlayerPlay } from "@tabler/icons-svelte";

  const { play } = usePlayer();

  export let clip: Clip;
</script>

<div
  role="button"
  tabindex="-1"
  on:click={() => play(clip)}
  on:keydown={() => {}}
  class="flex flex-col gap-2 p-4 transition-colors rounded-md group bg-dark-slate-grey hover:bg-charcoal"
>
  <div class="relative overflow-hidden">
    <img
      class="w-full rounded-md aspect-auto"
      src={clip.video.video_thumbnail}
      alt={clip.video.title}
    />
    <div
      class="absolute inset-0 flex items-center justify-center transition-all opacity-0 translate-y-1/3 group-hover:translate-y-0 group-hover:opacity-100"
    >
      <div class="p-3 rounded-full bg-cod-gray/80">
        <IconPlayerPlay class="w-6 h-6 fill-alice-blue stroke-alice-blue" />
      </div>
    </div>
  </div>
  <p class="font-semibold text-alice-blue">{clip.name}</p>
  <p class="text-sm text-light-grey line-clamp-2">{clip.video.channel.title}</p>
</div>
