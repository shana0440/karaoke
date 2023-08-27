<script lang="ts" context="module">
  export type ContextMenuContext = {
    open: (song: Song) => (e: MouseEvent) => void;
  };
</script>

<script lang="ts">
  import { onMount, setContext } from "svelte";
  import { makeEmptySong, type Song } from "../../domains/song";
  import { reScale, type Scale } from "../../scale/scale";

  export let scale: Scale;
  export let songs: Song[];

  let x: number;
  let y: number;
  let track: Song | undefined;

  setContext<ContextMenuContext>("contextmenu", {
    open: (song: Song) => (e: MouseEvent) => {
      e.stopPropagation();
      e.preventDefault();
      x = e.clientX;
      y = e.clientY;
      track = song;
    },
  });

  let container: HTMLDivElement;

  const addTrackToNext = () => {
    const index = songs.indexOf(track!);
    if (index !== -1) {
      songs.splice(index + 1, 0, makeEmptySong(scale.viewDomain, true));
      songs = [...songs];
    }
    track = undefined;
  };

  const addTrackToPrev = () => {
    const index = songs.indexOf(track!);
    if (index !== -1) {
      songs.splice(index, 0, makeEmptySong(scale.viewDomain, true));
      songs = [...songs];
    }
    track = undefined;
  };

  const expandTimeline = () => {
    scale = reScale(scale, track!.range);
    track = undefined;
  };

  const removeTrack = () => {
    songs = songs.filter((it) => it !== track);
    track = undefined;
  };

  const closeContextMenu = (e: MouseEvent) => {
    if (!e.target) {
      track = undefined;
      return;
    }
    if (!container.contains(e.target as Element)) {
      track = undefined;
      return;
    }
  };

  onMount(() => {
    window.addEventListener("click", closeContextMenu);
    return () => {
      window.removeEventListener("click", closeContextMenu);
    };
  });
</script>

<slot />
<div
  style={`left: ${x}px; top: ${y}px;`}
  bind:this={container}
  class="absolute"
>
  {#if track}
    <div class="py-1 rounded bg-bastille">
      <ul>
        <li>
          <button
            class="w-full px-2 py-1 text-left hover:bg-dodger-blue"
            on:click={expandTimeline}
          >
            Expand timeline
          </button>
        </li>
        <li>
          <button
            class="w-full px-2 py-1 text-left hover:bg-dodger-blue"
            on:click={addTrackToPrev}
          >
            Add track to prev
          </button>
        </li>
        <li>
          <button
            class="w-full px-2 py-1 text-left hover:bg-dodger-blue"
            on:click={addTrackToNext}
          >
            Add track to next
          </button>
        </li>
        <li>
          <button
            class="w-full px-2 py-1 text-left hover:bg-dodger-blue"
            on:click={removeTrack}
          >
            Remove track
          </button>
        </li>
      </ul>
    </div>
  {/if}
</div>
