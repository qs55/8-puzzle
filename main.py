import numpy as np
from queue import PriorityQueue
from copy import deepcopy

ACTION_COST = 1
GAME_SIZE = 3
STATES_PRODUCED = 0


class State:
    def __init__(self, config=None, path_cost=0, parent_pointer=None, blank_coordinates=(0, 0)):
        self.parent_pointer = parent_pointer
        self.config = config if config is not None else np.zeros((3, 3), 'int')
        self.heuristic = 0
        self.eval_func = 0
        self.path_cost = path_cost
        self.blank_coordinates = blank_coordinates

    def print_state(self):
        for i in range(GAME_SIZE - 1, -1, -1):
            for j in range(GAME_SIZE):
                print(self.config[i][j], end="  ")
            print()
        print()

    def __lt__(self, other):
        return True


class SearchSolution:
    goal_coordinates = {0: (0, 0), 1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0), 5: (0, 0), 6: (0, 0), 7: (0, 0),
                        8: (0, 0)}
    frontier = PriorityQueue()
    visited = []
    states_produced = 0
    states_visited = 0
    states_put_in_frontier: int = 0

    def __init__(self, solution_flag=False):
        self.start_state = SearchSolution.take_config_input("start")
        self.current_state = None
        self.goal_state = SearchSolution.take_config_input("end")
        self.solution_flag = solution_flag

    def initialize_game(self):
        SearchSolution.calculate_heuristic(self.start_state)
        # self.goal_state.heuristic = 0
        SearchSolution.frontier.put((self.start_state.eval_func, self.start_state))
        SearchSolution.states_put_in_frontier += 1
        self.current_state = deepcopy(self.start_state)
        while not SearchSolution.frontier.empty():
            self.current_state = SearchSolution.frontier.get()[1]
            SearchSolution.visited.append(self.current_state)
            SearchSolution.states_visited += 1
            if self.check_goal_state():
                self.solution_flag = True
                solution_size = SearchSolution.print_solution(self.current_state, 0)
                print(f"Solution steps are {solution_size}")
                break
            self.produce_child()

    @staticmethod
    def calculate_heuristic(state):
        distance = 0
        for i in range(GAME_SIZE - 1, -1, -1):
            for j in range(GAME_SIZE):
                if state.config[i][j]:
                    x1, y1 = SearchSolution.goal_coordinates[state.config[i][j]]
                    x = abs(x1 - i)
                    y = abs(y1 - j)
                    distance += (x + y)

        state.heuristic = distance
        state.eval_func = state.path_cost + state.heuristic

    def produce_child(self):
        i, j = self.current_state.blank_coordinates
        children = []
        if i < GAME_SIZE - 1:
            children.append((i + 1, j))  # Up
        if i > 0:
            children.append((i - 1, j))  # Down
        if j > 0:
            children.append((i, j - 1))  # Left
        if j < GAME_SIZE - 1:
            children.append((i, j + 1))  # Right

        for child in children:
            child_state = SearchSolution.produce_state(child, self.current_state)
            SearchSolution.calculate_heuristic(child_state)
            if not SearchSolution.check_in_visited(child_state):
                SearchSolution.frontier.put((child_state.eval_func, child_state))
                SearchSolution.states_put_in_frontier += 1

    @staticmethod
    def produce_state(new_child_coordinates, state):
        x1, y1 = state.blank_coordinates
        x2, y2 = new_child_coordinates
        config = deepcopy(state.config)
        config[x1, y1], config[x2, y2] = config[x2, y2], config[x1, y1]
        path_cost = state.path_cost + ACTION_COST
        blank_coordinates = new_child_coordinates
        parent_pointer = state
        new_state = State(config, path_cost, parent_pointer, blank_coordinates)
        SearchSolution.states_produced += 1
        return new_state

    @staticmethod
    def check_in_visited(state):
        for item in SearchSolution.frontier.queue:
            if (item[1].config == state.config).all():
                return True
        else:
            return False

    def check_goal_state(self):
        if (self.current_state.config == self.goal_state.config).all():
            return True
        return False

    @staticmethod
    def print_solution(state, size):
        if state is not None:
            size = SearchSolution.print_solution(state.parent_pointer, size)
            state.print_state()
        return size + 1

    @staticmethod
    def take_config_input(input_state):
        state = State()
        input_dict = {0: False, 1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False}
        for i in range(GAME_SIZE - 1, -1, -1):
            for j in range(GAME_SIZE):
                while True:
                    try:
                        val = int(input(f"Enter value for the tile located at ({i, j}) coordinate position for {input_state} configuration : "))
                        if 0 <= val <= 8 and not input_dict[int(val)]:
                            state.config[i][j] = val
                            if input_state == "end":
                                SearchSolution.goal_coordinates[val] = (i, j)
                            if not val:
                                state.blank_coordinates = (i, j)
                            input_dict[int(val)] = True
                            break
                        else:
                            print("Given value is not allowed for the configuration")
                            continue
                    except ValueError:
                        print("Given input was not a valid one, try again")
                        continue
        SearchSolution.states_produced += 1
        return state


def main():
    game = SearchSolution()
    # # game.current_state.config[0][0] = 9
    # game.start_state.print_state()
    # game.goal_state.print_state()
    # game.current_state.print_state()
    # print(game.start_state.blank_coordinates)
    game.initialize_game()
    # print(game.start_state.heuristic)

    print("*" * 100)
    print("*" * 100)
    print("*" * 100)
    # while not game.frontier.empty():
    #     config = game.frontier.get()[1].print_state()
    if game.solution_flag:
        print("Solution Found")
    else:
        print("Solution not found")
    print("*" * 100)
    print("*" * 100)
    print("*" * 100)
    print(f"States produced = {SearchSolution.states_produced}")
    print(f"States visited = {SearchSolution.states_visited}")
    print(f"States put in frontier = {SearchSolution.states_put_in_frontier}")


main()
