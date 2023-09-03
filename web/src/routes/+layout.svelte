<script lang="ts">
  import { page } from "$app/stores";
  import {
    IconHome,
    IconSearch,
    IconLayoutGridAdd,
  } from "@tabler/icons-svelte";

  import "../app.css";
  import Player from "$lib/components/player.svelte";
</script>

<div class="flex flex-col h-screen gap-2 p-2">
  <div class="flex flex-1 gap-2">
    <div class="min-h-full w-72">
      <ul
        class="flex flex-col min-h-full gap-2 p-2 rounded-lg bg-dark-slate-grey"
      >
        <li>
          <a
            class="nav-link"
            class:active={$page.url.pathname === "/"}
            href="/"
          >
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
    </div>
    <div class="flex-1">
      <slot />
    </div>
  </div>
  <Player />
</div>
