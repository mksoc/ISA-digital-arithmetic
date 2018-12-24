#! /usr/bin/python3
from sys import exit
import random


def gen_samples():
    samples = 1000
    mode = 1
    # generate samples
    NB = 12
    print("Generating samples...")

    with open('py-samples.txt', 'w') as outFile:
        for i in range(samples):
            if mode == 1:
                outFile.write('{}\n'.format(
                    random.randint(-2**(NB-1) + 1, 2**(NB-1) - 1)))
            elif mode == 2:
                outFile.write('{}\n'.format(random.choice(
                    [0, -2**(NB-1) + 1, 2**(NB-1) - 1])))
            else:
                print("Error. Unknown error. Exiting.")
                exit(1)
    print("Done.")


if __name__ == '__main__':
    gen_samples()
