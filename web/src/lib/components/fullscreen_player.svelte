<script lang="ts">
  import {
    IconPlayerSkipBack,
    IconPlayerSkipForward,
    IconPlayerPause,
    IconPlayerPlay,
    IconShare,
    IconX,
    IconDots,
  } from "@tabler/icons-svelte";
  import { Slider } from "radix-svelte";

  export let isFullScreenPlayerOpen: boolean;

  let rootValue: number[];
  let rootMin: number;
  let rootMax: number = 100;

  rootValue = [20];
</script>

<div
  class={`fixed inset-0 flex flex-col backdrop-blur-2xl transition-all opacity-0 translate-y-1/3 z-10 p-2 ${
    isFullScreenPlayerOpen ? "translate-y-0 opacity-100" : "pointer-events-none"
  }`}
>
  <div class="flex items-center justify-center flex-1">
    <div class="flex justify-center gap-10 h-[600px]">
      <div
        class="flex flex-col gap-10 px-6 py-10 rounded-3xl bg-dark-slate-grey/30 w-[450px]"
      >
        <img
          class="shadow-2xl rounded-3xl w-96 aspect-auto"
          src="https://i.ytimg.com/vi/u6ftrRfR5Nw/default.jpg"
          alt="【#歌枠 / karaoke 】ジブリ 縛り 歌枠　#初見大歓迎 【 #Vtuber 】"
        />
        <div class="flex flex-col gap-2">
          <p class="font-semibold text-alice-blue">風になる</p>
          <p class="text-sm text-light-Vgrey line-clamp-1">
            茶柱ノキ / Chabashira Noki
          </p>
          <p class="text-sm text-light-Vgrey line-clamp-1">
            【#歌枠 / karaoke 】ジブリ 縛り 歌枠　#初見大歓迎 【 #Vtuber 】
          </p>
        </div>

        <div class="flex items-center justify-center gap-2">
          <button class="p-4 rounded-full group">
            <IconPlayerSkipBack class="icon-btn-fill icon-btn-stroke" />
          </button>
          <button type="button" class="p-4 rounded-full bg-cod-gray group">
            <IconPlayerPause class="icon-btn-fill icon-btn-stroke" />
          </button>
          <button class="p-4 rounded-full group">
            <IconPlayerSkipForward class="icon-btn-fill icon-btn-stroke" />
          </button>
        </div>
      </div>
      <div class="self-start w-[600px] flex flex-col gap-4">
        <h2 class="text-2xl font-semibold">Queue</h2>
        <div class="relative flex-1 overflow-auto">
          <ul class="flex flex-col gap-2">
            {#each Array(10) as _, i}
              <li>
                <div
                  role="button"
                  class="flex items-center gap-4 px-4 py-2 transition-colors rounded-lg group hover:bg-cod-gray"
                >
                  <p class="relative flex items-center justify-center">
                    <span class="transition-opacity group-hover:opacity-0">
                      {i + 1}
                    </span>
                    <IconPlayerPlay
                      class="absolute w-5 h-5 transition-opacity opacity-0 group-hover:opacity-100 fill-alice-blue stroke-alice-blue"
                    />
                  </p>
                  <p class="flex-1 w-0 truncate">いのちの名前</p>
                  <time>04:50</time>
                  <button
                    class="p-1 transition-colors rounded-md hover:bg-charcoal"
                  >
                    <IconDots class="stroke-light-grey" />
                  </button>
                </div>
              </li>
            {/each}
          </ul>
          <div
            class="pointer-events-none absolute -inset-x-2.5 -bottom-2.5 h-1/3 bg-gradient-to-t from-jet to-jet/0"
          />
        </div>
      </div>
    </div>
  </div>
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
      <button
        class="group"
        on:click={() => (isFullScreenPlayerOpen = !isFullScreenPlayerOpen)}
      >
        <IconX class="icon-btn-stroke" />
      </button>
    </div>
  </div>
</div>
