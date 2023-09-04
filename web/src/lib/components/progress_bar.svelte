<script lang="ts">
  import { createSlider, melt } from "@melt-ui/svelte";
  import { usePlayer } from "$lib/hooks/use_player";
  import { isSome } from "fp-ts/lib/Option";

  const { currentTime, playingClip, syncToProgressBar } = usePlayer();
  const {
    elements: { root, range, thumb },
    options: { min, max },
  } = createSlider({
    defaultValue: [0],
    value: currentTime,
    min: 0,
    max: 0,
    step: 1,
    onValueChange({ curr, next }) {
      syncToProgressBar(next[0]);
      return next;
    },
  });

  $: {
    if (isSome($playingClip)) {
      min.set($playingClip.value.start_at);
      max.set($playingClip.value.end_at);
    }
  }
</script>

<span use:melt={$root} class="relative flex items-center flex-1 group">
  <span
    class="block w-full h-1 transition rounded-full cursor-pointer bg-gunmetal group-hover:scale-y-[200%]"
  >
    <span use:melt={$range} class="h-1 rounded-full bg-alice-blue" />
  </span>
  <span
    use:melt={$thumb()}
    class="block w-5 h-5 rounded-full outline-none cursor-pointer bg-alice-blue focus:ring-4 focus:ring-cod-gray/40"
  />
</span>
