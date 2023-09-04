export interface Track {
  name?: string,
  range: [number, number],
  selected: boolean;
}

export function makeEmptyTrack(range: [number, number], selected: boolean = false) {
  return {
    range,
    selected,
  }
}