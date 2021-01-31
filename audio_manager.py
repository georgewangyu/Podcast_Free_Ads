from pydub import AudioSegment
import numpy as np 
from scipy.signal import spectrogram 


def load_to_raw(filename : str):
    audiofile = AudioSegment.from_file(filename)
    return get_channels(audiofile),audiofile

def get_channels(audiofile):
    rawdata =  np.fromstring(audiofile.raw_data, np.int16)
    channels = [rawdata[ch::audiofile.channels] for ch in range(audiofile.channels)]
    return channels 


def fingerprint(audiofile):
    channels,rate  = get_channels(audiofile),audiofile.frame_rate
    FFT_WID = 4096
    FFT_WINDOW_OVERLAP_FRAC = 0.5
    FFT_WINDOW_OVERLAP = np.floor(FFT_WID * FFT_WINDOW_OVERLAP_FRAC) #we want 12.5% overlap between spectrogram samples ? 
    freqs,times,spec =  spectrogram(np.array(channels),rate,nperseg=FFT_WID,noverlap=FFT_WINDOW_OVERLAP)
    #it would be nice to convert the spectrogram into decibels:
    specDB = 10*np.log10(spec,out=np.zeros_like(spec),where = (spec>1))
    peaks = find_peaks(specDB[0])
    hashes = hash_peaks(peaks)
    return hashes 


def find_peaks(specDB_img ):
    from scipy.ndimage.filters import maximum_filter
    from scipy.ndimage.morphology import (binary_erosion,
                                        generate_binary_structure,
                                        iterate_structure)

    #let's find ourselves a peak!
    struct = generate_binary_structure(2, 2) #dimension, taxicab distance.

    #  And then we apply dilation using the following function
    #  http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.iterate_structure.html
    #  Take into account that if PEAK_NEIGHBORHOOD_SIZE is 2 you can avoid the use of the scipy functions and just
    #  change it by the following code:
    #  neighborhood = np.ones((PEAK_NEIGHBORHOOD_SIZE * 2 + 1, PEAK_NEIGHBORHOOD_SIZE * 2 + 1), dtype=bool)
    neighborhood = iterate_structure(struct, 15)

    # find local maxima using our filter mask
    local_max = maximum_filter(specDB_img, footprint=neighborhood) == specDB_img

    # Applying erosion, the dejavu documentation does not talk about this step.
    background = (specDB_img == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # Boolean mask of specDB_img with True at peaks (applying XOR on both matrices).
    detected_peaks = local_max != eroded_background

    # extract peaks
    amps = specDB_img[detected_peaks]
    freqInds, timeInds = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()

    # get indices for frequency and time
    filter_idxs = np.where(amps > 10)

    freqs_filter = freqInds[filter_idxs]
    times_filter = timeInds[filter_idxs]
    
    #okay let's sort based on ascending time, rather than ascending frequency? 
    times_filter,freqs_filter = zip(*sorted(zip(times_filter,freqs_filter)))

    return list(zip(freqs_filter,times_filter))
    
def hash_peaks(peaks ):
    import hashlib
    #let's take in the peaks, and output the corresponding hashes 
    #assume sorted by time.
    hashes = []
    rng = np.random.RandomState(1337)

    #let's use each peak at least once
    #and try it with a few other neighbouring peaks (randomly selected from the future 10 peaks ?) 

    maxind = np.shape(peaks)[0]-1
    for i,peak in enumerate(peaks):
        t0 = peak[0]
        print(i,t0,peak) 
        if(maxind - i < 8): 
            break
        allowed_inds= np.arange( i+1, np.min([i+6,maxind])  )
        other_peaks = np.sort(rng.choice(allowed_inds,np.min([5,maxind-i]),False))
        str = '%d'%(peak[1])
        for op_ind in other_peaks:
            op = peaks[op_ind]
            str+='|%d,%d'%(op[0]-t0,op[1])
    #     print(str)
        h =  hashlib.sha1(str.encode('utf-8'))
        hash = (h.hexdigest(),t0) 
        hashes.append(hash)

    return hashes
        

    

# def strip():
#     pass 



if(__name__ == '__main__'):
    source = 'audio/20210129_pmoney_pmpod1060_2.mp3'
    channels,audiofile = load_to_raw(source) 
    fingerprint(np.array(channels),audiofile.frame_rate) 
