import type { Clip } from "$lib/domains/clip";
import { get, writable } from "svelte/store";
import { some, type Option, isSome, none } from "fp-ts/Option";
import { useQueue } from "./use_queue";
import { last } from "fp-ts/Array";
import { pipe } from "fp-ts/function";
import { match } from "fp-ts/Option";

const playingClip = writable<Option<Clip>>(none);
const isPause = writable<boolean>(false);
const isRepeatOnce = writable<boolean>(false);
const currentTime = writable<number[]>([0]);

type OnPlayListener = () => void;
type OnPauseListener = () => void;
type OnSyncToProgressBarListener = (time: number) => void;

let onPlayListeners: OnPlayListener[] = [];
let onPauseListeners: OnPauseListener[] = [];
let onSyncToProgressBarListeners: OnSyncToProgressBarListener[] = [];

let previousClips: Clip[] = [];

export function usePlayer() {
  const { queue, remove, add } = useQueue();

  const play = (
    clip: Clip | undefined = undefined,
    saveToPreviousQueue: boolean = true
  ) => {
    if (clip) {
      if (saveToPreviousQueue) {
        pipe(
          get(playingClip),
          match(
            () => {},
            (clip) => {
              previousClips.push(clip);
            }
          )
        );
      }
      syncToProgressBar(clip.start_at);
      currentTime.set([clip.start_at]);
      playingClip.set(some(clip));
      isPause.set(false);
    } else {
      isPause.set(false);
    }
    onPlayListeners.forEach((it) => it());
  };

  const playNext = () => {
    if (get(isRepeatOnce)) {
      const nextClip = get(playingClip);
      pipe(
        nextClip,
        match(
          () => {},
          (clip) => {
            play(clip);
          }
        )
      );
    } else if (get(queue).length > 0) {
      const nextClip = get(queue)[0];
      play(nextClip);
      remove(nextClip);
    } else {
      pause();
    }
  };

  const playPrev = () => {
    pipe(
      get(playingClip),
      match(
        () => {},
        (clip) => {
          add(clip);
        }
      )
    );
    pipe(
      last(previousClips),
      match(
        () => {},
        (clip) => {
          play(clip, false);
          previousClips = previousClips.filter((it) => it !== clip);
        }
      )
    );
  };

  const pause = () => {
    isPause.set(true);
    onPauseListeners.forEach((it) => it());
  };

  const tick = (time: number) => {
    currentTime.set([time]);
    const clip = get(playingClip);
    if (isSome(clip) && clip.value.end_at < time) {
      playNext();
    }
  };

  const syncToProgressBar = (time: number) => {
    onSyncToProgressBarListeners.forEach((it) => it(time));
  };

  const onPlay = (listener: OnPlayListener) => {
    onPlayListeners.push(listener);
    return () => {
      onPlayListeners.filter((it) => it !== listener);
    };
  };

  const onPause = (listener: OnPauseListener) => {
    onPauseListeners.push(listener);
    return () => {
      onPauseListeners.filter((it) => it !== listener);
    };
  };

  const onSyncToProgressBar = (listener: OnSyncToProgressBarListener) => {
    onSyncToProgressBarListeners.push(listener);
    return () => {
      onSyncToProgressBarListeners.filter((it) => it !== listener);
    };
  };

  const isPlaying = (playingClip: Option<Clip>, clip: Clip) => {
    return pipe(
      playingClip,
      match(
        () => false,
        (playingClip) => playingClip.id === clip.id
      )
    );
  };

  return {
    playingClip,
    currentTime,
    isPause,
    isRepeatOnce,
    playNext,
    playPrev,
    play,
    pause,
    tick,
    syncToProgressBar,
    onPlay,
    onPause,
    onSyncToProgressBar,
    isPlaying,
  };
}
