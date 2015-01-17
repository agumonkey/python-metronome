#!/usr/bin/env python
# metronome.py - a programable metronome written in python
# Copyright (C) 2011 Piotr Stankiewicz <piotr[dot]stankiewicz{at}gmail(dot).com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import time
import sys
import os.path
import getopt
import re

try:
    import pygame
except ImportError:
    print("ERROR: PyGame needed to run this program. \
          Please install it and try again")
    sys.exit(2)


class Song():

    song = []

    def add(self, data):
        try:
            note = int(data['note'].strip())
            bpm = int(data['bpm'].strip())
            ticks = int(data['ticks'].strip())
            beats = int(data['beats'].strip())
            high = int(data['high'].strip())
        except ValueError:
            return "Integer required"

        if bpm < 30 or bpm > 250:
            return "BPM can be only 30 - 250"

        if note != 2 and note != 4 and note != 8 and note != 16:
            return "note can be only 2, 4, 8 or 16"

        self.song.append({'bpm': bpm,
                         'ticks': ticks,
                         'note': note,
                         'beats': beats,
                         'high': high
                          })
        return None


class Pattern():

    patterns = {}

    def add(self, name, data):
        self.patterns[name] = data


class Metronome():

    VERSION = "0.3"
    FREQ = 44100      # same as audio CD
    BITSIZE = -16     # unsigned 16 bit
    CHANNELS = 2      # 1 == mono, 2 == stereo
    BUFFER = 1024     # audio buffer size in no. of samples
    DURATION = 0.005  # tick length
    live_bpm = 100
    live_ticks = 4
    live_note = 4
    live_accent = False
    verbose = False
    maxtime = 0
    high_name = 'sounds/3520-1760/high.wav'
    low_name = 'sounds/3520-1760/low.wav'
    sound_high = None
    sound_low = None
    report = "BPM: %s - Metrum %s/%s - Accent: %s - Repeats: %s"

    pattern = Pattern()
    song = Song()

    def main(self):
        if not os.path.exists(os.path.join(sys.path[0],
                                           self.high_name)):
            print("File %s not found!" % self.high_name)
            sys.exit(2)
        if not os.path.exists(os.path.join(sys.path[0], self.low_name)):
            print("File %s not found!" % self.low_name)
            sys.exit(2)

        try:
            pygame.mixer.init(self.FREQ, self.BITSIZE,
                              self.CHANNELS, self.BUFFER)
            self.maxtime = int(self.DURATION) * 1000
            self.sound_high = pygame.mixer.Sound(os.path.join(sys.path[0], self.high_name))
            self.sound_low = pygame.mixer.Sound(os.path.join(sys.path[0], self.low_name))

        except pygame.error as exc:
            print("Could not initialize sound system: %s" % exc, file=sys.stderr)

    def play_file(self, filename):
        """
        Play all the bars from file"""

        song = self.load_song(filename)
        try:
            for element in song:
                bpm = 240.0 / element['note'] / element['bpm']
                delay = bpm - self.DURATION
                if self.verbose:
                    print(self.report % (element['bpm'],
                                         element['ticks'],
                                         element['note'],
                                         "yes" if element['high'] == 1 else "no",
                                         element['beats']))
                for i in range(element['beats']):
                    for j in range(element['ticks']):
                        if j == 0 and element['high'] == 1:
                            self.sound_high.play(maxtime=self.maxtime)
                        else:
                            self.sound_low.play(maxtime=self.maxtime)
                        time.sleep(delay)
        except KeyboardInterrupt:
            if self.verbose:
                print("Bye")

    def play_live(self):
        """
        Play bars live"""

        bpm = 240.0 / self.live_note / self.live_bpm
        delay = bpm - self.DURATION
        if self.verbose:
            print(self.report % (self.live_bpm,
                                 self.live_ticks,
                                 self.live_note,
                                 "yes" if self.live_accent == 1 else "no",
                                 "Infinite"))
        try:
            while True:
                for i in range(self.live_ticks):
                    if i == 0 and self.live_accent:
                        self.sound_high.play(maxtime=self.maxtime)
                    else:
                        self.sound_low.play(maxtime=self.maxtime)
                    time.sleep(delay)
        except KeyboardInterrupt:
            if self.verbose:
                print("Bye")

    def load_song(self, fname):
        """
        Loads song to the memory """

        try:
            f = open(fname)
        except IOError as e:
            print("Problem loading file: %s" % e)
            sys.exit(2)
        #pattern search
        pattern_pattern = re.compile(r'''!([a-zA-Z0-9]+)\s*=\s*\[([0-9\,\s]+)\]''', re.I | re.M | re.S)
        pattern_exists = False

        data_file = f.read()
        matches = re.findall(pattern_pattern, data_file)
        for pattern in matches:
            pattern_rows = []
            pattern_parts = pattern[1].split("\n")
            for pattern_part in pattern_parts:
                temp = pattern_part.strip().split(',')
                if len(temp) == 5:
                    pattern_rows.append(temp)
            self.pattern.add(pattern[0], pattern_rows)

        #song load
        f.seek(0)
        for count, line in enumerate(f, start=1):
            line = line.strip()
            if line.startswith('#') or len(line) == 0:
                #skipping empty lines and comments
                continue
            # skip pattern definition
            if line.startswith('!'):  # we have pattern definition
                pattern_exists = True
            if pattern_exists:
                if line.endswith(']'):  # pattern ends here
                    pattern_exists = False
                continue
            # end pattern skipping
            play_pattern = re.compile(r'''@([a-zA-Z0-9]+),\s*(\d+)''')
            matches = re.search(play_pattern, line)
            if matches:  # we have pattern call
                for i in range(int(matches.group(2))):
                    try:
                        for j in self.pattern.patterns[matches.group(1)]:
                            error = self.song.add({'bpm': j[0],
                                                   'ticks': j[1],
                                                   'note': j[2],
                                                   'beats': j[3],
                                                   'high': j[4]
                                                   })
                            if error:
                                print("Line %s: Error: %s" % (count, error))
                                sys.exit(2)
                    except KeyError:
                        print("Line %s: Error: %s" % (count,
                                                      "No such pattern found"))
                        sys.exit(2)
                continue
            entry_pattern = re.compile(r'''([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([01]+)''')
            elements = re.search(entry_pattern, line)
            if elements:
                error = self.song.add({'bpm': elements.group(1),
                                       'ticks': elements.group(2),
                                       'note': elements.group(3),
                                       'beats': elements.group(4),
                                       'high': elements.group(5)
                                       })
                if error:
                    print("Line %s: Error: %s" % (count, error))
                    sys.exit(2)
            else:
                print("Line %s: Error: %s" % (count, "Something is wrong in this line. It won't be played.'"))
        return self.song.song


