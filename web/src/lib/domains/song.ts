export interface Song {
  name?: string,
  range: [number, number],
  selected: boolean;
}

export function makeEmptySong(range: [number, number], selected: boolean = false) {
  return {
    range,
    selected,
  }
}