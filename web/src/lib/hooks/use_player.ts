import type { Clip } from "$lib/domains/clip";
import { writable } from "svelte/store"
import { none, some, type Option, isSome, isNone } from "fp-ts/Option"

interface PlayerContext {
    clip: Clip,
    currentTime: number,
    isPause: boolean,
}

const globalPlayer = writable<Option<PlayerContext>>(none);

export function usePlayer() {
    const play = (clip: Clip) => {
        globalPlayer.set(some({
            clip,
            currentTime: 0,
            isPause: false,
        }))
    }

    const pause = () => {
        globalPlayer.update(prev => {
            if (isNone(prev)) {
                return prev;
            }
            return some({
                ...prev.value,
                isPause: true,
            })
        })
    }

    return {
        player: { subscribe: globalPlayer.subscribe },
        play,
        pause,
    }
}