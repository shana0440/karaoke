import type { Clip } from "$lib/domains/clip";
import { get, writable } from "svelte/store"
import { some, type Option, isSome, none } from "fp-ts/Option"
import { useQueue } from "./use_queue";

const playingClip = writable<Option<Clip>>(none);
const isPause = writable<boolean>(false);
const currentTime = writable<number[]>([0]);

type OnPlayListener = () => void;
type OnPauseListener = () => void;
type OnSyncToProgressBarListener = (time: number) => void;

let onPlayListeners: OnPlayListener[] = [];
let onPauseListeners: OnPauseListener[] = [];
let onSyncToProgressBarListeners: OnSyncToProgressBarListener[] = [];

export function usePlayer() {
  const { queue, remove } = useQueue();

  const play = (clip?: Clip) => {
    if (clip) {
      syncToProgressBar(clip.start_at);
      currentTime.set([clip.start_at]);
      playingClip.set(some(clip));
      isPause.set(false);
      onPlayListeners.forEach(it => it())
    } else {
      isPause.set(false);
    }
  }

  const pause = () => {
    isPause.set(true);
    onPauseListeners.forEach(it => it())
  }

  const tick = (time: number) => {
    currentTime.set([time]);
    const clip = get(playingClip);
    if (isSome(clip) && clip.value.end_at < time) {
      pause();
      if (get(queue).length > 0) {
        const nextClip = get(queue)[0];
        play(nextClip);
        remove(nextClip);
      }
    }
  }

  const syncToProgressBar = (time: number) => {
    onSyncToProgressBarListeners.forEach(it => it(time))
  }

  const onPlay = (listener: OnPlayListener) => {
    onPlayListeners.push(listener);
    return () => {
      onPlayListeners.filter(it => it !== listener);
    }
  }

  const onPause = (listener: OnPauseListener) => {
    onPauseListeners.push(listener);
    return () => {
      onPauseListeners.filter(it => it !== listener);
    }
  }

  const onSyncToProgressBar = (listener: OnSyncToProgressBarListener) => {
    onSyncToProgressBarListeners.push(listener);
    return () => {
      onSyncToProgressBarListeners.filter(it => it !== listener);
    }
  }

  return {
    playingClip,
    currentTime,
    isPause,
    play,
    pause,
    tick,
    syncToProgressBar,
    onPlay,
    onPause,
    onSyncToProgressBar,
  }
}