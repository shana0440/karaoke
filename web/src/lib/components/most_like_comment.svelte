<script lang="ts">
  import { fetchMostLikeComment } from "$lib/api/api";
  import type { Comment } from "$lib/domains/comment";
  import { useApi } from "$lib/hooks/use_api";
  import { isSome, none, type Option } from "fp-ts/Option";
  import { onMount } from "svelte";

  export let videoId: string;

  let comment: Option<Comment> = none;

  const apiClient = useApi();

  const pasteWithoutStyle = (e: ClipboardEvent) => {
    e.preventDefault();
    var text = e.clipboardData?.getData("text/plain");
    const el = e.currentTarget as HTMLDivElement;
    el.innerText = text ?? "";
  };

  onMount(() => {
    fetchMostLikeComment(apiClient, { videoId }).then((mostLikeComment) => {
      comment = mostLikeComment;
    });
  });
</script>

{#if isSome(comment)}
  <div
    class="[&>*]:outline-none outline-none text-sm p-2"
    contenteditable="true"
    on:paste={pasteWithoutStyle}
  >
    {@html comment.value.textDisplay}
  </div>
{:else}
  <div>No Comment Yet</div>
{/if}
