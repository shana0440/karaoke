<script lang="ts">
  import { page } from "$app/stores";
  import {
    IconHome,
    IconSearch,
    IconLayoutGridAdd,
  } from "@tabler/icons-svelte";
  import { getContext } from "svelte";
  import type { FloatingYoutubeContext } from "./floating_youtube.svelte";

  export let isFullScreenPlayerOpen: boolean;

  const { move } = getContext<FloatingYoutubeContext>("floating-yt");
  let ytContainer: HTMLDivElement;

  $: {
    if (!isFullScreenPlayerOpen && ytContainer) {
      move(ytContainer.getBoundingClientRect());
    }
  }
</script>

<div class="flex flex-col min-h-full rounded-lg w-72 bg-dark-slate-grey">
  <ul class="flex flex-col flex-1 gap-2 p-2">
    <li>
      <a class="nav-link" class:active={$page.url.pathname === "/"} href="/">
        <IconHome />Home
      </a>
    </li>
    <li>
      <a
        class="nav-link"
        class:active={$page.url.pathname === "/search"}
        href="/search"
      >
        <IconSearch />Search
      </a>
    </li>
    <li>
      <a
        class="nav-link"
        class:active={$page.url.pathname.startsWith("/editor")}
        href="/editor"
      >
        <IconLayoutGridAdd />Clip
      </a>
    </li>
  </ul>
  <div class="aspect-video" bind:this={ytContainer} />
</div>
