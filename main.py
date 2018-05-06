from bs4 import BeautifulSoup
from bs4.element import Comment
from tamil import utf8
import re
import urllib2

#MIN_LENGTH = 5
#def get_tamil(text):
#    lines = []
#    for txt in text.split("."):
#        new_txt = extract_tamil_text(txt).strip()
#        if new_txt and len(new_txt) > MIN_LENGTH:
#            lines.append(new_txt)
#    return u"\n".join(lines)

def get_tamil(text):
    p = re.compile(r"^[\u0B82\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BBE-\u0BC2\u0BC6-\u0BC8\u0BCA\u0BCD\u0BD0\u0BD7\u0BE6-\u0BFA]+")
    p = re.compile(ur"^[\u0B82-\u0BFA]+")
    return p.sub("\0", text)

def extract_tamil_text(txt):
    letters = utf8.get_letters(txt)
    words = utf8.get_tamil_words(letters)
    text = u" ".join(t for t in words)
    return text

def get_text(soup):
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u"\n".join(t.strip() for t in visible_texts)

def get_soup(url):
    data = urllib2.urlopen(url).read().decode("utf-8-sig")
    return BeautifulSoup(data, "html.parser")

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

crawled_urls = set()

def crawl_tamil(url, depth):
    if depth <= 0 or url in crawled_urls or not url.startswith('http'):
        return
    crawled_urls.add(url)
    try:
        soup = get_soup(url)
    except Exception:
        return
    text = get_text(soup)
    tamil = get_tamil(text)
    with open("tamil.txt", "a+") as fp:
        fp.write(tamil.encode("utf-8")+"\n")

    for a in soup.find_all('a', href=True):
        new_url = a['href']
        crawl_tamil(new_url, depth-1)

def main():
    url = "https://ta.wikipedia.org/wiki/%E0%AE%95%E0%AF%8A%E0%AE%B4%E0%AF%81%E0%AE%AA%E0%AF%8D%E0%AE%AA%E0%AF%81_%E0%AE%85%E0%AE%AE%E0%AE%BF%E0%AE%B2%E0%AE%AE%E0%AF%8D"
    crawl_tamil(url, 1)

if __name__ == '__main__':
    main()
