import type { Channel } from "./channel";

export interface Video {
  id: number;
  resource_id: string;
  title: string;
  channel_id: number;
  video_thumbnail: string;
  channel: Channel;
}
