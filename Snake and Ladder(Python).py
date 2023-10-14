import random
import os
import platform
import collections

def find_shortest_path(board,boards,start, end,players_position,player_num):
    queue = collections.deque([(start, [start])])
    visited = set()
    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        for roll in range(1, 7):
            next_cell = current + roll
            if next_cell <= end and next_cell not in visited and next_cell!=0:
                visited.add(next_cell)
                # Check if the next cell has a ladder or a snake
                if ",LT" in board[boards[next_cell][0]][boards[next_cell][1]]:
                    row,column=players_position[player_num][0],players_position[player_num][1]
                    cell_content = board[row][column]
                    if ",LT" in cell_content:
                        ladder_tail_num = int(cell_content.split(",LT")[1][0])
                    else:
                        ladder_tail_num = 0
                    lhr=lhc=-1
                    for i in range(len(board)):#finding the head of the ladder
                        for j in range(len(board)):
                            if(f",LH{ladder_tail_num}" in board[i][j]):
                                lhr=i
                                lhc=j
                                break
                    keyj=-1
                    for key, value in boards.items():#retreiving the cell number where the ladder head is found from boards list
                        if value ==[lhr,lhc]:
                            keyj= key  # Return the key when a match is found
                            break
                    next_cell =  keyj# Climb the ladder
                elif ",SH" in board[boards[next_cell][0]][boards[next_cell][1]]:
                    row,column=players_position[player_num][0],players_position[player_num][1]
                    cell_content = board[row][column]
                    if ",SH" in cell_content:
                        ladder_tail_num = int(cell_content.split(",SH")[1][0])
                    else:
                        ladder_tail_num = 0
                    lhr=lhc=-1
                    for i in range(len(board)):#finding the head of the ladder
                        for j in range(len(board)):
                            if(f",ST{ladder_tail_num}" in board[i][j]):
                                lhr=i
                                lhc=j
                                break
                    keyj=-1
                    for key, value in boards.items():#retreiving the cell number where the ladder head is found from boards list
                        if value ==[lhr,lhc]:
                            keyj= key  # Return the key when a match is found
                            break
                    next_cell = keyj  # Avoid the snake
                next_path = path + [next_cell]
                queue.append((next_cell, next_path))
    return None
def main():
    while True:#asking user for the board format eh would like to pefer
        n = int(input("Choose your board size:\n1) 5 X 5\t4) 8 X 8\n2) 6 X 6\t5) 9 X 9\n3) 7 X 7\t6) 10 X 10\n\nYour Board Choice:")) + 4
        if n - 4 < 1 or n - 4 > 6:
            print("\n\nInvalid board size. Please choose a board size between 1 and 6.")
        else:
            break
    board = [["0" for _ in range(n)] for _ in range(n)]
    boards={}
    cell_value = 1
    k=1
    for row in range(n-1,-1,-1):#creating the board
        if k%2==1:
            for col in range(n):
                board[row][col] = str(cell_value)
                boards[cell_value]=[row,col]
                cell_value += 1
                k=0
        else:
            for col in range(n - 1, -1, -1):
                board[row][col] = str(cell_value)
                boards[cell_value]=[row,col]
                cell_value += 1
                k=1
    position_ladders_snakes(board,generate_random_snakes_ladders(board),"S")
    position_ladders_snakes(board,generate_random_snakes_ladders(board),"L")
    while True:#taking number of player playing the game
        num_players = int(input("\nEnter the number of players: "))
        if num_players>0:
            break
        else:
            print("Please enter valid number of players playing the game")
    players_position = {}
    players=[[0],]
    bonus_chance=[0]
    for player_num in range(1, num_players + 1):#creating list of players playing and bonus available to them
        players_position[player_num]=[-1,-1]
        bonus_chance.append(0)
        players.append([0])
    basic_display(board, players_position,players,bonus_chance)
    board_size=len(board)
    
    
    
    input("\t\tPRESS ENTER TO START THE GAME:")
    current_platform = platform.system()
    if current_platform == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    over=1
    k=-1
    while True:#running every player turn
        for player_num in range(1,num_players+1):
            #checking if player is placed outside the board
            if(players_position[player_num][0]==-1):
                dice_roll=random.randint(1, 6)
                print(f"Player {player_num} got a {dice_roll}")
                if(dice_roll==1 or dice_roll==6):
                    print(f"Congratulations Player {player_num} you have entered the board")
                    players[player_num].append(1)
                    players_position[player_num]=[board_size-1,0]
                    board[players_position[player_num][0]][players_position[player_num][1]]+=f",P{player_num}"
                    current_cell = board[players_position[player_num][0]][players_position[player_num][1]]
                    basic_display(board,players_position,players,bonus_chance)
                    if("LT" in current_cell):#checking if ladder is present in that cell
                        print("Double Congratulations you had landed on a ladder")
                        ladder_found(player_num,players_position,players,board,boards,bonus_chance)
                        bonus_chance[player_num]+=1
                else:
                    print("Oops it was neither a 6 nor a 1. Better Luck next time!")
                    basic_display(board,players_position,players,bonus_chance)
            #checking if player is inside the board
            else:
                k=inside_board(player_num,players,players_position,board,boards,bonus_chance)
            if(k==-1):
                refresh_console(player_num,players)
            if(k!=-1):
                basic_display(board,players_position,players,bonus_chance)  
                print(f"\t\tCongratulations Player {k} You won the game")
                over=0
                break
        if(over==0):
            break
