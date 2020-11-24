import random
 
class Game:                                                                   # class for game minesweeper

    DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))     # tupel used in def - uncover() and auto()

    def __init__(self, width=10, height=10, mines=10):
        self.width = width                                                                  # from __init__ - attributes
        self.height = height                                                                # from __init__ - attributes
        self.mines = mines                                                                  # from __init__ - attributes
        self.covered_cells = self.width*self.height-mines                                   # counter used in def - uncover(), set_flag() and unset_flag()
        self.board = [['?' for x in range(self.width)]                                      # list with lists for 2d board
                      for y in range(self.height)]   
        self.coordinates = [(j, i) for j in range(self.width) for i in range(self.height)]  # creates a list with tuples, every tupel is a coordinate like (x, y)
        self.mines_coordinates = (random.sample(self.coordinates, k=self.mines))            # creates coordinates for the mines
        self.game_status = 'active'                                                         # used to run the game
        self.cell_informations = []                                                         # list with lists - 0: mine? - 1: mines_next_door - 2: covered? - 3: flagged?
        self.zero_coordinates = []                                                          # list used in def - uncover() and auto()
        self.zero_coordinates_count = 0                                                     # counter used in def - uncover() and auto()

    def set_cellinformations(self):                                                         # assign every coordinate a list with informations - 0: mine? - 1: mines_next_door - 2: covered? - 3: flagged?
        check_mines_next_door = 0
        check_position = [0, 0]
        for coordinate in self.coordinates:
            check_mines_next_door = 0
            if coordinate in self.mines_coordinates:                                        # 0: mine?
                check_mine = True
            else:
                check_mine = False
            for direction in self.DIRECTIONS:                                               # 1: mines_next_door
                check_position[0] = coordinate[0]+direction[0]
                check_position[1] = coordinate[1]+direction[1]
                if tuple(check_position) in self.mines_coordinates:
                    check_mines_next_door += 1
            self.cell_informations.append([check_mine, check_mines_next_door, True])        # creates a list 3rd attribute = 2: covered? is at the beginning True for each coordinate
        return len(self.cell_informations)

    def uncover(self, coordinate):                                                          # methode to uncover a coordinate
        x = coordinate[0]-1
        y = coordinate[1]-1
        if self.cell_informations[self.coordinates.index((x, y))][0] == True:               # ceck for a mine on coordinate
            self.board[x][y] = 'B'
            self.game_status = 'over'
            return 'Booooooom! - Game over!'                
        elif self.cell_informations[self.coordinates.index((x, y))][2] == True:             # check that coordinat is covered
            self.board[x][y] = str(self.cell_informations[self.coordinates.index((x, y))][1]) # change the string in list board with number of mines next door
            self.cell_informations[self.coordinates.index((x, y))][2] = False               # change information covered to False
            self.covered_cells -= 1                                                         # this count is important for checking win-status
            if self.cell_informations[self.coordinates.index((x, y))][1] == 0:              # starts when 0 mines next door
                if coordinate not in self.zero_coordinates:                                 # appends coordinate to a list
                    self.zero_coordinates.append((x, y))
                    self.zero_coordinates_count += 1
                self.auto((x, y))                                                           # starts auto methode 
            for i in self.zero_coordinates:                                                 # starts auto methode for each uncovered coordinat with 0 mines next door
                if self.zero_coordinates.index(i) == self.zero_coordinates_count:
                    self.auto(i)
                    self.zero_coordinates_count += 1
            if self.covered_cells == 0:                                                     # checking win-status
                self.game_status = 'over'
                return 'You win!'
            return 'Move O.K!'
        else:                                                                               # returned when cell is allredy uncoverd or it is flagged
            return 'Not allowed!'

    def auto(self, coordinate):                                                             # method to uncover all coordinates arround a coordinate with 0 mines next door
        for direction in self.DIRECTIONS:
            try:
                x = coordinate[0]+direction[0]
                y = coordinate[1]+direction[1]
                if self.cell_informations[self.coordinates.index((x, y))][2] == True:       # checks if coordinate is coverd
                    self.board[x][y] = str(self.cell_informations[self.coordinates.index((x, y))][1]) # change the string in list board with number of mines next door
                    self.cell_informations[self.coordinates.index((x, y))][2] = False       # change information covered to False
                    self.covered_cells -= 1                                                 # this count is important for checking win-status
                if self.cell_informations[self.coordinates.index((x, y))][1] == 0 and (x, y) not in self.zero_coordinates:  # appends coordinate to a list
                    self.zero_coordinates.append((x, y))
            except:
                ValueError     

    def set_flag(self, coordinate):                                                         # methode to set a flag
        x = coordinate[0]-1
        y = coordinate[1]-1
        if self.board[x][y] == '?':
            self.board[x][y] = 'F'
            self.cell_informations[self.coordinates.index((y, x))][2] = False
            self.mines -= 1
            self.covered_cells -= 1
            return 'Flag set!'
        else:
            return 'Cell already uncovered!'

    def unset_flag(self, coordinate):                                                       # methode to unset a flag
        x = coordinate[0]-1
        y = coordinate[1]-1
        if self.board[x][y] == 'F':
            self.board[x][y] = '?'
            self.cell_informations[self.coordinates.index((y, x))][2] = True
            self.mines += 1
            self.covered_cells += 1
            return 'Flag unset!'
        else:
            return 'No flag on coordinate!'

    def save(self):                                                                             # methode to save a game in a text file   
        save_game = open('save.txt','w')  
        save_game.write('mines_coordinates|' + str(self.mines_coordinates))
        save_game.write('\r\nmines|' + str(self.mines))
        save_game.write('\r\ncovered_cells|' + str(self.covered_cells))
        for i in self.board:   
            save_game.write('\r\nboard|' + str(i))
        for i in self.cell_informations:                                                        # 0: mine? - 1: mines_next_door - 2: covered? - 3: flagged? 
            save_game.write('\r\ncell_informations|' + str(i))
        save_game.close()

    @staticmethod                                                                               # staticmethode to load a saved game from a text file
    def load(string):
        board_height = 0
        load_mines_coordinates = tuple
        load_mines = int
        load_covered_cells = int
        load_board = []
        load_cell_informations = []

        load_game = open(string)  
        for line in load_game:
            if line.split('|')[0] == 'cell_informations':
                a = line.split('[')[1].split(']')[0].split(',')
                a_list = []
                if a[0] == 'True':
                    a_list.append(True)
                else:
                    a_list.append(False)
                a_list.append(int(a[1][1:]))
                if a[2][1:] == 'True':
                    a_list.append(True)
                else:
                    a_list.append(False)
                load_cell_informations.append(a_list)
            elif line.split('|')[0] == 'board':
                board_height += 1
                new_list = []
                for i in line.split('[')[1].split(']')[0]:
                    if i != "'" and i != "," and i != ' ':
                        new_list.append(i)
                load_board.append(new_list)
            elif line.split('|')[0] == 'mines_coordinates':
                splitted_string = line.split('[')[1].split(']')[0].split(',')
                count = 0
                a_number = 0
                b_number = 0
                mines_coordinates_list = []
                for i in splitted_string:
                    if count%2 == 0:
                        a_number = int(i.split('(')[1])  
                    if count%2 != 0:
                        b_number = int(i.split(')')[0][1:])
                        mines_coordinates_list.append((a_number, b_number))
                    count += 1
                load_mines_coordinates = mines_coordinates_list
            elif line.split('|')[0] == 'mines':
                load_mines = int(line.split('|')[1])
            elif line.split('|')[0] == 'covered_cells':
                load_covered_cells = int(line.split('|')[1]) 
        board = Game(len(load_board[0]), board_height, 3) 
        board.mines_coordinates = load_mines_coordinates
        board.mines = load_mines
        board.covered_cells = load_covered_cells
        board.board = load_board
        board.cell_informations = load_cell_informations        
        return board

    def shell_display(self):                                                                # methode for output in the commandoline
        lines = []
        output = ['']  
        output. append('Mines: '+ str(self.mines) + '   Covered cells: ' + str(self.covered_cells + self.mines))
        output.append('row')
        for i in range(len(self.board)):
            output.append((str(i+1) + '\t' + '  '.join(self.board[i])))
        for i in range(self.width):
            lines.append(str(i+1))
        output.append('')
        output.append('line' + '\t' + '  '.join(lines))
        output.append('')
        return '\n'.join(output)
       
    def run_game(self):                                                                      # function for play a game in the commandoline
        choise = ''
        selection = ('Enter number:', '1. to uncover.', '2. to set a flag.', '3. to unset a flag.', '4. to save Game.')
        if len(self.cell_informations) != self.height*self.width:
            self.set_cellinformations()
        while self.game_status == 'active':
            print(self.shell_display())
            for i in selection:
                print(i)
            choise = (input('What move do you like next? '))
            if choise == '1':
                print(self.shell_display())
                print('Uncover a cell!')
                print(self.uncover((int(input('Please enter row: ')), int(input('Please enter line: ')))))
            elif choise == '2':
                print(self.shell_display())
                print('Set a Flag!')
                print(self.set_flag((int(input('Please enter row: ')), int(input('Please enter line: ')))))
            elif choise == '3':
                print(self.shell_display())
                print('Unset a Flag!')
                print(self.unset_flag((int(input('Please enter row: ')), int(input('Please enter line: ')))))
            elif choise == '4':
                self.save()                
            print(self.shell_display())
        

if __name__ == '__main__':

    board = Game()                                  # play a new Game
    board.run_game()



    #board = Game().load('save.txt')                # play a saved Game
    #board.run_game()

    
    


