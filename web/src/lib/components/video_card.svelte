<script lang="ts">
  import type { Video } from "$lib/domains/video";

  export let video: Video;
</script>

<a
  href={`/videos/${video.id}`}
  class="flex flex-col gap-2 p-4 transition-colors rounded-md group bg-dark-slate-grey hover:bg-charcoal"
>
  <div class="relative overflow-hidden">
    <img
      class="w-full rounded-md aspect-auto"
      src={video.video_thumbnail}
      alt={video.title}
    />
  </div>
  <p class="font-semibold text-alice-blue line-clamp-2">{video.title}</p>
  <p class="text-sm text-light-grey line-clamp-2">{video.channel.title}</p>
</a>
