export type Scale = {
  domain: [number, number];
  viewDomain: [number, number];
  range: [number, number];
};

// create a mapping object that map domain value to range value
export function makeScale(
  domain: [number, number],
  range: [number, number]
): Scale {
  return {
    domain: domain,
    viewDomain: domain,
    range: range,
  };
}

export function reScale(scale: Scale, domain: [number, number]): Scale {
  const viewDomain: [number, number] = [
    constrainDomain(scale, domain[0]),
    constrainDomain(scale, domain[1]),
  ];
  return {
    ...scale,
    viewDomain,
  };
}

export function reRange(scale: Scale, range: [number, number]): Scale {
  return {
    ...scale,
    range,
  };
}

export function toTranslate(range: [number, number]): string {
  return `transform: translateX(${range[0]}px);`;
}

export function toWidth(range: [number, number]): string {
  return `width: ${range[1] - range[0]}px;`;
}

export function calculateViewDomainDelta(scale: Scale, delta: number) {
  const domainDelta = scale.viewDomain[1] - scale.viewDomain[0];
  const rangeDelta = scale.range[1] - scale.range[0];
  const deltaRatio = domainDelta / rangeDelta;
  const domainDeltaFromRangeDelta = delta * deltaRatio;
  return domainDeltaFromRangeDelta;
}

export function constrainDomain(scale: Scale, value: number): number {
  return Math.min(Math.max(value, scale.domain[0]), scale.domain[1]);
}

export function calculateGap(scale: Scale, tickCount: number = 10): number {
  const containerWidth = scale.range[1] - scale.range[0];
  const gap = containerWidth / tickCount;
  const domainDelta = scale.viewDomain[1] - scale.viewDomain[0];
  const rangeDelta = scale.range[1] - scale.range[0];
  const scaleRatio = domainDelta / rangeDelta;
  const gapInDomain = Math.floor(gap * scaleRatio);
  return gapInDomain;
}

export function mapRangeToViewDomain(
  scale: Scale,
  range: [number, number]
): [number, number] {
  const domainDelta = scale.viewDomain[1] - scale.viewDomain[0];
  const rangeDelta = scale.range[1] - scale.range[0];
  const scaleRatio = domainDelta / rangeDelta;

  const viewDomain = range.map(
    (value) => (value - scale.range[0]) * scaleRatio + scale.viewDomain[0]
  );

  return viewDomain as [number, number];
}

export function mapViewDomainToRange(
  scale: Scale,
  domain: [number, number]
): [number, number] {
  const domainDelta = scale.viewDomain[1] - scale.viewDomain[0];
  const rangeDelta = scale.range[1] - scale.range[0];
  const scaleRatio = rangeDelta / domainDelta;

  const range = domain.map(
    (value) => (value - scale.viewDomain[0]) * scaleRatio + scale.range[0]
  );

  return range as [number, number];
}
