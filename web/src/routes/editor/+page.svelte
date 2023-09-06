<script lang="ts">
  import { IconSearch } from "@tabler/icons-svelte";
  import { handleKey } from "$lib/doc/doc";
  import { goto } from "$app/navigation";

  let error: string;
</script>

<div class="flex items-center justify-center py-40">
  <div class="flex flex-col w-full max-w-4xl gap-5">
    <h1 class="text-5xl text-center">Welcome to Karaoke</h1>
    <p class="text-2xl text-center">
      Input a youtube url and start mark the singing section
    </p>
    <div class="max-w-4xl input">
      <IconSearch class="w-6 h-6" />
      <input
        on:keypress={handleKey(["Enter"], (e) => {
          try {
            const url = new URL(e.currentTarget.value);
            const id = url.searchParams.get("v");
            if (id) {
              goto(`/editor/${id}`);
            } else {
              error = "Cannot found video id";
            }
          } catch (e) {
            error = "Invalid Youtube URL";
          }
        })}
      />
    </div>
    <div class="flex items-center justify-center gap-6 px-20">
      <div class="h-[1px] w-full bg-light-grey" />
      <p>or</p>
      <div class="h-[1px] w-full bg-light-grey" />
    </div>
    <a
      href="/editor/mvs"
      class="px-10 py-2 mx-auto text-2xl text-center transition-colors border rounded-md border-light-grey hover:bg-cod-gray"
    >
      Add MVs
    </a>
    {#if error}
      <p class="text-center text-terracotta-red">{error}</p>
    {/if}
  </div>
</div>
