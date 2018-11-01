"""
This program accepts tables of exchange rate as input, and checks if arbitrage
opportunity exists for transactions less than or equal to the dimension of
currencies.

We can prove by logic, there will be no repeated using of currencies when we
want to arbitrage with transactions length less than dimension of currencies.
"""


import argparse
import numpy as np
from itertools import combinations
from itertools import permutations


def transform_input(input_matrix, N):
    """
    transform our input_matrix by filling the diagonal term "1" in
    :param input_matrix: exchange rate with diagonal terms missing
    :param N: dimension of currencies
    :return: complete N*N matrix with diagonal terms being 1
    """
    t_input = np.ones((N, N))
    for i in range(N):
        for j in range(0, i):  # fill the numbers before the diagonal term
            t_input[i][j] = input_matrix[i][j]
        for j in range(i + 1, N):  # fill the numbers after the diagonal term
            t_input[i][j] = input_matrix[i][j - 1]
    return t_input


def generate_transaction(N, i):
    """
    generate all the possible transactions with length i (2 <= i <= N)
    e.g. 1, 2, 3 means 1-2-3-1
    :param N: dimension of currencies
    :param i: required length of transactions
    :return: all the possible transactions with length i using N currencies
    """
    transactions = []
    ccy = [i for i in range(N)]
    # from N pick i currency first, get all the combinations
    combs = list(combinations(ccy, i)) 
    for comb in combs:
        # for each combination generate all the permutations
        perm = list(permutations(list(comb))) 
        transactions += perm
    return transactions


def detect_arbitrage(m, N, memo={}):
    """
    detect whether arbitrage exists given the exchange rate matrix
    :param m: the complete exchange rate matrix
    :param N: dimension of currencies
    :param memo: map transactions to values
    :return: all the possible transactions if exists, o/w  "No arbitrage exist"
    """
    arb_chains = []  # list of all possible arbitrage transactions
    for i in range(2, N + 1):  # detect from the shortest transactions
        transactions = generate_transaction(N, i)  # generate transactions
        for t in transactions:
            cycle_result = 1  # start value is 1
            if t[:-1] in memo:  # we have calculate all shorter transactions
                # to calculate 1-2-3-4-1 we first calculate 1-2-3-4 
                # 1-2-3-4 equals to 1-2-3 times 3-4
                cycle_result *= memo[t[:-1]]
                cycle_result *= m[t[-2]][t[-1]]
            else:  # for the first two currency transactions i=2
                cycle_result *= m[t[0]][t[1]]  
            memo[t] = cycle_result  # add result to memo for memoization
            cycle_result *= m[t[-1]][t[0]]  # finish the transaction
            if cycle_result > 1.01:  # if arbitrage exists, add to arb_chains
                cycle_t = list(t) + [t[0]]
                cycle_t = [item + 1 for item in cycle_t]  # index start from 0
                arb_chains.append(cycle_t)
    return arb_chains


def print_arbchains(arb_chains, output_file=None):
    """
    print all chains producing arbitrage and write
    :param arb_chains: a list of lists containing name of currency
    :param output_file: a file used to contain output, default is print-only
    """
    ans_to_write = ""  # record everything need to be written into the file

    if arb_chains:  # if there exists arbitrage
        for arb_chain in arb_chains:
            arb_chain_str = ""
            for ccy in arb_chain:  # format the output
                arb_chain_str += (str(ccy) + "-")
            ans_to_write += arb_chain_str[:-1] + "\n"
    else:  # if no arbitrage exists
        ans_to_write += "no arbitrage sequence exists\n"

    print(ans_to_write)
    ans_to_write += "\n"

    if output_file:
        # write into a text file
        output_file.write(ans_to_write)


def main():
    # parse input file
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    # prepare output file
    output = open("arb_chains.txt", "w+")

    with open(args.filename, encoding='utf-16') as file:
        while True:
            try:
                # read input
                dim = int(file.readline())
                input_matrix = [[float(num) for num in file.readline().split()]
                                            for _ in range(dim)]

                # run the program
                m = transform_input(input_matrix, dim)
                arb_chains = detect_arbitrage(m, dim)
                print_arbchains(arb_chains, output)

            except ValueError:
                # end of the file
                break

    output.close()


if __name__ == "__main__":
    main()
