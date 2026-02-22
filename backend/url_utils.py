from urllib.parse import urlparse, parse_qs

def is_valid_youtube_url(url):

    if len(url) == 0:
        return False

    if url.isspace():
        return False

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False

    youtube_hostnames = ["youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"]
    
    if parsed.hostname.lower() not in youtube_hostnames:
        return False

    return True
     

def url_to_video_id(url):
    if is_valid_youtube_url(url) == False:
        return None
    
    parsed = urlparse(url)
    query_string = parsed.query
    parsed_query = parse_qs(query_string)
    parsed_query_value = parsed_query.get('v')
    
    if isinstance(parsed_query_value, list) and len(parsed_query_value) > 0:
        return parsed_query_value[0]
    
    if parsed.hostname.lower() == "youtu.be":
        return parsed.path[1:]

    


