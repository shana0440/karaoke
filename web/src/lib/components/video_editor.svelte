<script lang="ts" context="module">
  import { makeEmptyTrack, type Track } from "$lib/domains/track";
  import { reScale, type Scale } from "$lib/scale/scale";
  import { none, type Option, match, some } from "fp-ts/Option";
  import { pipe } from "fp-ts/lib/function";
  import { setContext } from "svelte";
  import { get, writable, type Writable } from "svelte/store";

  export type VideoEditorContext = {
    scale: Writable<Option<Scale>>;
    tracks: Writable<Track[]>;
    addTrackToNext: (track: Track) => void;
    addTrackToPrev: (track: Track) => void;
    expandTimeline: (track: Track) => void;
    removeTrack: (track: Track) => void;
    mergeTracks: (tracks: Track[]) => void;
    splitTracks: (track: Track[], time: number) => void;
    addTrack: () => void;
  };
</script>

<script lang="ts">
  let tracks = writable<Track[]>([]);
  let scale = writable<Option<Scale>>(none);

  const addTrackToNext = (track: Track) => {
    tracks.update((prev) => {
      return pipe(
        get(scale),
        match(
          () => prev,
          (scale) => {
            const index = prev.indexOf(track);
            if (index !== -1) {
              prev.splice(index + 1, 0, makeEmptyTrack(scale.viewDomain, true));
            }
            return prev;
          }
        )
      );
    });
  };

  const addTrackToPrev = (track: Track) => {
    tracks.update((prev) => {
      return pipe(
        get(scale),
        match(
          () => prev,
          (scale) => {
            const index = prev.indexOf(track);
            if (index !== -1) {
              prev.splice(index, 0, makeEmptyTrack(scale.viewDomain, true));
            }
            return prev;
          }
        )
      );
    });
  };

  const expandTimeline = (track: Track) => {
    scale.update((prev) => {
      return pipe(
        prev,
        match(
          () => prev,
          (scale) => some(reScale(scale, track.range))
        )
      );
    });
  };

  const removeTrack = (track: Track) => {
    tracks.update((prev) => prev.filter((it) => it !== track));
  };

  const mergeTracks = (mergableTracks: Track[]) => {
    if (mergableTracks.length < 2) {
      return;
    }
    const mergedTrack: Track = {
      name: mergableTracks
        .map((track) => track.name)
        .filter(Boolean)
        .join("-"),
      range: [
        Math.min(...mergableTracks.map((track) => track.range[0])),
        Math.max(...mergableTracks.map((track) => track.range[1])),
      ],
      selected: false,
    } satisfies Track;
    tracks.update((prev) => {
      const firstTrackIndex = prev.findIndex((it) =>
        mergableTracks.includes(it)
      );
      prev = prev.filter((it) => !mergableTracks.includes(it));
      prev.splice(firstTrackIndex, 0, mergedTrack);
      return prev;
    });
  };

  const splitTracks = (splitableTracks: Track[], time: number) => {
    tracks.update((prev) => {
      return prev.flatMap((track) => {
        if (!splitableTracks.includes(track)) {
          return track;
        }
        if (time <= track.range[0] || time >= track.range[1]) {
          return track;
        }
        const firstHalf: Track = {
          name: track.name ? track.name + "-1" : "",
          range: [track.range[0], time],
          selected: true,
        };
        const secondHalf: Track = {
          name: track.name ? track.name + "-2" : "",
          range: [time, track.range[1]],
          selected: true,
        };
        return [firstHalf, secondHalf];
      });
    });
  };

  const addTrack = () => {
    const range: [number, number] = pipe(
      get(scale),
      match(
        () => [0, 0],
        (scale) => scale.viewDomain
      )
    );
    tracks.update((prev) => [...prev, makeEmptyTrack(range)]);
  };

  setContext<VideoEditorContext>("video-editor", {
    scale,
    tracks,
    addTrackToNext,
    addTrackToPrev,
    expandTimeline,
    removeTrack,
    mergeTracks,
    splitTracks,
    addTrack,
  });
</script>

<slot />
