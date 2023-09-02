<script lang="ts">
  import { formatTime } from "$lib/time/time";

  export let value: number;
</script>

{formatTime(value)}
