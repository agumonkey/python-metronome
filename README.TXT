Python Metronome

1. Usage.

    Simplest, live mode:
    
    $> python ./metronome.py
    
    will start clicking in 100 BPM 4/4 time signature, without accent.
    
    It is possible to override this settings by using options:
    -b, --bpm BPM - defines beats per minute in live mode. BPM can be only 30 to 250
    -t, --ticks TICKS - defines number of notes in time signature
    -n, --note NOTE - defines notes in time signature. NOTE can be only 2, 4, 8 or 16 
    -a, --accent - switches on first tick accent
    
    From file:
    
    #> python ./metronome.py -f file.mt
    
    will play ticks according to file.mt definitions.
    
    In both cases you can turn on verbose mode by using -v (--verbose) switch
    
2. Using .mt files.

    Simplest way is to write instructions each one in separate line using this pattern:

    bpm,ticks,note,repeats,accent

    For example:
    
    125,6,8,3,1
    
    will play 6/8 time signature, 125 BPM, it will be repeated 3 times with accent on first note in bar.
    
    65,3,4,1,0:
    
    will play 3/4 time signature, 65 BPM, it will be played only once, and without accent on first note in bar.
    
    You can have as much that kind of entries in your file as you want.
    
    Additionaly you can define so called patterns, for example:
    
    !pattern = [
    125,4,4,4,1
    130,4,4,4,1
    100,4,4,8,0
    ]
    
    That pattern won't be played until you write this line:
    
    @pattern,3
    
    Which means: take whole predefined pattern, and repeat it 3 times in song.
    Writting it without using patterns would look like:
    
    125,4,4,4,1
    130,4,4,4,1
    100,4,4,8,0
    
    125,4,4,4,1
    130,4,4,4,1
    100,4,4,8,0
    
    125,4,4,4,1
    130,4,4,4,1
    100,4,4,8,0
    
    
