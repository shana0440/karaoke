import type { Clip } from "$lib/domains/clip";
import { get, writable } from "svelte/store"
import { some, type Option, isSome } from "fp-ts/Option"

const playingClip = writable<Option<Clip>>(some({
  id: 1,
  name: "風になる",
  start_at: 300,
  end_at: 505,
  created_at: "",
  updated_at: "",
  video: {
    id: 1,
    channel_id: 1,
    resource_id: "u6ftrRfR5Nw",
    title: "【#歌枠 / karaoke 】ジブリ 縛り 歌枠　#初見大歓迎 【 #Vtuber 】",
    video_thumbnail: "https://i.ytimg.com/vi/u6ftrRfR5Nw/default.jpg",
    channel: {
      id: 1,
      title: "茶柱ノキ / Chabashira Noki",
      resource_id: "UCZtjgZesCXH5RQHKrp-dCOQ",
      thumbnail_url: " https://yt3.ggpht.com/w7yrGSrUb9TaNcHWgfelFi1y6paMwU6X9ae9o22j9y_q0oEAhuqfM9DbZf4LXhhUtBs95DxRBA=s88-c-k-c0x00ffffff-no-rj",
      custom_url: "@chabashiranoki",
    }
  }
}));
const isPause = writable<boolean>(false);
const currentTime = writable<number[]>([0]);

type OnPlayListener = () => void;
type OnPauseListener = () => void;
type OnSyncToProgressBarListener = (time: number) => void;

let onPlayListeners: OnPlayListener[] = [];
let onPauseListeners: OnPauseListener[] = [];
let onSyncToProgressBarListeners: OnSyncToProgressBarListener[] = [];

export function usePlayer() {
  const play = (clip?: Clip) => {
    if (clip) {
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

  const updateTime = (time: number) => {
    currentTime.set([time]);
    const clip = get(playingClip);
    if (isSome(clip) && clip.value.end_at < time) {
      pause();
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
    updateTime,
    syncToProgressBar,
    onPlay,
    onPause,
    onSyncToProgressBar,
  }
}