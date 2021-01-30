import feedparser
d = feedparser.parse('https://feeds.npr.org/510289/podcast.xml')

max_download = 4
mp3s_list = []

for i,podmeta in enumerate(d['entries']):
    if(i > max_download):
        break
    for linkmeta in podmeta['links']:
        if('.mp3' in linkmeta['href']):
            mp3s_list.append(linkmeta['href'])



#TODO: download the mp3s_list to the audio/ folder
