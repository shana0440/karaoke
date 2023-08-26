def extract_youtube_id(url):
    start = url.find("v=") + 2
    end = url.find("&", start)
    if end == -1:
        end = len(url)
    return url[start:end]
