
# first pattern definition
!part1 = [
125,4,4,1,1
125,3,4,1,1
125,2,4,1,1
125,7,8,1,1
]


# second pattern definition
!part2 = [
220,2,4,1,1
220,7,8,1,1
]

# play BPM 220 in 2/4 time signature, repeat once, with accent on first tick
220,2,4,1,1

#play first pattern once
@part1,1

#play second pattern twice
@part2,2


# play BPM 70 in 4/4 time signature, repeat four times, without accents
70,4,4,4,0
