<script lang="ts">
  import { fetchMVsFromChannelURL } from "$lib/api/api";
  import type { Mv } from "$lib/domains/mv";
  import { useApi } from "$lib/hooks/use_api";
  import { createDialog, melt } from "@melt-ui/svelte";
  import { IconLink } from "@tabler/icons-svelte";
  import { fly } from "svelte/transition";
  import { addToast } from "./toaster.svelte";
  import {
    hideLoadingOverlay,
    showLoadingOverlay,
  } from "./loading_overlay.svelte";

  const {
    elements: {
      close,
      trigger,
      overlay,
      title,
      content,
      description,
      portalled,
    },
    states: { open },
  } = createDialog({});

  export let onImport: (mvs: Mv[]) => void;

  let url: HTMLInputElement;

  const apiClient = useApi();
  const importMvsFromChannel = () => {
    showLoadingOverlay();
    fetchMVsFromChannelURL(apiClient, {
      channelUrl: url.value,
    })
      .then((mvs) => {
        onImport(mvs);
        open.set(false);
        addToast({
          data: {
            intent: "success",
            message: `Import ${mvs.length} MVs`,
          },
        });
      })
      .catch(() => {
        addToast({
          data: {
            intent: "failed",
            message: "Import Failed",
          },
        });
      })
      .finally(hideLoadingOverlay);
  };
</script>

<button use:melt={$trigger} class={$$restProps.class}>
  <slot />
</button>
<div use:melt={$portalled}>
  {#if $open}
    <div use:melt={$overlay} class="fixed inset-0 z-10 bg-transparent-black" />
    <div
      use:melt={$content}
      class="fixed left-[50%] top-[50%] z-10 max-h-[85vh] w-[90vw] max-w-[450px] translate-x-[-50%] translate-y-[-50%] rounded-xl bg-black-coral border border-transparent-red p-6 flex flex-col gap-6"
      transition:fly={{
        duration: 150,
        y: 8,
      }}
    >
      <h2 use:melt={$title} class="text-2xl">Import from Channel URL</h2>
      <p use:melt={$description} class="text-lg">Input youtube channel URL</p>
      <div class="input">
        <IconLink />
        <!-- svelte-ignore a11y-autofocus -->
        <input bind:this={url} autofocus />
      </div>
      <p class="text-sm text-light-grey">
        this will import any video in the channel that duration less than 20
        mins.
      </p>
      <div class="flex justify-end gap-6">
        <button class="" use:melt={$close}>Close</button>
        <button class="btn" on:click={importMvsFromChannel}>Import</button>
      </div>
    </div>
  {/if}
</div>
