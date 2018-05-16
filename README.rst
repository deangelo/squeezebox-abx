Simple ABX tool for comparing audio from multiple squeezeboxes.
===============================================================

- Simple Text user interface
- 2 or more players supported
- Supports multiple users

Usage:
------

create a player configuration file, see example player.json with URLs pointing to your squeezebox players

  ::
    $ python3 abx.py  player.json -o results.json --random
    Running ABX test with 2 sources
    Keyboard usage:
     - 1..9: Select source
     - 0:    Select unknown source
     - q:    Mute all sound
     - e:    Evaluate and save results to file
     - n:    Next trial
     - p [1-9] [comment] choose X=n, for user p. [can be any character except the other commands
    > 1
    > 2
    > 2
    > 0
    > 1
    > 2
    > 0
    > pablo 1
    > user2 1
    > n
    > 1
    > 2
    > 0
    > 1
    > pablo 2
    > user2 1
    > n
    > e
    {'x': 1, 'results': {'user2': [0], 'pablo': [0]}, 'src': [1, 0]}
    {'x': 0, 'results': {'user2': [0], 'pablo': [1]}, 'src': [0, 1]}
    user2: 1/2, 0.500, guess probability: 0.75, choosen sources: {0: 1, 1: 1}
    pablo: 0/2, 0.000, guess probability: 1.00, choosen sources: {1: 2}
      

