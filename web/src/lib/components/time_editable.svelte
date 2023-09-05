<script lang="ts">
  import { parse, isValid, startOfDay, differenceInSeconds } from "date-fns";
  import TimeFormat from "./time_format.svelte";
  import { formatTime } from "$lib/time/time";

  export let time: number;

  const changeTime = (e: KeyboardEvent) => {
    if (e.key == "ArrowUp") {
      time++;
    }
    if (e.key === "ArrowDown") {
      time--;
    }
    if (e.key === "Enter") {
      e.preventDefault();
      (e.target as HTMLSpanElement).blur();
    }
  };

  const editTime = (e: Event) => {
    const target = e.currentTarget as HTMLSpanElement;
    const reference = startOfDay(new Date());
    const newTime = parse(target.innerText, "HH:mm:ss", reference);
    if (isValid(newTime)) {
      time = differenceInSeconds(newTime, reference);
    } else {
      target.innerText = formatTime(time);
    }
  };
</script>

<span
  role="textbox"
  class="outline-none text-light-grey focus:text-alice-blue focus:underline underline-offset-2 caret-dodger-blue"
  tabindex="-1"
  contenteditable="true"
  on:keydown={changeTime}
  on:blur={editTime}
>
  <TimeFormat value={time} />
</span>
