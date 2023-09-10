<script lang="ts">
  import { isOverlayWithRect, normalizeRect, type Rect } from "$lib/doc/rect";
  import { none, some, match, type Option, isSome } from "fp-ts/Option";
  import { pipe } from "fp-ts/lib/function";
  import { onMount } from "svelte";

  export let targetClass: string;
  export let onSelect: (el: HTMLElement) => void;
  export let onUnSelect: (el: HTMLElement) => void;
  export let container: HTMLElement;
  export let dragableClass: string;

  let rect: Option<Rect> = none;
  let internalSelectedElements: HTMLElement[] = [];

  const getStyle = (rect: Rect) => {
    const { top, left } = container.getBoundingClientRect();
    const normalizedRect = normalizeRect(rect);
    const style = {
      left: `${normalizedRect.left - left}px`,
      top: `${normalizedRect.top - top}px`,
      width: `${normalizedRect.width}px`,
      height: `${normalizedRect.height}px`,
    };
    return Object.entries(style)
      .map(([key, value]) => `${key}: ${value}`)
      .join(";");
  };

  const startDrag = (e: MouseEvent) => {
    const target = e.target as HTMLElement;

    if (target.classList.contains(dragableClass.substring(1))) {
      // NOTE: a workaround to prevent mouse related event won't fire due to state update
      setTimeout(() => {
        rect = some({
          top: e.clientY + container.scrollTop,
          left: e.clientX + container.scrollLeft,
          width: 0,
          height: 0,
        });
        internalSelectedElements = [];
      }, 0);
    }
  };
  const dragging = (e: MouseEvent) => {
    rect = pipe(
      rect,
      match(
        () => none,
        (rect) => {
          e.preventDefault();
          const newRect = {
            ...rect,
            width: e.clientX - rect.left + container.scrollLeft,
            height: e.clientY - rect.top + container.scrollTop,
          };
          const containerRect = container.getBoundingClientRect();

          const scrollDownOffset =
            e.clientY - (containerRect.top + containerRect.height);
          const scrollUpOffset = e.clientY - containerRect.top;
          if (scrollDownOffset > 0) {
            container.scrollTop += scrollDownOffset;
          }
          if (scrollUpOffset < 0) {
            container.scrollTop += scrollUpOffset;
          }

          const rectOffset = {
            top: container.scrollTop,
            left: container.scrollLeft,
          };
          document.querySelectorAll(targetClass).forEach((it) => {
            const el = it as HTMLElement;
            if (isOverlayWithRect(el, newRect, rectOffset)) {
              if (!internalSelectedElements.includes(el)) {
                internalSelectedElements.push(el);
                onSelect(el);
              }
            }
          });

          internalSelectedElements = internalSelectedElements.filter((el) => {
            if (!isOverlayWithRect(el, newRect, rectOffset)) {
              onUnSelect(el);
              return false;
            }
            return true;
          });

          return some(newRect);
        }
      )
    );
  };

  const stopDrag = (e: MouseEvent) => {
    rect = none;
    internalSelectedElements = [];
  };

  onMount(() => {
    window.addEventListener("mousedown", startDrag);
    window.addEventListener("mousemove", dragging);
    window.addEventListener("mouseup", stopDrag);
    return () => {
      window.removeEventListener("mousedown", startDrag);
      window.removeEventListener("mousemove", dragging);
      window.removeEventListener("mouseup", stopDrag);
    };
  });
</script>

{#if isSome(rect)}
  <div
    style={getStyle(rect.value)}
    class="absolute border border-outer-space bg-transparent-black rounded-sm z-10"
  />
{/if}
