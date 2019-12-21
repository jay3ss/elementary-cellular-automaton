"""Definition of cellular automatons"""
import random
import time


class CellularAutomaton:
    def __init__(self, width, ruleset, rand=(False, 0.5), generation=0, state_strs=(u'·', ' ')):
        self.generation = generation
        self.row = []
        self.width = width
        rand_init, density = rand
        if not rand_init:
            self.__create_row()
        else:
            self.__create_random_row(density)
        self.ruleset = ruleset
        self._state_strs = state_strs

    def generate(self):
        next_gen = []
        left = self.row[-1]
        middle = self.row[0]
        right = self.row[1]
        state = self.__rules(left.state, middle.state, right.state)
        cell = Cell(state=state, state_strs=self._state_strs)
        next_gen.append(cell)
        for i in range(1, self.width-1):
            left = self.row[i-1]
            middle = self.row[i]
            right = self.row[i+1]
            state = self.__rules(left.state, middle.state, right.state)
            cell = Cell(state=state, state_strs=self._state_strs)
            next_gen.append(cell)
        left = self.row[-2]
        middle = self.row[-1]
        right = self.row[0]
        state = self.__rules(left.state, middle.state, right.state)
        cell = Cell(state=state, state_strs=self._state_strs)
        next_gen.append(cell)
        # next_gen.append(self.row[-1])
        self.row = next_gen
        self.generation += 1

    def print_row(self):
        for cell in self.row:
            print(cell, end='')

    def terminal_run(self, iterations, delay=0.001):
        for i in range(iterations):
            self.print_row()
            time.sleep(delay)
            print()
            self.generate()

    def __create_random_row(self, density):
        for i in range(self.width):
            cell = Cell()
            cell.state = random.random() < density
            self.row.append(cell)

    def __create_row(self):
        middle = int(self.width/2) - 1
        for i in range(self.width):
            cell = Cell()
            if i == middle:
                cell.state = True
            self.row.append(cell)

    def __rules(self, left, middle, right):
        if left == True and middle == True and right == True:
            return self.ruleset[0]
        elif left == True and middle == True and right == False:
            return self.ruleset[1]
        elif left == True and middle == False and right == True:
            return self.ruleset[2]
        elif left == True and middle == False and right == False:
            return self.ruleset[3]
        elif left == False and middle == True and right == True:
            return self.ruleset[4]
        elif left == False and middle == True and right == False:
            return self.ruleset[5]
        elif left == False and middle == False and right == True:
            return self.ruleset[6]
        elif left == False and middle == False and right == False:
            return self.ruleset[7]

    def __str__(self):
        row = []
        for cell in self.row:
            row.append(cell.to_string())
        return ''.join(row)


class Cell:
    def __init__(self, state=False, state_strs=(u'·', ' ')):
        self.state = state
        self._on, self._off = state_strs

    def to_string(self):
        return self.__str__()

    def __bool__(self):
        return self.state

    def __repr__(self):
        return self.state

    def __str__(self):
        if self.state:
            return self._on
        else:
            return self._off
