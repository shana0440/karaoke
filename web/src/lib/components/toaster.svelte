<script lang="ts" context="module">
  export type ToastData = {
    message: string;
    intent: "success" | "failed";
  };

  const {
    elements: { content, title, description, close },
    helpers,
    states: { toasts },
    actions: { portal },
  } = createToaster<ToastData>();

  export const addToast = helpers.addToast;
</script>

<script lang="ts">
  import { createToaster, melt } from "@melt-ui/svelte";
  import { flip } from "svelte/animate";
  import { fly } from "svelte/transition";
  import { IconX } from "@tabler/icons-svelte";
</script>

<div
  class="fixed bottom-0 right-0 z-50 flex flex-col items-end gap-2 m-4"
  use:portal
>
  {#each $toasts as { id, data } (id)}
    <div
      use:melt={$content(id)}
      animate:flip={{ duration: 500 }}
      in:fly={{ duration: 150, x: "100%" }}
      out:fly={{ duration: 150, x: "100%" }}
      class="text-white border rounded-lg shadow-md bg-gunmetal border-outer-space"
    >
      <div
        class="relative flex w-[24rem] max-w-[calc(100vw-2rem)] items-center justify-between gap-4 p-5"
      >
        <div class="flex-1">
          <h3
            use:melt={$title(id)}
            class="flex items-center gap-4 font-semibold"
          >
            <span
              class="rounded-full w-2 h-2 {data.intent === 'success'
                ? 'bg-green-500'
                : data.intent === 'failed'
                ? 'bg-terracotta-red'
                : ''}"
            />
            {data.message}
          </h3>
        </div>
        <button
          use:melt={$close(id)}
          class="p-2 rounded-full text-light-grey hover:bg-charcoal"
        >
          <IconX />
        </button>
      </div>
    </div>
  {/each}
</div>
