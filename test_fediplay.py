import fediplay

def test_extract_links():
    toot = {
        'content': "<p><a href=\"https://cybre.space/tags/nowplaying\" class=\"mention hashtag\" rel=\"tag\">#<span>nowplaying</span></a> <a href=\"https://cybre.space/tags/fediplay\" class=\"mention hashtag\" rel=\"tag\">#<span>fediplay</span></a> Grimes ft. Janelle Mon\u00e1e - Venus Fly <a href=\"https://www.youtube.com/watch?v=eTLTXDHrgtw\" rel=\"nofollow noopener\" target=\"_blank\"><span class=\"invisible\">https://www.</span><span class=\"ellipsis\">youtube.com/watch?v=eTLTXDHrgt</span><span class=\"invisible\">w</span></a></p>"
    }
    urls = fediplay.extract_links(toot)
    assert urls == ['https://www.youtube.com/watch?v=eTLTXDHrgtw']
