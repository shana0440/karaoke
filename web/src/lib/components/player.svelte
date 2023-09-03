<script lang="ts">
  import {
    IconPlayerPlay,
    IconPlayerSkipBack,
    IconPlayerSkipForward,
    IconPlayerPause,
    IconPhotoSensor,
    IconShare,
  } from "@tabler/icons-svelte";
  import { Slider } from "radix-svelte";

  let rootValue: number[];
  let rootMin: number;
  let rootMax: number = 100;

  rootValue = [20];
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
    <Slider.Root
      class="relative flex h-5
		w-full touch-none select-none items-center 
		data-[orientation=vertical]:h-[200px] 
		data-[orientation=vertical]:w-5 
		data-[orientation=vertical]:flex-col
		"
      bind:value={rootValue}
      min={rootMin}
      max={rootMax}
      aria-label="Volume"
    >
      <Slider.Track class="relative h-1 rounded-full grow bg-charcoal">
        <Slider.Range class="absolute h-full rounded-full bg-alice-blue" />
      </Slider.Track>
      <Slider.Thumb
        class="block h-5 w-5 rounded-full bg-alice-blue cursor-pointer focus:shadow-[0_0_0_5px] focus:shadow-cod-gray/50 focus:outline-none"
      />
    </Slider.Root>
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
    <button class="group">
      <IconPhotoSensor class="icon-btn-stroke" />
    </button>
  </div>
</div>
