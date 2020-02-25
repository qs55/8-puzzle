import numpy as np
from queue import PriorityQueue
from copy import copy, deepcopy

# Would it be ok to use dictionary to store config

ACTION_COST = 1
GAME_SIZE = 3

class State:
    def __init__(self, config=None, path_cost =0, parent_pointer=None, blank_coordinates=(0,0)):
        self.parent_pointer = parent_pointer
        self.config = config if config else np.zeros((3,3),'int')
        self.heuristic = State.calc_heuristic(config)
        self.path_cost = path_cost
        self.blank_coordinates = blank_coordinates

    @staticmethod
    def calc_heuristic(config):
        # Calculation
        # self.heuristic = calculation
        pass

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



class SearchSolution:
    def __init__(self, start_state=None, goal_state=None, frontier=PriorityQueue(), visited=[], solution_flag=False):
        self.start_state = SearchSolution.take_config_input("start")
        self.current_state = deepcopy(self.start_state)
        self.goal_state = SearchSolution.take_config_input("end")
        self.frontier = frontier
        self.visited = visited
        self.solution_flag = solution_flag

    @staticmethod
    def take_config_input(input_state):
        state = State()
        input_dict = {0:False, 1:False, 2:False, 3:False, 4:False, 5:False, 6:False, 7:False, 8:False}
        for i in range(GAME_SIZE-1, -1, -1):
            for j in range(GAME_SIZE):
                while True:
                    try:
                        val= input(f"Enter value for the tile located at ({i, j}) coordinate position for {input_state} configuration : ")
                        if (not val and not input_dict[0]):
                            state.config[i][j] = 0
                            input_dict[0] = True
                            state.blank_coordinates = (i, j)
                            break
                        elif (1 <= int(val) <= 8 and not input_dict[int(val)]):
                            state.config[i][j] = int(val)
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
        if i > 0:
            children.append((i-1, j))       # Up
        if i < GAME_SIZE-1:
            children.append((i+1, j))       # Down
        if j > 0:
            children.append((i,j-1))        #Left
        if j < GAME_SIZE-1:
            children.append((i, j+1))       #Right


        for child in children:
            state = self.produce_state(child, self.current_state)
            self.frontier.put(state)    # If it does not exist in the frontier already other wise update cost

    def produce_state(self, coordinates , state):
        x1, y1 = state.blank_coordinates
        x2, y2 = coordinates
        config = deepcopy(state.config)
        config[x1, y1] , config[x2, y2] = config[x2,y2], config[x1, y1]
        path_cost = state.path_cost + ACTION_COST
        blank_coordinates = coordinates
        parent_pointer = state

        new_state = State(config, path_cost, parent_pointer, blank_coordinates)
        return new_state

    def check_frontier(self):   # check if a node exists in frontier
        pass

    def start_search(self):
        pass

    def print_solution(self):
        pass

def main():
    game = SearchSolution()
    game.current_state.config[0][0] = 9
    game.start_state.print_state()
    game.goal_state.print_state()
    game.current_state.print_state()

main()


