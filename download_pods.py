import feedparser
import wget
d = feedparser.parse('https://feeds.npr.org/510289/podcast.xml')

max_download = 4
mp3s_list = []

for i,podmeta in enumerate(d['entries']):
    if(i > max_download):
        break
    for linkmeta in podmeta['links']:
        if('.mp3' in linkmeta['href']):
            mp3s_list.append(linkmeta['href'])


for mp3 in mp3s_list:
    file_name = wget.download(mp3, out='audio')

#TODO: download the mp3s_list to the audio/ folder
