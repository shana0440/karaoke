import { onMount } from "svelte";
import { writable, get } from "svelte/store";

export const useDrag = (
  onMove: (delta: number) => void,
  onDropped?: (delta: number) => void
) => {
  const isMoved = writable(false);
  const moving = writable(false);
  const prevClientX = writable(0);
  const drag = (e: MouseEvent) => {
    moving.update(() => true);
    prevClientX.update(() => e.clientX);
    isMoved.update(() => false);
  };
  const move = (e: MouseEvent) => {
    if (get(moving)) {
      isMoved.update(() => true);
      prevClientX.update((prev) => {
        onMove(e.clientX - prev);
        return e.clientX;
      });
    }
  };
  const drop = (e: MouseEvent) => {
    if (get(moving)) {
      moving.update(() => false);
      prevClientX.update((prev) => {
        onMove(e.clientX - prev);
        onDropped && onDropped(e.clientX - prev);
        return e.clientX;
      });
    }
  };
  onMount(() => {
    window.addEventListener("mousemove", move);
    window.addEventListener("mouseup", drop);

    return () => {
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseup", drop);
    };
  });
  return {
    moving: { subscribe: moving.subscribe },
    isMoved: { subscribe: isMoved.subscribe },
    drag,
    move,
    drop,
  };
};
