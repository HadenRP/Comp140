"""
Stock market prediction using Markov chains.
"""

import comp140_module3 as stocks
import random


def markov_chain(data, order):
    """
    Create a Markov chain with the given order from the given data.

    inputs:
        - data: a list of ints or floats representing previously collected data
        - order: an integer representing the desired order of the Markov chain

    returns: a dictionary that represents the Markov chain
    """
    chain_dict = {}
    data_len = len(data)
    for index in range(data_len - order):
        current = tuple(data[index : index + order])
        next_val = data[index + order]

        if current not in chain_dict:
            chain_dict[current] = {}
        if next_val not in chain_dict[current]:
            chain_dict[current][next_val] = 1
        else:
            chain_dict[current][next_val] += 1

    for current in chain_dict:
        total = sum(chain_dict[current].values())
        for subitem in chain_dict[current]:
            chain_dict[current][subitem] /= total

    return chain_dict


def predict(model, last, num):
    """
    Predict the next num values given the model and the last values.

    inputs:
        - model: a dictionary representing a Markov chain
        - last: a list (with length of the order of the Markov chain)
                representing the previous states
        - num: an integer representing the number of desired future states

    returns: a list of integers that are the next num states
    """
    next_values = []
    vals = tuple(last)
    possible_states = [0, 1, 2, 3]

    for _ in range(num):
        if vals not in model:
            next_state = random.choice(possible_states)
            next_values.append(next_state)
            vals = (next_state,)
        else:
            total = 0.0
            current = []
            for item in model[vals].keys():
                total += model[vals][item]
                current.append([item, total])
            rand_total = total * random.random()
            for possible, tot in current:
                if rand_total <= tot:
                    next_values.append(possible)
                    vals = vals[1:] + (possible,)
                    break
    return next_values


def mse(result, expected):
    """
    Calculate the mean squared error between two data sets.

    The length of the inputs, result and expected, must be the same.

    inputs:
        - result: a list of integers or floats representing the actual output
        - expected: a list of integers or floats representing the predicted output

    returns: a float that is the mean squared error between the two data sets
    """
    total = 0
    for actual, predicted in zip(result, expected):
        total += (actual - predicted) ** 2

    return total / len(result)


def run_experiment(train, order, test, future, actual, trials):
    """
    Run an experiment to predict the future of the test
    data given the training data.

    inputs:
        - train: a list of integers representing past stock price data
        - order: an integer representing the order of the Markov chain
                 that will be used
        - test: a list of integers of length "order" representing past
                stock price data (different time period than "train")
        - future: an integer representing the number of future days to
                  predict
        - actual: a list representing the actual results for the next
                  "future" days
        - trials: an integer representing the number of trials to run

    returns: a float that is the mean squared error over the number of trials
    """
    model = markov_chain(train, order)
    total = 0
    for _ in range(trials):
        predicted = predict(model, test, future)
        if len(predicted) < future:
            predicted += [predicted[-1]] * (future - len(predicted))
        total += mse(predicted, actual)
    return total / trials


def run():
    """
    Run application.

    You do not need to modify any code in this function. You should
    feel free to look it over and understand it, though.
    """
    symbols = stocks.get_supported_symbols()

    changes = {}
    bins = {}
    for symbol in symbols:
        prices = stocks.get_historical_prices(symbol)
        changes[symbol] = stocks.compute_daily_change(prices)
        bins[symbol] = stocks.bin_daily_changes(changes[symbol])

    test_changes = {}
    test_bins = {}
    for symbol in symbols:
        test_prices = stocks.get_test_prices(symbol)
        test_changes[symbol] = stocks.compute_daily_change(test_prices)
        test_bins[symbol] = stocks.bin_daily_changes(test_changes[symbol])

    # Display data
    # Comment these 2 lines out if you don't want to see the plots
    stocks.plot_daily_change(changes)
    stocks.plot_bin_histogram(bins)

    orders = [1, 3, 5, 7, 9]
    n_trials = 500
    days = 5

    for symbol in symbols:
        print(symbol)
        print("====")
        print("Actual:", test_bins[symbol][-days:])
        for order in orders:
            error = run_experiment(
                bins[symbol],
                order,
                test_bins[symbol][-order - days : -days],
                days,
                test_bins[symbol][-days:],
                n_trials,
            )
            print("Order", order, ":", error)
        print()


run()
