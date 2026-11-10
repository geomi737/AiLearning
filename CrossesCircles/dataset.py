import copy
import json

import numpy as np


def is_ended(game: list):
    first_row = set()
    second_row = set()
    third_row = set()
    first_column = set()
    second_column = set()
    third_column = set()
    left_diagonal = set()
    right_diagonal = set()
    all_items = [first_row,
                 second_row,
                 third_row,
                 first_column,
                 second_column,
                 third_column,
                 left_diagonal,
                 right_diagonal]

    for i in range(len(game)):
        first_row.add(game[0][i])
        second_row.add(game[1][i])
        third_row.add(game[2][i])
        first_column.add(game[i][0])
        second_column.add(game[i][1])
        third_column.add(game[i][2])
        left_diagonal.add(game[i][i])
        right_diagonal.add(game[-(i + 1)][i])

    if any(map(lambda x: len(x) < 2 and -1 in x, all_items)):
        return -1
    elif any(map(lambda x: len(x) < 2 and 1 in x, all_items)):
        return 1
    elif all(map(lambda x: 0 not in x and 1 in x, all_items)):
        return 0
    else:
        return None


default_map = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]

all_combinations = []

move = -1


def minimax(situation: list, move: int):
    status = is_ended(situation)
    if status or status == 0:
        return status
    result_map = [
        [-move, -move, -move],
        [-move, -move, -move],
        [-move, -move, -move],
    ]
    for i in range(3):
        for j in range(3):
            if situation[i][j] != 0:
                continue
            new_situation = copy.deepcopy(situation)
            new_situation[i][j] = move
            result = minimax(new_situation, -move)
            result_map[i][j] = result
    combination = {"situation": situation, "result_map": result_map}
    all_combinations.append(combination)
    return max(map(max, result_map)) if move == 1 else min(map(min, result_map))


minimax(default_map, move)
minimax(default_map, -move)

with open("dataset_impr.jsonl", "w", encoding="UTF-8") as f:
    for line in all_combinations:
        f.write(json.dumps(line) + "\n")
