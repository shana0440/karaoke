<script lang="ts">
  import { IconPlayerPlay } from "@tabler/icons-svelte";
</script>

<div
  role="button"
  class="flex flex-col gap-2 p-4 transition-colors rounded-md group bg-dark-slate-grey hover:bg-charcoal"
>
  <div class="relative overflow-hidden">
    <img
      class="w-full rounded-md aspect-auto"
      src="https://i.ytimg.com/vi/u6ftrRfR5Nw/default.jpg"
      alt="【#歌枠 / karaoke 】ジブリ 縛り 歌枠　#初見大歓迎 【 #Vtuber 】"
    />
    <div
      class="absolute inset-0 flex items-center justify-center transition-all opacity-0 translate-y-1/3 group-hover:translate-y-0 group-hover:opacity-100"
    >
      <div class="p-3 rounded-full bg-cod-gray/80">
        <IconPlayerPlay class="w-6 h-6 fill-alice-blue stroke-alice-blue" />
      </div>
    </div>
  </div>
  <p class="font-semibold text-alice-blue">風になる</p>
  <p class="text-sm text-light-grey line-clamp-2">茶柱ノキ / Chabashira Noki</p>
</div>
