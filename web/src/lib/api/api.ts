import type { Clip } from "$lib/domains/clip";
import type { Pagination } from "$lib/domains/pagination";
import axios, { type AxiosInstance } from "axios";

export const apiClient = axios.create({
    baseURL: "http://localhost:8888",
});

export function fetchClips(apiClient: AxiosInstance, data: {
    limit?: number,
    offset?: number,
}) {
    return apiClient.request({
        url: "/clips",
        params: data,
    }).then((resp) => {
        return resp.data as Pagination<Clip>
    })
}