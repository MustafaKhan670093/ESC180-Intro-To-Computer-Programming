"""Gomoku starter code
You should complete every incomplete function,
and add more functions and variables as needed.

Note that incomplete functions have 'pass' as the first statement:
pass is a Python keyword; it is a statement that does nothing.
This is a placeholder that you should remove once you modify the function.

Author(s): Michael Guerzhoy with tests contributed by Siavash Kazemian.  Last modified: Oct. 26, 2020
"""

def is_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] != " "):
                return False
                break
    return True
    
    
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    next1 = y_end+d_y
    next2 = x_end+d_x
    back1 = y_end-length*d_y
    back2 = x_end-length*d_x
    closedstart = False
    closedend = False
    if(next1 <= len(board)-1 and next2<=len(board) - 1 and next1 >=0 and next2 >= 0):
        if board[next1][next2]!=" ":
            closedend=True
        elif board[next1][next2] == "w" or board[next1][next2] == "b":
            closedend=False
    else:
        closedend = True
    
    if(back1 <= len(board)-1 and back2<=len(board) - 1 and back1 >=0 and back2 >= 0):
        if board[back1][back2]!=" ":
            closedstart=True
        elif board[back1][back2] == "w" or board[back1][back2] == "b":
            closedstart=False
    else:
        closedstart = True
    
    if closedstart == True and closedend == True:
        return "CLOSED"
    elif closedstart == False and closedend == False:
        return "OPEN"
    else:
        return "SEMIOPEN"
    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    current_1 = y_start
    current_2 = x_start
    while(current_1>=0 and current_1<=(len(board)-1) and current_2>=0 and current_2<=len(board)-1):
        color_status = True       
        if (current_1+(length-1)*d_y) >= 0 and (current_1 + (length-1) * d_y) <= (len(board) - 1) and (current_2 + (length-1)*d_x) >= 0 and (current_2 + (length-1)*d_x) <=(len(board) - 1):
            for i in range(length):
                if(board[current_1 + i*d_y][current_2+i*d_x] != col):
                        color_status = False
            ############################ THIS CODE MAKES IT SO THAT IF YOU HAVE: wwww and you are checking for steps of 3, you should return 1 semiopen and NOT 2.
            endcolor = True       #This checks whether the end colours or start colours are different. If they are different from col, it is true
            startcolor = True
            if(current_1+length*d_y) >= 0 and (current_1+length*d_y) <= (len(board) - 1)  and (current_2 + (length)*d_x) >= 0 and (current_2 + (length)*d_x) <=(len(board) - 1):
                if(board[current_1+length*d_y][current_2+length*d_x] == col):
                    endcolor = False
            if(current_1-d_y) >= 0 and (current_1-d_y) <= (len(board) - 1)  and (current_2 - d_x) >= 0 and (current_2 - d_x) <=(len(board) - 1):
                if(board[current_1 - d_y][current_2-d_x] == col):
                    startcolor = False
            ###############################
            if color_status == True:
                if is_bounded(board, current_1 + (length-1)*d_y, current_2 + (length-1)*d_x, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                
                elif is_bounded(board, current_1 + (length-1)*d_y, current_2 + (length-1)*d_x, length, d_y, d_x) == "SEMIOPEN" and endcolor == True and startcolor == True:   #####THESE TRUE STATEMENTS ARE RELATED TO THE PREVIOUS MODIFICATION
                    semi_open_seq_count += 1
        current_1 += d_y
        current_2 += d_x
    return open_seq_count, semi_open_seq_count
    
def detect_rows(board, col, length):
    ####CHANGE ME
    open_seq_count, semi_open_seq_count = 0, 0
    for i in range(len(board)):
        #Vertical checks from x - 0, 7 and y =0.
        a, b = detect_row(board, col, 0, i, length, 1, 0)
        open_seq_count+=a
        semi_open_seq_count += b
        #Horizontal checks from y - 0,7 and x=0
        c, d = detect_row(board, col, i, 0, length, 0, 1)
        open_seq_count+=c
        semi_open_seq_count += d
        #Diagonal-Bottom-Right (RIGHT HALF) checks from x - 0,7 and y = 0 (ONLY COVERS DIAGONALS FROM 0,0  TILL 7,7)
        a, b = detect_row(board, col, 0, i, length, 1, 1)
        open_seq_count+=a
        semi_open_seq_count += b
        #Diagonal Up-Right (LEFT HALF) checks from y - 0,7 and x = 0 (ONLY COVERS DIAGONALS FROM 7,0 TILL 0,7)
        c, d = detect_row(board, col, i, 0, length, -1, 1)
        open_seq_count+=c
        semi_open_seq_count += d
        #Diagonal-Up-Right (RIGHT HALF) checks from x - 0,7 and y = 7 (ONLY COVERS DIAGONALS FROM 0,0  TILL 7,7)
        if(i>0):
            a, b = detect_row(board, col, 7, i, length, -1, 1)
            open_seq_count+=a
            semi_open_seq_count += b
        #Diagonal Bottom-right (LEFT HALF) checks from y - 0, 7 and x = 0 (ONLY COVERS DIAGONALS FROM 1,1 till 7,6)
        if(i>0):
            c, d = detect_row(board, col, i, 0, length, 1, 1)
            open_seq_count+=c
            semi_open_seq_count += d
        
    

    return open_seq_count, semi_open_seq_count
    
def search_max(board):
    move_y = 0
    move_x = 0
    maxscore = -10000
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == " "): 
                # print("Row: " + str(i))
                # print("Column: " + str(j))
                # print("MaxScore: " + str(maxscore))
                #print_board(board)
                board[i][j] = "b"
                tempscore = score(board)
                if tempscore > maxscore:
                    maxscore = tempscore
                    # print(maxscore)
                    # print("max i")
                    # print("max j")
                    move_y = i
                    move_x = j
                board[i][j] = " "
    return move_y, move_x
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def is_win(board):
    full = True
    for i in range(len(board)):
        for j in range(len(board[0])):
            if(board[i][j] == " "): 
                full = False
    a,b = detect_rows(board, "b", 5)
    c,d = detect_rows(board, "w", 5)
    if(full == True):
        return "Draw"
    elif a >= 1 or b >= 1:
        return "Black won"
    elif c >= 1 or d >=1:
        return "White won"
    else:
        return "Continue playing"


