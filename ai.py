class Minimax:

    def __init__(self, depth):
        self.max_depth = depth

    def decision(self, grid):
        up = self.search_d(grid.get_up_grid(), 1, 1)
        down = self.search_d(grid.get_down_grid(), 1, 1)
        left = self.search_d(grid.get_left_grid(), 1, 1)
        right = self.search_d(grid.get_right_grid(), 1, 1)
        dirs = [up, down, left, right]
        return dirs.index(max(dirs))

    def search_d(self, grid, depth, turn):
        if depth == self.max_depth:
            return self._value1(grid.data) + self._value2(grid.data) * 3

        if turn == 0:  # player(ai)
            up = self.search_d(grid.get_up_grid(), depth + 1, 1)
            down = self.search_d(grid.get_down_grid(), depth + 1, 1)
            left = self.search_d(grid.get_left_grid(), depth + 1, 1)
            right = self.search_d(grid.get_right_grid(), depth + 1, 1)
            return max([up, down, left, right])

        # computer
        vacancy = []
        for i in range(4):
            for j in range(4):
                if grid.data[i][j] == 0:
                    vacancy.append((i, j))
        values = []
        for i, j in vacancy:
            new_grid = grid.clone()
            new_grid.data[i][j] = 1
            values.append(self.search_d(new_grid, depth, 0))
        return min(values)

    def _value1(self, matrix):
        """if the max block is at corner, and the less is beside the max"""
        res = 0

        max_value, max_i, max_j, max_ijs = 0, 0, 0, []
        for i in range(4):
            for j in range(4):
                if matrix[i][j] > max_value:
                    max_ijs.clear()
                    max_value = matrix[i][j]
                    max_ijs.append((i, j))
                if matrix[i][j] == max_value:
                    max_ijs.append((i, j))

        for i, j in max_ijs:
            if self._max_at_corner(i, j, matrix):
                res += 10
            else:
                res -= 5

        if self._max2_beside_max(max_i, max_j, matrix):
            res += 10

        return res

    def _value2(self, matrix):
        vac_count = 0
        for i in range(4):
            for j in range(4):
                if matrix[i][j] == 0:
                    vac_count += 1
        return vac_count

    def _max_at_corner(self, max_i, max_j, matrix):

        i0, i1, j0, j1 = max_i, max_i, max_j, max_j
        while i0 < 4 and i1 >= 0:
            if matrix[i0][max_j] != 0:
                return False
            if matrix[i1][max_j] != 0:
                return False
            i0 += 1
            i1 -= 1
        while j0 < 4 and j1 >= 0:
            if matrix[max_i][j0] != 0:
                return False
            if matrix[max_i][j1] != 0:
                return False
            j0 += 1
            j1 -= 1
        return True

    def _max2_beside_max(self, max_i, max_j, matrix):
        max2 = matrix[max_i][max_j] - 1

        if max2 <= 0:
            return True

        max2_i, max2_j = -1, -1  # if max2 is in matrix
        for i in range(4):
            for j in range(4):
                if matrix[i][j] == max2:
                    max2_i, max2_j = i, j

        if max2_i < 0 or max2_j < 0:
            return True
        else:
            if (abs(max_i-max2_i) == 1 and max_j == max2_j) or (abs(max_i-max2_i) == 1 and max_j == max2_j):
                return True

        return False
