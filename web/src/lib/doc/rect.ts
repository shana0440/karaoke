export type Rect = {
  top: number;
  left: number;
  width: number;
  height: number;
};

export const normalizeRect = (rect: Rect): Rect => {
  const { top, left, width, height } = rect;
  const newWidth = Math.abs(width);
  const newHeight = Math.abs(height);

  return {
    top: height < 0 ? top + height : top,
    left: width < 0 ? left + width : left,
    width: newWidth,
    height: newHeight,
  };
};

export const isOverlayWithRect = (
  element: HTMLElement,
  rect: Rect,
  scrollOffset: { top: number; left: number }
): boolean => {
  const { top, left, width, height } = normalizeRect(rect);
  const {
    top: elementTop,
    left: elementLeft,
    width: elementWidth,
    height: elementHeight,
  } = element.getBoundingClientRect();

  const elementBottom = elementTop + elementHeight;
  const elementRight = elementLeft + elementWidth;

  const isOverlapping =
    elementTop <= top + height - scrollOffset.top &&
    elementBottom >= top - scrollOffset.top &&
    elementLeft <= left + width - scrollOffset.left &&
    elementRight >= left - scrollOffset.left;

  return isOverlapping;
};
