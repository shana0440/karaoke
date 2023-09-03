import type { Video } from "./video";

export interface Clip {
    id: number;
    name: string;
    start_at: number;
    end_at: number;
    video: Video;
    created_at: string;
    updated_at: string;
}
