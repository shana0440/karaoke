<script lang="ts">
  import {
    IconCloudUp,
    IconFileImport,
    IconPackageImport,
  } from "@tabler/icons-svelte";
  import ImportMvFromChannelDialog from "$lib/components/import_mv_from_channel_dialog.svelte";
  import ImportMvFromVideoDialog from "$lib/components/import_mv_from_video_dialog.svelte";
  import type { Mv } from "$lib/domains/mv";
  import MvCard from "$lib/components/mv_card.svelte";
  import { uniqBy } from "lodash";
  import { useApi } from "$lib/hooks/use_api";
  import { saveMvs as _saveMvs } from "$lib/api/api";
  import {
    hideLoadingOverlay,
    showLoadingOverlay,
  } from "$lib/components/loading_overlay.svelte";
  import { addToast } from "$lib/components/toaster.svelte";

  let mvs: Mv[] = [];

  const importMVs = (newMVs: Mv[]) => {
    mvs = uniqBy([...mvs, ...newMVs], (it) => it.id);
  };
  const removeMv = (mv: Mv) => {
    mvs = mvs.filter((it) => it.id !== mv.id);
  };

  const apiClient = useApi();
  const saveMvs = () => {
    showLoadingOverlay();
    _saveMvs(apiClient, { videoIds: mvs.map((it) => it.id) })
      .then(() => {
        addToast({
          data: {
            intent: "success",
            message: `Saved ${mvs.length} MVs`,
          },
        });
        mvs = [];
      })
      .catch(() => {
        addToast({
          data: {
            intent: "failed",
            message: "Save MVs failed",
          },
        });
      })
      .finally(hideLoadingOverlay);
  };
</script>

<div class="flex flex-col gap-4 p-2">
  <h1 class="text-2xl font-semibold">Add MVs</h1>
  <div class="grid grid-cols-2 gap-4">
    <div class="flex gap-4">
      <ImportMvFromChannelDialog onImport={importMVs} class="px-4 py-2 btn">
        <IconPackageImport />
        Import from Channel URL
      </ImportMvFromChannelDialog>
      <ImportMvFromVideoDialog onImport={importMVs} class="px-4 py-2 btn">
        <IconFileImport />
        Import from Video URL
      </ImportMvFromVideoDialog>
    </div>
    <div class="flex justify-end gap-4">
      <button class="px-4 py-2 btn justify-self-end" on:click={saveMvs}>
        <IconCloudUp />
        Save
      </button>
    </div>
  </div>
  <div class="flex-1 min-h-0 overflow-auto">
    <ul class="grid gap-6 lg:grid-cols-5 md:grid-cols-3">
      {#each mvs as mv (mv.id)}
        <li>
          <MvCard {mv} onRemove={removeMv} />
        </li>
      {:else}
        <li class="col-span-5 py-40 text-center">
          <ImportMvFromChannelDialog
            onImport={importMVs}
            class="px-4 py-2 mx-auto btn"
          >
            <IconPackageImport />
            Start import MVs from Channel URL
          </ImportMvFromChannelDialog>
          <div
            class="flex items-center justify-center w-1/3 gap-6 mx-auto my-10"
          >
            <div class="h-[1px] w-full bg-light-grey" />
            <p>or</p>
            <div class="h-[1px] w-full bg-light-grey" />
          </div>
          <ImportMvFromVideoDialog
            onImport={importMVs}
            class="px-4 py-2 mx-auto btn"
          >
            <IconFileImport />
            Import from Video URL
          </ImportMvFromVideoDialog>
        </li>
      {/each}
    </ul>
  </div>
</div>
