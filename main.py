import numpy as np
from queue import PriorityQueue
from copy import copy, deepcopy

# Would it be ok to use dictionary to store config

ACTION_COST = 1
GAME_SIZE = 3

class State:
    def __init__(self, config=None, path_cost =0, parent_pointer=None, blank_coordinates=(0,0)):
        self.parent_pointer = parent_pointer
        self.config = config if config is not None else np.zeros((3,3),'int')
        self.heuristic = 0
        self.path_cost = path_cost
        self.blank_coordinates = blank_coordinates

    def update_parent_pointer(self, pointer):
        self.parent_pointer = pointer

    def update_path_cost(self, cost):
        self.path_cost = cost

    def print_state(self):
        for i in range(GAME_SIZE-1, -1, -1):
            for j in range(GAME_SIZE):
                print(self.config[i][j], end="  ")
            print()
        print()

    def update_blank_coordinates(self):
        for i in range(GAME_SIZE):
            for j in range(GAME_SIZE):
                if self.config[i][j] == 0:
                    return (i, j)

    def __lt__(self, other):
        return True



class SearchSolution:
    goal_coordinates = {0:(0,0), 1:(0,0), 2:(0,0), 3:(0,0), 4:(0,0), 5:(0,0), 6:(0,0), 7:(0,0), 8:(0,0)}
    def __init__(self, start_state=None, goal_state=None, frontier=PriorityQueue(), visited=[], solution_flag=False):
        self.start_state = SearchSolution.take_config_input("start")
        self.current_state = deepcopy(self.start_state)
        self.goal_state = SearchSolution.take_config_input("end")
        self.frontier = frontier
        self.visited = visited
        self.solution_flag = solution_flag

    def initialize_game(self):
        SearchSolution.calculate_heuristic(self.start_state)
        self.goal_state.heuristic = 0
        self.produce_child()

    @staticmethod
    def calculate_heuristic(state):
        distance = 0
        for i in range(GAME_SIZE-1, -1, -1):
            for j in range(GAME_SIZE):
                if state.config[i][j]:
                    x1, y1 = SearchSolution.goal_coordinates[state.config[i][j]]
                    x = abs(x1-i)
                    y = abs(y1-j)
                    distance += (x+y)

        state.heuristic = distance

    @staticmethod
    def take_config_input(input_state):
        state = State()
        input_dict = {0:False, 1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False}
        for i in range(GAME_SIZE-1, -1, -1):
            for j in range(GAME_SIZE):
                while True:
                    try:
                        val= int(input(f"Enter value for the tile located at ({i, j}) coordinate position for {input_state} configuration : "))
                        if (0 <= val <= 8 and not input_dict[int(val)]):
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
        return state

    def produce_child(self):
        i, j = self.current_state.blank_coordinates
        children = []
        if i < GAME_SIZE-1:
            children.append((i+1, j))       # Up
        if i > 0 :
            children.append((i-1, j))       # Down
        if j > 0:
            children.append((i,j-1))        #Left
        if j < GAME_SIZE-1:
            children.append((i, j+1))       #Right


        for child in children:
            child_state = self.produce_state(child, deepcopy(self.current_state))
            SearchSolution.calculate_heuristic(child_state)
            fn = child_state.heuristic + child_state.path_cost
            self.frontier.put((fn, child_state))    # If it does not exist in the frontier already other wise update cost

    def produce_state(self, coordinates , state):
        x1, y1 = state.blank_coordinates
        x2, y2 = coordinates
        config = deepcopy(state.config)
        config[x1, y1], config[x2, y2] = config[x2, y2], config[x1, y1]
        path_cost = state.path_cost + ACTION_COST
        blank_coordinates = coordinates
        parent_pointer = state

        new_state = State(config, path_cost, parent_pointer, blank_coordinates)
        return new_state

    @staticmethod
    def check_in_frontier(state):
        pass

    def check_frontier(self):   # check if a node exists in frontier
        pass

    def start_search(self):
        pass

    def print_solution(self):
        pass

def main():
    game = SearchSolution()
    # game.current_state.config[0][0] = 9
    game.start_state.print_state()
    game.goal_state.print_state()
    game.current_state.print_state()
    print(game.start_state.blank_coordinates)
    game.initialize_game()
    print(game.start_state.heuristic)

    print("*" * 100)
    while not game.frontier.empty():
        config = game.frontier.get()[1].print_state()

main()


