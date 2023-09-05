import type { Clip } from "$lib/domains/clip";
import type { Comment } from "$lib/domains/comment";
import type { Pagination } from "$lib/domains/pagination";
import axios, { type AxiosInstance } from "axios";
import { none, some, type Option } from "fp-ts/Option";

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
