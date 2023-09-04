<script lang="ts">
  import { IconSearch } from "@tabler/icons-svelte";
  import { handleKey } from "$lib/doc/doc";

  let error: string;
</script>

<div class="flex items-center justify-center py-40">
  <div class="flex flex-col w-full max-w-4xl gap-5">
    <h1 class="text-5xl text-center">Welcome to Karaoke</h1>
    <p class="text-2xl text-center">
      Input a youtube url and start mark the singing section
    </p>
    <div class="input">
      <IconSearch class="w-6 h-6" />
      <input
        on:keypress={handleKey(["Enter"], (e) => {
          try {
            const url = new URL(e.currentTarget.value);
            const id = url.searchParams.get("v");
            if (id) {
              window.location.href = `/editor/${id}`;
            } else {
              error = "Cannot found video id";
            }
          } catch (e) {
            error = "Invalid Youtube URL";
          }
        })}
      />
    </div>
    {#if error}
      <p class="text-center text-terracotta-red">{error}</p>
    {/if}
  </div>
</div>
