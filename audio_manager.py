from pydub import AudioSegment
import numpy as np 


def load_to_raw(filename : str):
    audiofile = AudioSegment.from_file(filename)
    rawdata = np.fromstring(audiofile.raw_data, np.int16)

    channels = []
    for chn in range(audiofile.channels):
        channels.append(rawdata[chn::audiofile.channels])

    return channels,audiofile


def fingerprint(rawdata,rate : float):

    pass 


# def strip():
#     pass 



if(__name__ == '__main__'):
    source = 'audio/20210129_pmoney_pmpod1060_2.mp3'
    channels,audiofile = load_to_raw(source) 
    fingerprint(channels,audiofile.frame_rate) 