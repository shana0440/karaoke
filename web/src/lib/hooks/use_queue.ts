import type { Clip } from "$lib/domains/clip";
import { writable } from "svelte/store"

const globalQueue = writable<Clip[]>([]);

export function useQueue() {
    const add = (clip: Clip) => {
        globalQueue.update(prev => [...prev, clip])
    }
    const remove = (clip: Clip) => {
        globalQueue.update(prev => prev.filter(it => it.id !== clip.id))
    }

    return {
        queue: { subscribe: globalQueue.subscribe },
        add,
        remove,
    }
}