def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


  
            
if __name__ == '__main__':
    #play_gomoku(8)
    #test_is_empty()
    #test_is_bounded()
    
    #Test 1 - Figure 1.0
    # board = make_empty_board(8)
    # x = 1; y = 4; d_x = 0; d_y = 1; length = 3
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    # print_board(board)
    # print(is_bounded(board, 6, 1, length, d_y, d_x))
    #Test2 - Figure 2.0
    # board = make_empty_board(8)
    # y = 3; x = 3; d_y = 0; d_x = -1; length = 3
    # put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    # board[3][0] = "w"
    # print_board(board)
    # print(is_bounded(board, 3, 1, length, d_y, d_x))
    #Test 3 - Figure 4.0
    # board = make_empty_board(8)
    # y = 7; x = 2; d_y = -1; d_x = -1; length = 3
    # put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    # print_board(board)
    # print(is_bounded(board, 5, 0, length, d_y, d_x))
    #Test 4 - Figure 5.0
    # board = make_empty_board(8)
    # y = 3; x = 3; d_y = -1; d_x = 1; length = 4
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    # print_board(board)
    # print(is_bounded(board, 0, 6, length, d_y, d_x)) 

    #DETECT ROW TESTS
    #Test 1 - 1 open, 1 semi open.
    # board = make_empty_board(8)
    # x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    # x = 5; y = 5; d_x = 0; d_y = 1; length = 3
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    # print_board(board)
    # print(detect_row(board, "w", 0,x,length,d_y,d_x))
    #Test 2 - Returns Closed aka 0, 0 
    # board = make_empty_board(8)
    # y = 5; x = 0; d_y = 1; d_x = 1; length = 3
    # put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    # print_board(board)
    # print(detect_row(board, "w", 5,0,length,d_y,d_x))
    #Test 3 - checking step sizes of 2 aka length = 2 in detect_row. Returns (0, 2).
    # board = make_empty_board(8)
    # y = 4; x = 1; d_y = 1; d_x = 0; length = 3
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    # print_board(board)
    # print(detect_row(board, "w", 0,1, 2,d_y,d_x))
    #DETECT ROWS TESTS
    #TEST 1 - 1 
    # board = make_empty_board(8)
    # x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    # x = 0; y = 4; d_x = 1; d_y = -1; length = 3; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w") #1 SEMIOPEN DIAGONALS OF LENGTH 3 + 1 OPEN VERTICAL. RETURNS 1,1
    # x = 5; y = 6; d_x = 1; d_y = -1; length = 3; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w") #2 SEMIOPEN DIAGONALS OF LENGTH 3 + 1 OPEN VERTICAL. RETURNS 1,2
    # x = 4; y = 0; d_x = 1; d_y = 1; length = 3; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w") #3 SEMIOPEN DIAGONALS OF LENGTH 3 + 1 OPEN VERTICAL. RETURNS 1,3
    # x = 2; y = 4; d_x = 1; d_y = 1; length = 3; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, 2, "w") #3 SEMIOPEN DIAGONALS OF LENGTH 3 + 2 OPEN VERTICAL. RETURNS 2,3
    # x = 2; y = 7; d_x = 1; d_y = 0; length = 3; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w") #2 SEMIOPEN OF LENGTH 3 + 3 OPEN of length 3. RETURNS 3,2
    # print_board(board)
    # print(detect_rows(board, col, length))
    #TEST CASE 2 - DIFFERENT COLOURS
    # board = make_empty_board(8)
    # x = 0; y = 4; d_x = 1; d_y = -1; length = 3; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    # x = 1; y = 3; d_x = 1; d_y = 1; length = 3; col = 'b'
    # put_seq_on_board(board, y, x, d_y, d_x, length, "b") 
    # print_board(board)
    # print(detect_rows(board, "w", length))
    #GIVEN TEST CASE
    #some_tests()
    # board = make_empty_board(8)
    # x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, length, col)
    # x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    # put_seq_on_board(board, y, x, d_y, d_x, length, col)
    # #board[4][6] = "b"
    # print_board(board)
    # print(search_max(board))
    # #test_search_max()
    # # open_b = {}
    # # semi_open_b = {}
    # # open_w = {}
    # # semi_open_w = {}
    # # for i in range(2, 6):
    # #     open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
    # #     open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
    # # print(open_b)
    # # print(semi_open_b)
    #test_search_max()
    #TEST SEARCH MAX PART 2
    # board = make_empty_board(8)
    # x = 2; y = 1; d_x = 1; d_y = 1; length = 4; col = 'w'
    # put_seq_on_board(board, y, x, d_y, d_x, length, col)
    # x = 0; y = 7; d_x = 1; d_y = 0; length = 3; col = 'b'
    # put_seq_on_board(board, y, x, d_y, d_x, length, col)
    # print_board(board)
    # print(search_max(board))
    play_gomoku(8)