from collections import Counter, OrderedDict, defaultdict
from functools import partial
from itertools import product, combinations
import json
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.spatial.distance import pdist, squareform
import data


def get_token_counts(solution):
    # caveat: 'r' can be either 'right' or 'red' depending on the context
    nesting = 0
    test = False
    counts = defaultdict(int)
    counts = OrderedDict([
        (token, 0)
        for token in ['shoot', 'repeat', 'while', 'if', 'else',
                      'col', 'pos', 'nest']
    ])
    for token in solution:
        if token == '{':
            nesting += 1
            counts['nest'] = max(nesting, counts['nest'])
            test = False
            continue
        if token == '}':
            nesting -= 1
            continue
        if token == 'W':
            counts['while'] += 1
        if token == 'I':
            counts['if'] += 1
        if token == 'R':
            counts['repeat'] += 1
        if token == 's':
            counts['shoot'] += 1
        if token == '/':
            counts['else'] += 1
        if test and token in 'yrgbk':
            counts['col'] += 1
        if test and token == 'x':
            counts['pos'] += 1
        if token in 'WI':
            test = True
    return counts


def canonize(letters):
    # canonize wormhole names
    letters = ['W' if letter in 'XYZ' else letter for letter in letters]
    return letters


def get_letter_counts(statement):
    letters = Counter()
    fields = statement['fields']
    for row in fields:
        for _background, objects in row:
            letters.update(canonize(objects))
    return letters


def get_special_color_count(statement):
    fields = statement['fields']
    colors = set()
    for row in fields:
        for background, _objects in row:
            colors.add(background)
    return len(colors) - 2  # don't count black and blue


def get_features(task):
    statement = json.loads(task.setting)
    solution = task.solution
    #print(statement, '\n*\n', solution)
    # statement features
    letter_counts = get_letter_counts(statement)
    features = OrderedDict([
        (letter, letter_counts[letter])
        for letter in 'AMDW'
    ])
    features['Y'] = get_special_color_count(statement)
    features['limit'] = int('length' in statement)
    features['energy'] = int('energy' in statement)
    # solution features
    token_counts = get_token_counts(solution)
    features.update(token_counts)
    return features


TASKS = data.load('robomission-2018-03-10/tasks.csv')
RAW_FEATURES = pd.DataFrame.from_records([
    get_features(task) for task in TASKS.itertuples()])
STATEMENT_FEATURES = ['A', 'M', 'D', 'W', 'Y', 'limit', 'energy']
SOLUTION_FEATURES = ['shoot', 'repeat', 'while', 'if', 'else', 'col', 'pos', 'nest']


def get_feature_df(which_features='all', transform=None, bias=True):
    """Create a DataFrame with selected and transformed featrues.

    Args:
        which_features: {'statement', 'solution', 'all'}
        transform: {'bin', 'log', 'max', 'zscore', 'idf', 'pref', 'regr'}
           - Can be combined, e.g. 'log+idf'.
           - Note that 'none', 'bin', 'log', 'max', 'zscore'
             and their combination are variants of term-frequency;
             see https://en.wikipedia.org/wiki/Tf%E2%80%93idf
             for descriptions.
           - 'idf', 'pref', 'regr' normalize for feature importance
           - Idf is the "common-one": log(N/n), where N
             is the number of all tasks, n is the number of
             tasks containing the feature.
           - 'pref': increase weight for solution features
    """
    # select features
    feature_names = []
    if which_features in {'statement', 'all'}:
        feature_names += STATEMENT_FEATURES
    if which_features in {'solution', 'all'}:
        feature_names += SOLUTION_FEATURES
    features = RAW_FEATURES[feature_names].copy()
    # apply transformations
    which_transforms = transform.split('+') if transform else []
    if 'log' in which_transforms:
        features = features.apply(lambda s: np.log(s + 1))
    if 'bin' in which_transforms:
        features = features.apply(lambda s: 0 + (s > 0))
    if 'zscore' in which_transforms:
        features = features.apply(lambda s: (s - s.mean())/s.std(ddof=0))
    if 'max' in which_transforms:
        features = features.apply(lambda s: s / s.max())
    if 'idf' in which_transforms:
        idf = lambda f: (-1) * np.log((f > 0).mean())
        features = features.apply(lambda f: f * idf(f))
    if 'pref' in which_transforms:
        assert which_features in {'solution', 'all'}
        solution_preference = 5
        for f in ['repeat', 'while', 'if', 'else', 'col', 'pos']:
            features[f] *= solution_preference
    # add bias feature (if a task has all features 0, it has std=0 and
    # correlation is undefined)
    if bias:
        features['bias'] = 1
    # fix index
    features = features.set_index(TASKS.index)
    return features

#FEATURES = get_feature_df(transform='log+max+idf+pref')