def inside_board(player_num,players,players_position,board,boards,bonus_chance):
    dice_roll=random.randint(1, 6)
    print(f"Player {player_num} got a {dice_roll}")
    new_position = players[player_num][-1] + dice_roll
    if(dice_roll==1 and new_position==(1+len(board)*len(board))):
        return player_num
    elif not(new_position <= len(board) ** 2):
        print(f"Player {player_num} token will go out of bounds,\nPlayer {player_num} please wait at cell {players[player_num][-1]} till your next move") 
        bonus_chance[player_num]=0
        basic_display(board,players_position,players,bonus_chance)
    else:
        if(dice_roll==6):
            print("WOOHOO you got a 6, You will get a bonus chance for this")
            bonus_chance[player_num]+=1
        print(f"Player {player_num} advances from cell {players[player_num][-1]}  to cell {new_position}")
        board[boards[players[player_num][-1]][0]][boards[players[player_num][-1]][1]]=board[boards[players[player_num][-1]][0]][boards[players[player_num][-1]][1]].replace(f",P{player_num}","")
        players[player_num].append(new_position)
        players_position[player_num][0],players_position[player_num][1]=boards[new_position][0],boards[new_position][1]
        board[boards[new_position][0]][boards[new_position][1]]+=f",P{player_num}"
        current_cell = board[players_position[player_num][0]][players_position[player_num][1]]
        basic_display(board,players_position,players,bonus_chance)
        if("LT" in current_cell):#checking if ladder is present in that cell
            print("\n\n\n\n\n\n\n\n\n\n\nCongratulations you had landed on a ladder\nYou will receive a Bonus chance for this")
            bonus_chance[player_num]+=1
            ladder_found(player_num,players_position,players,board,boards,bonus_chance)
        if("SH" in current_cell):
            print("\n\n\n\n\n\n\n\n\n\n\n!!!!    Oh No you landed on a snake    !!!!")
            bonus_chance[player_num]=0
            snake_found(player_num,players_position,players,board,boards,bonus_chance)
    if(bonus_chance[player_num]>3):
        print("!!!!    Oh No you have excede the limit of receiving bonus chances so all bonus chances you earned are now cancelled    !!!!")
    while(bonus_chance[player_num]!=0):
        print("\n\n\n\n\n\n\n\n\n\n\nLets use your bonus chances")
        input(f"Player {player_num} Press Enter to roll the dice again")
        bonus_chance[player_num]-=1
        inside_board(player_num,players,players_position,board,boards,bonus_chance)
    start=players[player_num][-1]
    end=len(board)*len(board)
    shortest_path = find_shortest_path(board,boards,start, end,players_position,player_num)
    if shortest_path:
        print("Shortest Path:", shortest_path)
        print("Number of Moves:", len(shortest_path) - 1)
        print("Next dice move required to land on shortest path:",(shortest_path[1]-shortest_path[0]))
    else:
        print("No path found.")
    return -1
