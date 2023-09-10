import type { KeyboardEventHandler } from "svelte/elements";

export function handleKey<T extends EventTarget>(
  keys: string[],
  handler: (e: KeyboardEvent & { currentTarget: EventTarget & T }) => void
): KeyboardEventHandler<T> {
  return (e) => {
    if (keys.includes(e.key)) {
      handler(e);
    }
  };
}
