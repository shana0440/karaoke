import type { Clip } from "$lib/domains/clip";
import { writable } from "svelte/store";

const globalQueue = writable<Clip[]>([]);

export function useQueue() {
  const add = (clip: Clip) => {
    // NOTE: create a new reference of clip,
    // to avoid duplicate clip in queue, the remove won't remove all of them.
    globalQueue.update((prev) => [...prev, { ...clip }]);
  };
  const remove = (clip: Clip) => {
    globalQueue.update((prev) => prev.filter((it) => it !== clip));
  };

  return {
    queue: { subscribe: globalQueue.subscribe },
    add,
    remove,
  };
}
