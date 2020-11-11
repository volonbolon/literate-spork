#!/usr/bin/env python

import argparse
import plistlib
import numpy as np
import matplotlib.pyplot as plt

def plot_ratings_and_durations(ratings, durations):
    x = np.array(durations, np.int32)
    x = x / 60000.0
    
    y = np.array(ratings, np.int32)

    plt.subplot(2,1,1)
    plt.plot(x, y, 'o')
    
    plt.axis([0, 1.05*np.max(x), -1, 110])
    plt.xlabel('Track Duration')
    plt.ylabel('Track Rating')

    plt.subplot(2,1,2)
    plt.hist(x, bins=20)
    plt.xlabel('Track Duration')
    plt.ylabel('Count')

    plt.show()

def plot_stats(filename):
    try:
        with open(filename, 'rb') as f:
            plist = plistlib.load(f)
    except Exception as e:
        print(e)
        print('error opening file')
        exit(1)
    tracks = plist['Tracks']
    ratings = []
    durations = []
    for trackId, track in tracks.items():
        try:
            ratings.append(track['Album Rating'])
            durations.append(track['Total Time'])
        except:
            pass

    if len(ratings) == 0 or len(durations) == 0:
        print('No valid rating/Total Duration')
        return

    plot_ratings_and_durations(ratings, durations)

def find_dups(filename):
    print('Finding duplicate tracks in %s…' % filename)
    try:
        with open(filename, 'rb') as f:
            plist = plistlib.load(f)
    except:
        print('Error loading the plist')
        exit(1)
    tracks = plist['Tracks']
    track_names = {}
    for trackId, track in tracks.items():
        try:
            name = track['Name']
            duration = track['Total Time']
            if name in track_names:
                if duration // 1000 == track_names[name][0] // 1000:
                    count = track_names[name][1]
                    track_names[name] = (duration, count+1)
            else:
                track_names[name] = (duration, 1)
        except:
            pass
    dups = []
    for k, v in track_names.items():
        if v[1] > 1:
            dups.append((v[1], k))
    if len(dups) > 0:
        print('Found %d duplicates. Track names saved to dup.txt' % len(dups))
    else:
        print('No dups found')
    fd = open('dups.txt', 'w')
    for val in dups:
        fd.write("[%d] %s\n" % (val[0], val[1]))
    fd.close()

def main():
    descStr = """
    This program analyzes playlist files (.xml) exported from iTunes.
    """
    parser = argparse.ArgumentParser(description = descStr)
    group = parser.add_mutually_exclusive_group()

    group.add_argument('--stats', dest='plFile', required=False)
    group.add_argument('--dup', dest='plFileD', required=False)

    args = parser.parse_args()

    if args.plFile:
        plot_stats(args.plFile)
    elif args.plFileD:
        find_dups(args.plFileD)
    else:
        print('These are not the tracks you are looking for')

if __name__ == '__main__':
    # find_dups('/Users/arielrodriguez/Documents/itunes_py/Library.xml')
    # plot_stats('/Users/arielrodriguez/Documents/itunes_py/Library.xml')
    main()
