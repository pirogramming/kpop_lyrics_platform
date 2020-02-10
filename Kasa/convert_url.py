# youtube 영상 링크를 <iframe>에 맞춰서 변환
def convert_youtube(current_url):
    if 'watch?v=' in current_url:
        current_url = current_url.replace("watch?v=", "embed/")
    else:
        current_url = current_url.replace(".com/", ".com/embed/")
    convert_url = current_url

    return convert_url
