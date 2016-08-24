from math import exp, lgamma, log
import itertools
import sys

def num_subsequences(seq, sub):
    """Count the occurrences of sub in seq."""
    m,n = len(seq),len(sub)
    count = 0
    for i in range(m-n+1):
        found = True
        for j in range(n):
            if seq[i+j] != sub[j]:
                found = False
                break
        if found:
            count += 1
    return count

def total_num_subsequences(x,v,alphabet):
    """Count the occurrences in x of all possible sequences with prefix v."""
    return sum([num_subsequences(x,v+a) for a in alphabet])

def K(m,x,alphabet):
    """Implements formula (1.19) of Ryabko et al. 2016."""
    t = len(x)
    A = float(len(alphabet))
    if t <= m:
        return exp(-t*log(A))
    else:
        universe = [alphabet]*m
        acc = 0.0
        for v in itertools.product(*universe):
            v = ''.join(list(v))
            acc2 = 0.0
            for a in alphabet:
                acc2 += lgamma(num_subsequences(x,v+a)+0.5)-lgamma(0.5)
            acc += acc2-lgamma(total_num_subsequences(x,v,alphabet)+0.5)+lgamma(A*0.5)
        return exp(-m*log(A)+acc)

def R(x, alphabet=['0','1']):
    """Implements formula (1.25) of Ryabko et al. 2016."""
    t = len(x)
    acc = 0.0
    k = float('inf')
    i = 0
    while i <= log(t+1)/log(2)+5:
        k = (1.0/log(i+2)-1.0/log(i+3))*K(i,x,alphabet)
        acc += k
        i += 1
    return acc

def Rcond(a,x,alphabet=['0','1']):
    """Implements formula (1.50) of Ryabko et al. 2016.
    Computes the conditional probability of the next element of the sequence being a given the history x."""
    r = R(x)
    if r == 0.0:
        return 1.0
    else:
        return R(x+a,alphabet=alphabet)/r

def fetch_input():
    """Repeatedly gets user input until the user enters '0' or '1'."""
    s = ''
    while True:
        s = input('Enter 0 or 1: ')
        if s == '0' or s == '1':
            return s
        else:
            print('Bad input')

def argmax(x):
    """Computes the index of the largest element of x."""
    m = 0
    for i in range(len(x)):
        if x[i] > x[m]:
            m = i
    return m

def main_loop(total,inputs):
    """The logic of the user input guessing game.
    This function plays the game for total rounds, using the history contained in inputs.
    Returns the history with newest inputs appended.
    Also prints status updates of the predictor's performance."""
    correct = 0                 # number of correct guesses
    guessed = 0                 # number of guesses made by the predictor
    thresh = 0.5                # make a prediction of 0 if the conditional probability of 0 is higher than thresh
    for i in range(1,total+1):
        p = Rcond('0',inputs)
        actual = fetch_input()
        if p > thresh and actual == '0':
            correct += 1
            guessed += 1
            print('Input: %s, Prediction: 0'%actual)
            print('Universal predictor accuracy: %.2f%%'%(100*correct/guessed))
        elif p < thresh and actual == '1':
            correct += 1
            guessed += 1
            print('Input: %s, Prediction: 1'%actual)
            print('Universal predictor accuracy: %.2f%%'%(100*correct/guessed))
        elif (p < thresh and actual == '0') or (p > thresh and actual == '1'):
            guessed += 1
            print('Incorrect!')
            print('Universal predictor accuracy: %.2f%%'%(100*correct/guessed))
        else:
            print('Pass!')
            if guessed == 0:
                print('Universal predictor accuracy: unknown')
            else:
                print('Universal predictor accuracy: %.2f%%'%(100*correct/guessed))
        inputs += actual
    return inputs

if __name__ == '__main__':
    argc = len(sys.argv)-1
    if argc != 2:
        print('Wrong number of arguments: expected 2, got %d'%argc)
        sys.exit(1)
    training_rounds = int(sys.argv[1])
    print('Training phase of %d rounds initiated.'%training_rounds)
    inputs = main_loop(training_rounds,'')
    competitive_rounds = int(sys.argv[2])
    print('Competitive phase of %d elements initiated'%competitive_rounds)
    main_loop(competitive_rounds,inputs)
