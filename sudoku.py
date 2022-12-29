import time, sys, random
global moves

holding_board = [] # holds the inital numbers and their positions on the board

moves = 0 # amount of moves it takes to complete the sudoku

def print_board(sudoku):
    for i in range(9):
        print(sudoku[i][0:3],'|',sudoku[i][3:6],'|',sudoku[i][6:9])
        if i==5 or i==2:
            print('-'*51)

#allows the player to select what mode they want to run
def menu(sudoku):
    clear_board(sudoku) # clears the board

    start_time = time.time() # records the start time of the program

    player_mode = str(input("what mode do you want to play? human or computer: "))
    if player_mode == "human":
        human_play(sudoku, start_time)
    else:
        times_ran =+1
        computer_play(sudoku, start_time)

#keeps a list of all the numbers in the board so it can be re-set when the board is completed
def record_inital_board(sudoku):
    for row in range(0,9):
        for column in range(0,9):
            if sudoku[row][column] != " ":
                value = [sudoku[row][column], row, column]
                holding_board.append(value)

# clears the board if a new game is started
def clear_board(sudoku):
    #sets every item in the board to blank
    for row in range(0,9):
        for column in range(0,9):
            update_board(sudoku, row, column, " ")

    # puts every original value back into the board
    for item in range(len(holding_board)-1):
        number = str(holding_board[item][0])
        row = int(holding_board[item][1])
        column = int(holding_board[item][2])
        update_board(sudoku, row, column, number)

#updates the board every time it is changed
def update_board(sudoku, row, column, input):
    sudoku[int(row)][int(column)] = str(input)

#allows the player to manually add numbers into the sudoku board
def human_play(sudoku, start_time):
    inputted_values =[] # keeps track of all the numbers the player inputs
    errors = 0 # counts the amount of errors in the code

    #allows the player to input numbers
    def user_input(moves):

        row_input = str(input("what row do you want to add to: "))
        column_input = str(input("what column do you want to add to: "))

        #validation - only allows rows and columns to be within the boundries of the sudoku board
        if int(row_input) > 8 or int(row_input) < 0:
            print("numbers must be between 1 and 9")
        elif int(column_input) > 8 or int(column_input) < 0:
            print("numbers must be between 1 and 9")
        #validation - only allows you to put a number if that space has not been taken    
        elif sudoku[int(row_input)][int(column_input)] != " ":
            print("that space is already taken")
        else:
            number_input = str(input("what number do you want to put: "))
            check_if_valid = is_valid(sudoku, number_input, row_input, column_input)
            # if the placed number is invalid, it is recorded as invalid
            if check_if_valid == False:
                errors = 1
            else:
                errors = 0

            value_added = [[row_input, column_input], number_input, errors]
            inputted_values.append(value_added)
            update_board(sudoku, row_input, column_input, number_input)
            moves += 1
            print(inputted_values)

    #allows the player to delete numbers they have inputted
    def delete_input():

        delete_row = str(input("what row do you want to delete from: "))
        delete_column = str(input("what column do you want to delete from: "))

        #validation - only allows numbers from 1 to 9 to be entered
        if int(delete_row) > 8 or int(delete_row) < 0:
            print("numbers must be between 1 and 9")
        elif int(delete_column) > 8 or int(delete_column) < 0:
            print("numbers must be between 1 and 9")
        else:
            delete_value = [delete_row, delete_column]
            if inputted_values == []: # checks if the table is empty, therefore no items to delete
                print("no numbers to delete")
            else:
                for i in range(len(inputted_values)):
                    found = False
                    comparing_array = inputted_values[i-1][0] # checks if the coordinates match
                    if comparing_array[0] == delete_value[0] and comparing_array[1] == delete_value[1]:
                        inputted_values.pop(i) # removes the value from the array as it is removed from the board
                        update_board(sudoku, delete_row, delete_column, " ")
                        found = True
                if found == False:
                    print("number has not been added to this place")
                else:
                    print("number deleted")

    game_complete = game_state(sudoku, inputted_values, 1)

    while game_complete == False:
        print_board(sudoku)
        action = str(input("do you want to add or delete: "))
        if action == "add":
            user_input(moves)
        elif action == "delete":
            delete_input()
        else:
            print("invalid input")

    if game_complete == True:
        end_game(sudoku, 1, start_time)

#allows the computer to solve the sudoku using backtracking
def computer_play(sudoku, start_time):

    #finds the next empty space in the grid
    def find_empty_space(sudoku):
        for row in range(0,9):
            for column in range(0,9):
                if sudoku[row][column] == " ":
                    return(row, column)

    #passes in numbers until the inputs are valid and the board is full
    def solve_sudoku(sudoku):
        empty = find_empty_space(sudoku)
        #if its empty, it'll put a number, else it checks the next space
        if not empty:
            return sudoku
        else:
            row, column = empty
            for num in range(1, 10):
                if is_valid(sudoku, num, row, column):
                    update_board(sudoku, row, column, num)

                    if solve_sudoku(sudoku):
                        return sudoku
                    
                    update_board(sudoku, row, column, " ")
        return False

    solve_sudoku(sudoku)
    print_board(sudoku)
    end_game(sudoku, 0, start_time)

