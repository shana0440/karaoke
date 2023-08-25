import { formatDuration, intervalToDuration } from "date-fns";

export function formatTime(duration: number) {
    const zeroPad = (num: number) => String(num).padStart(2, "0");
    const interval = intervalToDuration({ start: 0, end: duration * 1000 });

    return formatDuration(interval, {
        format: ["hours", "minutes", "seconds"],
        zero: true,
        delimiter: ":",
        locale: {
            formatDistance: (_token, count) => zeroPad(count),
        },
    })
}