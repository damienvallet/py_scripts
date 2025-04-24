# **********************************************************************
# Name : generate_image_from_wavfile.py                                                                    
# version : 1.0
# Author : Damien Vallet
# Role : This script generates a plot of a wav file and saves it as a png image.
# Licence : MIT License (MIT)
# Usage : <python> <script> <path/to/folder/containing/wav/files>
# ******************************************************************

import os, sys
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

def save_plot_as_png(sound_file,output_file):
    """ save a plot of the sound file as a png file """
    downsample_factor = 80
    data, samplerate = sf.read(sound_file)

    data_downsampled = data[::downsample_factor]
    samplerate_downsampled = samplerate // downsample_factor

    length = len(data_downsampled)
    time = np.arange(0, length) / samplerate_downsampled

    # Plot
    plt.plot(time, data_downsampled,linewidth=0.1, alpha=1, color='red')
    plt.axis('tight')
    plt.axis('off')
    plt.savefig(output_file, bbox_inches='tight', pad_inches=0, dpi=200, transparent=True)

def main(folder):
    for file in os.listdir(folder):
        if file.endswith(".wav"):
            output_file = os.path.splitext(file)[0] + '.png'
            save_plot_as_png(folder + file, folder + output_file)

if __name__ == "__main__":
    print("script to generate images from wav files")
    if len(sys.argv) <= 1:
        print("Error: Please specify the folder containing the wav files")
        print("Usage: python3 <script> <folder>")
        sys.exit(1)
    else:
        folder = sys.argv[1]
        main(folder)