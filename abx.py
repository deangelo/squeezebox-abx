#!/usr/bin/env python3
#
# ABX script using lms
# Copyright Pablo d'Angelo
#
# Licenced under GPL V3
#

import argparse
import math
import random
import json
from collections import defaultdict
import urllib.request
import traceback

# config

randomize_ab=False

class LMSSwitcher(object):
    # switcher object
    def __init__(self, choices):
        """Test """
        self.active = 0
        self.choices = choices

    def off(self, i):
        url = self.choices[i]["url"]%0
        #print(url)
        urllib.request.urlopen(url).read()
    
    def on(self, i):
        url = self.choices[i]["url"]%self.choices[i]["volume"]
        #print(url)
        urllib.request.urlopen(url).read()

    def volume_inc(self):
        self.choices[self.active]["volume"] = self.choices[self.active]["volume"] + 1
        self.on(self.active)
        print(choices)

    def volume_dec(self):
        self.choices[self.active]["volume"] = self.choices[self.active]["volume"] - 1
        self.on(self.active)
        print(choices)

    def __len__(self):
        return len(self.choices)

    def __call__(self, choice):
        """Test """
        self.off(self.active)
        # TODO: add sleep?
        self.on(choice)
        self.active=choice

class ABX(object):
    #
    def __init__(self, switch, resultfile=None, randomize=False):
        self.switch = switch
        self.resultfile = resultfile
        self.randomize_ab = randomize
        
        # experiments contains list of {src=[a_idx, b_idx],
        #                               x=x_idx,
        #                               results={listener:[guess_idx, comment], ...}
        self.experiments = []
        random.seed()

    def setup(self):
        experiment = dict(x=random.randrange(len(self.switch)), results=dict())
        # setup experient
        experiment["src"] = list(range(len(self.switch)))
        if self.randomize_ab:
            random.shuffle(experiment["src"])

        self.experiment = experiment
        #print (self.experiment)

    def on_input(self, value):
        # handle user input (switch sources, or report result)
        #print("on_input: %s"%value)
        try:
            i = int(value)
            if i == 0:
                self.switch(self.experiment["x"])
            elif i < len(self.switch)+1:
                self.switch(self.experiment["src"][i-1])
            else:
                print("Invalid source:",i, "max:", len(self.switch))
        except ValueError:
            try:
                if value.startswith("+"):
                    # increase volume
                    self.switch.volume_inc()
                elif value.startswith("-"):
                    # increase volume
                    self.switch.volume_dec()
                elif value.startswith("q"):
                    # mute
                    for l in range(len(self.switch)):
                        self.switch.off(l)
                elif value.startswith("n"):
                    # save experiment
                    self.experiments.append(self.experiment)
                    # prepare new experiment
                    self.setup()
                elif value.startswith("e"):
                    results = self.evaluate(self.experiments)
                    if self.resultfile:
                        # dump config into save file
                        json.dump(dict(experiments=self.experiments,
                                       sources=self.switch.choices,
                                       results=results),
                                  open(self.resultfile,"w"))
                    # TODO: save to file, if requested
                else:
                    v = value.split()
                    v[1] = int(v[1]) -1
                    # check if user name was given
                    self.experiment["results"][v[0]] = v[1:]
            except Exception as exc:
                print("Invalid input:", value)
                print(traceback.format_exc())
                print(exc)
        
    def evaluate(self, experiments):
        # extract statistics per user
        users = defaultdict(list)
        for e in experiments:
            print(e)
            for u,r in e["results"].items():
                users[u].append([1 if r[0] == e["x"] else 0, e["src"][r[0]]])
        # evaluate results for each user
        results = dict()
        for u,r in users.items():
            n = len(r)
            k = sum(next(zip(*r)))
            p = 0.0
            for x in range(k, n + 1):
                p = p + math.factorial(n) / (math.factorial(x) * math.factorial(n - x)) * 0.5 ** n

            trials=defaultdict(int)
            # count number of each source choosen
            for r1 in r:
                trials[r1[1]] += 1
            results[u] = dict(trials=n, correct=k, rate=1.0*k/n, probability=p, choosen=dict(trials))
            print("%s: %d/%d, %.3f, guess probability: %.2f, choosen sources: %s"%(u, k, n, 1.0*k/n, p, dict(trials)))
            #print(u, results)
        return results
           
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("switch_file")
    parser.add_argument("-o", help="Save results to file")
    parser.add_argument("-r", "--random", help="Randomize sources", action="store_true")
    args = parser.parse_args()

    # configure switch
    choices=json.load(open(args.switch_file))
    switch = LMSSwitcher(choices)

    # run experiment
    abx = ABX(switch, resultfile=args.o, randomize=args.random)
    abx.setup()

    print("Running ABX test with",len(choices),"sources")
    print("Keyboard usage:")
    print(" - 1..9: Select source")
    print(" - 0:    Select unknown source")
    print(" - q:    Mute all sound")
    print(" - +:    Increase volume of current source")
    print(" - -:    Decreas volume of current source")
    print(" - e:    Evaluate and save results to file")
    print(" - n:    Next trial")
    print(" - p [1-9] [comment] choose X=n, for user p. [can be any character except the other commands")
    
    while True:
        inp = input("> ");
        abx.on_input(inp.strip())
    
    

