import { describe, it, expect } from "vitest";
import { makeScale, mapRangeToViewDomain, mapViewDomainToRange } from "./scale";

describe("scale test", () => {
  it("map domain 0-100 to range 0-1000", () => {
    const scale = makeScale([0, 100], [0, 1000]);
    expect(mapViewDomainToRange(scale, [0, 100])).toStrictEqual([0, 1000]);
    expect(mapViewDomainToRange(scale, [25, 75])).toStrictEqual([250, 750]);
    expect(mapViewDomainToRange(scale, [50, 51])).toStrictEqual([500, 510]);
  });

  it("map range 0-1000 to domain 0-100", () => {
    const scale = makeScale([0, 100], [0, 1000]);
    expect(mapRangeToViewDomain(scale, [0, 1000])).toStrictEqual([0, 100]);
    expect(mapRangeToViewDomain(scale, [250, 750])).toStrictEqual([25, 75]);
    expect(mapRangeToViewDomain(scale, [500, 510])).toStrictEqual([50, 51]);
  });
});
