import numpy as np
import matplotlib.pyplot as plt
class GameOfLife:

    def __init__(self, size_of_board, board_start_mode, rules, rle='', pattern_position=(0,0)):
        self.size_of_board = size_of_board
        self.rules = rules
        self.rle = rle
        self.pattern_position = pattern_position
        if(rle == ''):
            if (5 > board_start_mode > 1):     #if the mode is 2 3 4
                self.board_start_mode = board_start_mode
                self.pattern_position = (10, 10)    #no need the regular pttrnposition anymore (in case of 4)
            else:
                self.board_start_mode = 1
            self.mat = self.board_start()     #putting one of the 4 patterns
        else:
            self.mat = self.stick_rlematrix()    #the case where rle isnt empty


    def board_start(self):
        mat = np.zeros((self.size_of_board, self.size_of_board))
        num = self.board_start_mode
        if (num == 1):
            for i in range(self.size_of_board):
                for j in range(self.size_of_board):
                    if (np.random.randint(0, 2) == 0):
                        mat[i][j] = 0
                    else:
                        mat[i][j] = 255
        elif (num == 2):
            for i in range(self.size_of_board):
                for j in range(self.size_of_board):
                    if (np.random.randint(1, 6) < 5):
                        mat[i][j] = 255
                    else:
                        mat[i][j] = 0
        elif (num == 3):
            for i in range(self.size_of_board):
                for j in range(self.size_of_board):
                    if (np.random.randint(1, 6) < 5):
                        mat[i][j] = 0
                    else:
                        mat[i][j] = 255
        else:
            self.rle = '24bo$22bobo$12b2o6b2o12b2o$11bo3bo4b2o12b2o$2o8bo5bo3b2o$2o8bo3bob2o4bobo$10bo5bo7bo$11bo3bo$12b2o!'
            return self.stick_rlematrix()
        return mat
    def helping_list(self):   #creating a coardinates list for convinient coding of counting living neighbors
        index_list = [i for i in range(self.size_of_board)]
        index_list.insert(0, self.size_of_board - 1)
        index_list.append(0)
        return index_list
    def count_friends(self, mat, point):  # return the number of nliving neighbors
        arr = self.helping_list()
        locx = int(point[0]) + 1
        locy = int(point[1]) + 1
        count = 0
        cells = [[arr[locx - 1], arr[locy - 1]], [arr[locx - 1], arr[locy]], [arr[locx - 1], arr[locy + 1]],
                                 [arr[locx], arr[locy - 1]], [arr[locx], arr[locy + 1]],
                 [arr[locx + 1], arr[locy - 1]], [arr[locx + 1], arr[locy]], [arr[locx + 1], arr[locy + 1]]]
        for i in cells:
            if (mat[i[0]][i[1]] == 255):
                count += 1
        return count
    def trans_rules_to_list(self):
        rules = self.rules[1:len(self.rules)]
        arr = []
        while (rules != ''):
            arr.append(rules[0])
            rules = rules[1:len(rules)]
        arr.remove("S")
        return arr


    def update(self):
        rules = self.trans_rules_to_list()
        size = self.size_of_board
        mat1 = np.copy(self.mat)
        for i in range(size):
            for j in range(size):
                num_friends = self.count_friends(mat1, [i, j])
                if (mat1[i][j] == 0 and str(num_friends) in rules[0: rules.index("/")] or
                    mat1[i][j] == 255 and str(num_friends) in rules[rules.index("/") + 1: len(rules)]):
                    self.mat[i][j] = 255
                else:
                    self.mat[i][j] = 0
        return self.mat

    def save_board_to_file(self, file_name):
        plt.imsave(file_name, self.mat)

    def display_board(self):
        plt.imshow(self.mat)
        plt.pause(0.01)

    def return_board(self):
        return self.mat

    def transform_rle_to_matrix(self, rle):
        mat = [[]]
        index = 0
        while (rle[0] != '!'):
            num = 0
            while (rle[0] != '$' and rle[0] != 'b' and rle[0] != 'o'):
                num = (10 * num) + int(rle[0])
                rle = rle[1:len(rle)]
            if (num != 0):
                if (rle[0] == 'o'):
                    for j in range(num):
                        mat[index].append(255)
                elif (rle[0] == 'b'):
                    for j in range(num):
                        mat[index].append(0)
                else:
                    for i in range(num):
                        mat.append([])
                    index += num
            else:
                if (rle[0] == 'o'):
                    mat[index].append(255)
                elif (rle[0] == 'b'):
                    mat[index].append(0)
                else:
                    mat.append([])
                    index += 1
            rle = rle[1:len(rle)]
        length = 0
        for i in mat:   #notice: every "i" is a line of the matrix
            if (len(i) > length):
                length = len(i)
        for i in mat:
            for j in range(length - len(i)):  #adding zeros to complete to sqare
                i.append(0)
        return mat


    def stick_rlematrix(self):  # pastes the rle matrix to the real one
         x = self.pattern_position[0]
         y = self.pattern_position[1]
         matrix = np.zeros((self.size_of_board, self.size_of_board))
         for i in range(len(self.transform_rle_to_matrix(self.rle))):
             for j in range(len(self.transform_rle_to_matrix(self.rle)[0])):
                  matrix[x + i][y + j] = self.transform_rle_to_matrix(self.rle)[i][j]
         return matrix


x= GameOfLife(50,4,'B3/S23') #example: mode 4
for i in range(100):
    x.display_board()
    x.update()


