from __future__ import print_function

import dwavebinarycsp as dbc


def get_label(row, col, direction):
    return "".join([str(row), ",", str(col), direction])


def sum_to_two_or_zero(*args):
    sum_value = sum(args)
    return sum_value in [0, 2]


class Maze():
    #TODO: test for valid start and end; do they HAVE to be on the boarder? no
    def __init__(self, n_rows, n_cols, start, end, walls):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.start = start
        self.end = end
        self.walls = walls
        self.csp = dbc.ConstraintSatisfactionProblem(dbc.BINARY)

    def _apply_valid_move_constraint(self):
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                directions = {get_label(i, j, 'n'), get_label(i, j, 'w'), get_label(i+1, j, 'n'), get_label(i, j+1, 'w')}
                self.csp.add_constraint(sum_to_two_or_zero, directions)

    def _set_start_and_end(self):
        # Constraint: Start and end locations
        self.csp.fix_variable(self.start, 1)  # start location
        self.csp.fix_variable(self.end, 1)  # end location

    def _set_boarders(self):
        # Constraint: No walking through boarders of the maze
        for j in range(self.n_cols):
            top_boarder = get_label(0, j, 'n')
            bottom_boarder = get_label(self.n_rows, j, 'n')

            try:
                self.csp.fix_variable(top_boarder, 0)
            except ValueError:
                if not top_boarder in [self.start, self.end]:
                    raise ValueError

            try:
                self.csp.fix_variable(bottom_boarder, 0)
            except ValueError:
                if not bottom_boarder in [self.start, self.end]:
                    raise ValueError

        for i in range(self.n_rows):
            left_boarder = get_label(i, 0, 'w')
            right_boarder = get_label(i, self.n_cols, 'w')

            try:
                self.csp.fix_variable(left_boarder, 0)
            except ValueError:
                if not left_boarder in [self.start, self.end]:
                    raise ValueError

            try:
                self.csp.fix_variable(right_boarder, 0)
            except ValueError:
                if not right_boarder in [self.start, self.end]:
                    raise ValueError

    def _set_inner_walls(self):
        # Constraint: Inner self.walls of the maze
        for wall in self.walls:
            self.csp.fix_variable(wall, 0)

    def get_bqm(self):
        self._apply_valid_move_constraint()
        self._set_start_and_end()
        self._set_boarders()
        self._set_inner_walls()
        
        bqm = dbc.stitch(self.csp)
        return bqm




