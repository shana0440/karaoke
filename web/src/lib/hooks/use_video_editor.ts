import type { VideoEditorContext } from "$lib/components/video_editor.svelte";
import { getContext } from "svelte";

export function useVideoEditor() {
  return getContext<VideoEditorContext>("video-editor");
}