def usage():
    print("Options are:")
    print("-h, --help - this screen")
    print("-f, --file FILE - loads .mt FILE and plays it's contents \
          (ignores other options except -v)")
    print("-b, --bpm BPM - defines beats per minute in live mode. BPM \
          can be only 30 to 250")
    print("-t, --ticks TICKS - defines number of notes in time signature")
    print("-n, --note NOTE - defines notes in time signature. NOTE can \
          be only 2, 4, 8 or 16 ")
    print("-a, --accent - switches on first tick accent")
    print("-v, --verbose - makes program verbose")
    print("if called without options program starts to play schema:")
    print(metronome.report % (metronome.live_bpm,
                              metronome.live_ticks,
                              metronome.live_note,
                              "yes" if metronome.live_accent == 1 else "no",
                              "Infinite"))
if __name__ == "__main__":
    metronome = Metronome()
    from_file = False
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hf:b:t:n:av",
                                   ["help", "file=", "bpm=", "ticks=",
                                    "note=", "accent", "verbose"])
    except getopt.GetoptError as err:
        usage()
        print(str(err))
        sys.exit(2)
    for o, a in opts:
        if o in ("-f", "--file"):
            from_file = True
            filename = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-b", "--bpm"):
            try:
                metronome.live_bpm = int(a)
            except ValueError as e:
                print("Integer required: %s" % e)
                sys.exit(2)
            if metronome.live_bpm < 30 or metronome.live_bpm > 250:
                print("BPM should be between 30 and 250.")
                sys.exit(2)
        elif o in ("-t", "--ticks"):
            try:
                metronome.live_ticks = int(a)
            except ValueError as e:
                print("Integer required: %s" % e)
                sys.exit(2)
        elif o in ("-n", "--note"):
            try:
                metronome.live_tpb = int(a)
            except ValueError as e:
                print("Integer required: %s" % e)
                sys.exit(2)
            if metronome.live_note != 2 and metronome.live_note != 4 and metronome.live_note != 8 and metronome.live_note != 16:
                print("Note can be only 2, 4, 8, 16!")
                sys.exit(2)
        elif o in ("-a", "--accent"):
            metronome.live_accent = True
        elif o in ("-v", "--verbose"):
            metronome.verbose = True
        else:
            assert False, "nhandled option"

    metronome.main()
    if from_file:
        metronome.play_file(filename)
    else:
        metronome.play_live()
