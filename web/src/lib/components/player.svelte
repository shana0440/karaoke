<script lang="ts">
  import {
    IconPlayerPlay,
    IconPlayerSkipBack,
    IconPlayerSkipForward,
    IconPlayerPause,
    IconPhotoSensor,
    IconShare,
  } from "@tabler/icons-svelte";
  import { createSlider, melt } from "@melt-ui/svelte";
  const {
    elements: { root, range, thumb },
    states: { value },
  } = createSlider({
    defaultValue: [100],
    max: 500,
    step: 1,
    onValueChange({ curr, next }) {
      return next;
    },
  });

  export let isFullScreenPlayerOpen: boolean;
</script>

<div
  class="flex items-center w-full gap-10 px-4 py-2 rounded-lg bg-dark-slate-grey"
>
  <div class="flex w-64 gap-2">
    <img
      class="rounded h-14 aspect-auto"
      src="https://i.ytimg.com/vi/u6ftrRfR5Nw/default.jpg"
      alt="【#歌枠 / karaoke 】ジブリ 縛り 歌枠　#初見大歓迎 【 #Vtuber 】"
    />
    <div class="flex flex-col justify-around">
      <p class="font-semibold text-alice-blue">風になる</p>
      <p class="text-sm text-light-grey line-clamp-1">
        茶柱ノキ / Chabashira Noki
      </p>
    </div>
  </div>
  <div class="flex items-center justify-center gap-2">
    <button class="p-2 rounded-full group">
      <IconPlayerSkipBack class="icon-btn-fill icon-btn-stroke" />
    </button>
    <button type="button" class="p-2 rounded-full bg-cod-gray group">
      <IconPlayerPlay class="icon-btn-fill icon-btn-stroke" />
    </button>
    <button class="p-2 rounded-full group">
      <IconPlayerSkipForward class="icon-btn-fill icon-btn-stroke" />
    </button>
  </div>
  <div class="flex items-center flex-1 gap-2">
    <time class="text-light-grey">01:30</time>
    <span use:melt={$root} class="relative flex items-center flex-1">
      <span class="block w-full h-1 bg-gunmetal">
        <span use:melt={$range} class="h-1 bg-alice-blue" />
      </span>
      <span
        use:melt={$thumb()}
        class="block w-5 h-5 rounded-full outline-none bg-alice-blue focus:ring-4 focus:ring-cod-gray/40"
      />
    </span>
    <time class="text-light-grey">04:30</time>
  </div>
  <div class="flex items-center justify-end gap-4">
    <a
      href="https://youtube.com/watch?v=u6ftrRfR5Nw&t=300s"
      target="_blank"
      class="group"
    >
      <IconShare class="icon-btn-stroke" />
    </a>
    <button
      class="group"
      on:click={() => (isFullScreenPlayerOpen = !isFullScreenPlayerOpen)}
    >
      <IconPhotoSensor class="icon-btn-stroke" />
    </button>
  </div>
</div>
