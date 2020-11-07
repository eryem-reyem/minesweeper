import game

# pytest test_game.py

def test_board():
    board = game.Game(5, 5, 5)
    assert len(board.board) == board.height
    for alist in board.board:
        assert len(alist) == board.width
    assert len(board.coordinates) == board.width*board.height
    assert len(board.mines_coordinates) == board.mines
    assert board.set_cellinformations() == board.width*board.height
    for coordinate in board.mines_coordinates:
        assert coordinate in board.coordinates
        assert board.coordinates.index(coordinate) < board.width*board.height
        assert board.cell_informations[board.coordinates.index(coordinate)][0] == True

def test_board_2():
    board = game.Game()
    assert len(board.board) == board.height
    for alist in board.board:
        assert len(alist) == board.width
    assert len(board.coordinates) == board.width*board.height
    assert len(board.mines_coordinates) == board.mines
    assert board.set_cellinformations() == board.width*board.height
    for coordinate in board.mines_coordinates:
        assert coordinate in board.coordinates
        assert board.coordinates.index(coordinate) < board.width*board.height
        assert board.cell_informations[board.coordinates.index(coordinate)][0] == True

def test_board_3():
    board = game.Game(100, 100, 100)
    assert len(board.board) == board.height
    for alist in board.board:
        assert len(alist) == board.width
    assert len(board.coordinates) == board.width*board.height
    assert len(board.mines_coordinates) == board.mines
    assert board.set_cellinformations() == board.width*board.height
    for coordinate in board.mines_coordinates:
        assert coordinate in board.coordinates
        assert board.coordinates.index(coordinate) < board.width*board.height
        assert board.cell_informations[board.coordinates.index(coordinate)][0] == True

def test_game_1():
    board = game.Game.load('test_game_1.txt')
    assert board.uncover((5, 1)) == 'Move O.K!'
    assert board.uncover((5, 1)) == 'Not allowed!'
    assert board.set_flag((5, 1)) == 'Cell already uncovered!'
    assert board.set_flag((4, 2)) == 'Flag set!'
    assert board.unset_flag((4, 2)) == 'Flag unset!'
    assert board.unset_flag((1, 5)) == 'No flag on coordinate!'
    assert board.uncover((4, 1)) == 'Move O.K!'
    assert board.uncover((5, 2)) == 'Move O.K!'
    assert board.uncover((5, 3)) == 'Move O.K!'
    assert board.uncover((5, 4)) == 'You win!'

def test_game_1_a():
    board = game.Game.load('test_game_1.txt')
    assert board.uncover((1, 5)) == 'Booooooom! - Game over!'

def test_game_2():
    board = game.Game.load('test_game_2.txt')
    assert board.unset_flag((5, 4)) == 'Flag unset!'
    assert board.unset_flag((10, 1)) == 'No flag on coordinate!'
    assert board.set_flag((5, 4)) == 'Flag set!'
    assert board.set_flag((5, 1)) == 'Cell already uncovered!'
    assert board.uncover((5, 1)) == 'Not allowed!'
    assert board.uncover((6, 1)) == 'Move O.K!'
    assert board.uncover((7, 1)) == 'Move O.K!'
    assert board.uncover((8, 1)) == 'Move O.K!'
    assert board.uncover((10, 1)) == 'Move O.K!'
    assert board.uncover((7, 9)) == 'Move O.K!'
    assert board.uncover((6, 8)) == 'You win!'

def test_game_2_a():
    board = game.Game.load('test_game_2.txt')
    assert board.uncover((7, 10)) == 'Booooooom! - Game over!'
   
    