def snake_found(player_num,players_position,players,board,boards,bonus_chance):
    row,column=players_position[player_num][0],players_position[player_num][1]
    cell_content = board[row][column]
    ladder_tail_num = int(str(cell_content).split(",SH")[1][0])
    print(ladder_tail_num)
    lhr=-1
    lhc=-1
    for i in range(len(board)):#finding the head of the ladder
        for j in range(len(board)):
            if(f",ST{ladder_tail_num}" in board[i][j]):
                lhr=i
                lhc=j
                break
    board[boards[players[player_num][-1]][0]][boards[players[player_num][-1]][1]]=board[players_position[player_num][0]][players_position[player_num][1]].replace(f",P{player_num}","")
    keyj=-1
    for key, value in boards.items():
        if value ==[lhr,lhc]:
            keyj= key  # Return the key when a match is found
            break
    print(f"You move from cell {players[player_num][-1]} to cell {keyj}")
    players[player_num].append(keyj)
    players_position[player_num][0],players_position[player_num][1]=lhr,lhc
    board[players_position[player_num][0]][players_position[player_num][1]]+=f",P{player_num}" 
    basic_display(board,players_position,players,bonus_chance)   
def ladder_found(player_num,players_position,players,board,boards,bonus_chance):
    row,column=players_position[player_num][0],players_position[player_num][1]
    cell_content = board[row][column]
    ladder_tail_num = int(str(cell_content).split(",LT")[1][0])
    lhr=-1
    lhc=-1
    for i in range(len(board)):#finding the head of the ladder
        for j in range(len(board)):
            if(f",LH{ladder_tail_num}" in board[i][j]):
                lhr=i
                lhc=j
                break
    board[boards[players[player_num][-1]][0]][boards[players[player_num][-1]][1]]=board[players_position[player_num][0]][players_position[player_num][1]].replace(f",P{player_num}","")
    keyj=-1
    for key, value in boards.items():
        if value ==[lhr,lhc]:
            keyj= key  # Return the key when a match is found
            break
    print(f"You move from cell {players[player_num][-1]} to cell {keyj}")
    players[player_num].append(keyj)
    players_position[player_num][0],players_position[player_num][1]=lhr,lhc
    board[players_position[player_num][0]][players_position[player_num][1]]+=f",P{player_num}" 
    basic_display(board,players_position,players,bonus_chance)    
def position_ladders_snakes(board,num,ls):
    board_size = len(board)
    for ladder_num in range(1, num + 1):
        while True:
            head_row = random.randint(0, board_size - 2)
            tail_row = random.randint(head_row + 1, board_size - 1)
            head_col = random.randint(0, board_size - 1)
            possible_tail_cols = [col for col in range(board_size) if col != head_col]
            tail_col = random.choice(possible_tail_cols)
            # Calculate the head position
            head_position = head_row * board_size + head_col
            # Ensure that the head and tail positions are different and the head position is within the allowed range
            if (head_row, head_col) != (tail_row, tail_col) and 1 <= head_position <= board_size * board_size - 1 and  len(board[head_row][head_col])<=2 and len(board[tail_row][tail_col])<=2:
                break
        board[head_row][head_col] += f",{ls}H{ladder_num}"
        board[tail_row][tail_col] += f",{ls}T{ladder_num}"
def refresh_console(player_num,players):#clears the console
    k=player_num+1
    if(len(players)==player_num+1):
        k=1
    input(f"\nPlayer {k} Press Enter to roll your dice...")
    current_platform = platform.system()
    if current_platform == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
def basic_display(board, players_position,players,bonus_chance):
    num_players = len(players_position)
    for i in range(len(board)):#for normally printing the board
        print("\t", end="")
        for j in range(len(board[0])):
            print(board[i][j], end="\t")
        print("\n")
    print("\nPlayers still outside the board:")
    for player_num in range(1,num_players+1):# for diplaying the players token which have still not entered the board
        if(players_position[player_num][0]==-1):
            if i != num_players - 1:
                print(f"P{player_num},", end=" ")
    print("\n")
    for i, j in enumerate(players):
        if(i!=0):
            print(f"Player {i}: {j}\t")
    print("\n\n")
    print("Players bonus available:\t")# to show bonusses claimed by the players by landing on a ldder or getting a 6
    for i, bonus in enumerate(bonus_chance):
        if(i!=0):
            print(f"Player {i}: {bonus}\t", end="")
    print("\n\n")
def generate_random_snakes_ladders(board):
    board_size = len(board)
    if board_size == 5:
        return random.randint(1, 2)
    elif board_size == 6:
        return random.randint(2, 4)
    elif board_size == 7:
        return random.randint(3, 5)
    elif board_size == 8:
        return random.randint(4, 6)
    elif board_size == 9:
        return random.randint(5, 7)
    elif board_size == 10:
        return random.randint(6, 8)
if __name__ == "__main__":
    main()