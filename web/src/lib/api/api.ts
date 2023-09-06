import type { Clip } from "$lib/domains/clip";
import type { Channel, ChannelWithBanner } from "$lib/domains/channel";
import type { Comment } from "$lib/domains/comment";
import type { Pagination } from "$lib/domains/pagination";
import axios, { type AxiosInstance } from "axios";
import { none, some, type Option } from "fp-ts/Option";
import type { Video } from "$lib/domains/video";
import type { Mv } from "$lib/domains/mv";

export const apiClient = axios.create({
  baseURL: "http://localhost:8888",
  headers: {
    "Content-Type": "application/json",
  },
});

export function fetchClips(
  apiClient: AxiosInstance,
  data: {
    limit?: number;
    offset?: number;
  }
) {
  return apiClient
    .request({
      url: "/clips",
      params: data,
    })
    .then((resp) => {
      return resp.data as Pagination<Clip>;
    });
}

export function fetchMostLikeComment(
  apiClient: AxiosInstance,
  data: {
    videoId: string;
  }
): Promise<Option<Comment>> {
  return apiClient
    .request({
      url: `/videos/${data.videoId}/most-like-comment`,
    })
    .then((resp) => {
      if (resp.data) {
        return some(resp.data);
      } else {
        return none;
      }
    });
}

export function predict(apiClient: AxiosInstance, data: { url: string }) {
  return apiClient
    .request({
      url: `/predict`,
      method: "POST",
      data,
    })
    .then((resp) => {
      return resp.data as { timeslots: [number, number][] };
    });
}

export function saveClips(
  apiClient: AxiosInstance,
  data: {
    videoUrl: string;
    clips: { name: string | undefined; startAt: number; endAt: number }[];
  }
) {
  return apiClient.request({
    url: "clips",
    method: "POST",
    data: {
      stream_url: data.videoUrl,
      clips: data.clips.map((it) => ({
        name: it.name,
        start_at: it.startAt,
        end_at: it.endAt,
      })),
    },
  });
}

export function fetchChannels(
  apiClient: AxiosInstance,
  data: {
    limit?: number;
    offset?: number;
  }
) {
  return apiClient
    .request({
      url: "/channels",
      params: data,
    })
    .then((resp) => {
      return resp.data as Pagination<Channel>;
    });
}

export function fetchChannel(
  apiClient: AxiosInstance,
  data: {
    channelId: number | string;
  }
) {
  return apiClient
    .request({
      url: `/channels/${data.channelId}`,
    })
    .then((resp) => {
      return resp.data as ChannelWithBanner;
    });
}

export function fetchChannelClips(
  apiClient: AxiosInstance,
  data: {
    channelId: number | string;
    limit?: number;
    offset?: number;
  }
) {
  return apiClient
    .request({
      url: `/channels/${data.channelId}/clips`,
      params: {
        limit: data.limit,
        offset: data.offset,
      },
    })
    .then((resp) => {
      return resp.data as Pagination<Clip>;
    });
}

export function searchChannels(
  apiClient: AxiosInstance,
  data: {
    search: string;
    limit?: number;
    offset?: number;
  }
) {
  return apiClient
    .request({
      url: `/channels/search`,
      params: {
        q: data.search,
        limit: data.limit,
        offset: data.offset,
      },
    })
    .then((resp) => {
      return resp.data as Pagination<Channel>;
    });
}

export function searchVideos(
  apiClient: AxiosInstance,
  data: {
    search: string;
    limit?: number;
    offset?: number;
  }
) {
  return apiClient
    .request({
      url: `/videos/search`,
      params: {
        q: data.search,
        limit: data.limit,
        offset: data.offset,
      },
    })
    .then((resp) => {
      return resp.data as Pagination<Video>;
    });
}

export function searchClips(
  apiClient: AxiosInstance,
  data: {
    search: string;
    limit?: number;
    offset?: number;
  }
) {
  return apiClient
    .request({
      url: `/clips/search`,
      params: {
        q: data.search,
        limit: data.limit,
        offset: data.offset,
      },
    })
    .then((resp) => {
      return resp.data as Pagination<Clip>;
    });
}

export function fetchVideo(
  apiClient: AxiosInstance,
  data: {
    videoId: number | string;
  }
) {
  return apiClient
    .request({
      url: `/videos/${data.videoId}`,
    })
    .then((resp) => {
      return resp.data as Video;
    });
}

export function fetchVideoClips(
  apiClient: AxiosInstance,
  data: {
    videoId: number | string;
    limit?: number;
    offset?: number;
  }
) {
  return apiClient
    .request({
      url: `/videos/${data.videoId}/clips`,
      params: {
        limit: data.limit,
        offset: data.offset,
      },
    })
    .then((resp) => {
      return resp.data as Pagination<Clip>;
    });
}

export function fetchMVsFromChannelURL(
  apiClient: AxiosInstance,
  data: {
    channelUrl: string;
  }
) {
  return apiClient
    .request({
      method: "POST",
      url: `/mvs/channel`,
      data: {
        channel_url: data.channelUrl,
      },
    })
    .then((resp) => {
      return resp.data as Mv[];
    });
}

export function fetchMVFromVideoURL(
  apiClient: AxiosInstance,
  data: {
    videoUrl: string;
  }
) {
  return apiClient
    .request({
      method: "POST",
      url: `/mvs/video`,
      data: {
        video_url: data.videoUrl,
      },
    })
    .then((resp) => {
      return resp.data as Mv;
    });
}

export function saveMvs(
  apiClient: AxiosInstance,
  data: { videoIds: string[] }
) {
  return apiClient.request({
    method: "POST",
    url: `/mvs`,
    data: {
      video_ids: data.videoIds,
    },
  });
}
