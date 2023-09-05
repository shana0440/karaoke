export interface Channel {
  id: number;
  title: string;
  thumbnail_url: string;
  custom_url: string;
  resource_id: string;
}

export interface ChannelWithBanner extends Channel {
  banner_url: string;
}

export function sizeBanner(url: string, width: number) {
  return `${url}=w${width}`;
}
