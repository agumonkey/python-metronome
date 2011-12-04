# BPM(30 - 250), Ticks, Ticks per bar(2, 4, 8, 16), Bars, High note(0, 1)
# Example: 120, 6, 8, 4, 1 means 120 BPM in 6/8 metrum, repeat 4 times with accent on first tick

# !name = [ ... ] - pattern definiton, now you can access it by writing:
# @name,5 - which means: repeat pattern 'name' five times.


# first pattern definition
!part1 = [
125,4,4,1,1
125,3,4,1,1
125,2,4,1,1
125,7,8,1,1
]


# second pattern definition
!part2 = [220,2,4,1,1
220,7,8,1,1]

# play BPM 220 in 2/4 time signature, repeat once, with accent on first tick
220,2,4,1,1

#play first pattern once
@part1,1

#play second pattern twice
@part2,2


# play BPM 70 in 4/4 time signature, repeat four times, without accents
70,4,4,4,0