# used to check if the number being added follows the rules of sudoku
def is_valid(sudoku, number_input, row, column):
    valid = True
    while valid == True:
        #checks column for repeated numbers
        for i in range(0,9):
            if sudoku[i][int(column)] == str(number_input):
                valid = False
                    
        #checks row for repeated numbers
        for j in range(0,9):
            if sudoku[int(row)][j] == str(number_input):
                valid = False
                    
        #check 3x3 for repeated numbers
        start_row = int(row) - int(row % 3)
        start_column = int(column) - int(column % 3)
        for i in range(3):
            for j in range(3):
                if sudoku[i + start_row][j + start_column] == str(number_input):
                    valid = False
        break
    return valid
    
#runs when the game has finished to display stats of the game
def end_game(sudoku, is_player, start_time):
    if is_player == 1:
        print("This sudoku took", moves, "moves to complete")

    print("the CPU runtime for this program is:", time.time() - start_time, "seconds")
    restart_game = str(input("do you want to play again? "))
    if restart_game == "yes":
        menu(sudoku)
    else:
        sys.exit()

# checks if the game has ended
def game_state(sudoku, inputted_values, is_player):
    errors = 0
    if is_player == 1:
        for value in inputted_values: # counts how many errors were recorded
            if value[3] == 1:
                errors += 1

    grid_full = True
    #checks the whole board for missing values
    for i in range(0,8):
        for j in range(0,8):
            for element in sudoku[i][j]:
                if element == " ":
                    grid_full = False

    if grid_full == True:
        if errors >= 1:
            print("You failed the sudoku with", errors, "errors")
        else:
            print("Congratulations you won !!!")

    return grid_full
    

    
if __name__ == '__main__':

    # Don't change the layout of the following sudoku examples
    sudoku1 = [
        [' ', '1', '5', '4', '7', ' ', '2', '6', '9'],
        [' ', '4', '2', '3', '5', '6', '7', ' ', '8'],
        [' ', '8', '6', ' ', ' ', ' ', ' ', '3', ' '],
        ['2', ' ', '3', '7', '8', ' ', ' ', ' ', ' '],
        [' ', ' ', '7', ' ', ' ', ' ', ' ', '9', ' '],
        ['4', ' ', ' ', ' ', '6', '1', ' ', ' ', '2'],
        ['6', ' ', ' ', '1', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '4', ' ', ' ', ' ', '1', ' ', '7'],
        [' ', ' ', ' ', ' ', '3', '7', '9', '4', ' '],
    ]
    sudoku2 = [
        [' ', ' ', ' ', '3', ' ', ' ', ' ', '7', ' '],
        ['7', '3', '4', ' ', '8', ' ', '1', '6', '2'],
        ['2', ' ', ' ', ' ', ' ', ' ', ' ', '3', '8'],
        ['5', '6', '8', ' ', ' ', '4', ' ', '1', ' '],
        [' ', ' ', '2', '1', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '7', '8', ' ', ' ', '2', '5', '4'],
        [' ', '7', ' ', ' ', ' ', '2', '8', '9', ' '],
        [' ', '5', '1', '4', ' ', ' ', '7', '2', '6'],
        ['9', ' ', '6', ' ', ' ', ' ', ' ', '4', '5'],
    ]
    sudoku3 = [
        ['8', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        [' ', ' ', '3', '6', ' ', ' ', ' ', ' ', ' '],
        [' ', '7', ' ', ' ', '9', ' ', '2', ' ', ' '],
        [' ', '5', ' ', ' ', ' ', '7', ' ', ' ', ' '],
        [' ', ' ', ' ', ' ', '4', '5', '7', ' ', ' '],
        [' ', ' ', ' ', '1', ' ', ' ', ' ', '3', ' '],
        [' ', ' ', '1', ' ', ' ', ' ', ' ', '6', '8'],
        [' ', ' ', '8', '5', ' ', ' ', ' ', '1', ' '],
        [' ', '9', ' ', ' ', ' ', ' ', '4', ' ', ' '],
    ]
    sudoku4 = [
        [' ', '4', '1', ' ', ' ', '8', ' ', ' ', ' '],
        ['3', ' ', '6', '2', '4', '9', ' ', '8', ' '],
        [' ', ' ', ' ', ' ', ' ', ' ', ' ', '7', ' '],
        [' ', ' ', ' ', '4', '7', ' ', '2', '1', ' '],
        ['7', ' ', ' ', '3', ' ', ' ', '4', ' ', '6'],
        [' ', '2', ' ', ' ', ' ', ' ', ' ', '5', '3'],
        [' ', ' ', '7', ' ', '9', ' ', '5', ' ', ' '],
        [' ', ' ', '3', ' ', '2', ' ', ' ', ' ', ' '],
        [' ', '5', '4', ' ', '6', '3', ' ', ' ', ' '],
    ]

    # make sure 'option=2' is used in your submission
    option = 2

    if option == 1:
        sudoku = sudoku1
    elif option == 2:
        sudoku = sudoku2
    elif option == 3:
        sudoku = sudoku3
    elif option == 4:
        sudoku = sudoku4
    else:
        raise ValueError('Invalid choice!')

    # add code here to solve the sudoku
    
    record_inital_board(sudoku)
    menu(sudoku)