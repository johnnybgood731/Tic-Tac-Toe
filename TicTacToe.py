# TicTacToe is a game of tic tac toe that a player may play against my brute force AI which never loses.
# While brute force is not the most efficient method of programming tic tac toe, I wanted practice with
# programming a brute force algorithm.  One improvement I would like to make is to have the computer
# identify whether a move forces a cat's game and avoid doing so when possible.

# The board indexes in a spiral in case I ever want to check for rotational symmetry
def printBoard(board):
    print("")
    print("")
    print(board[0] + "|" + board[1] + "|" + board[2])
    print("-----")
    print(board[7] + "|" + board[8] + "|" + board[3])
    print("-----")
    print(board[6] + "|" + board[5] + "|" + board[4])
    print("")
    print("")


def checkWin(board):
    if board[0] == board[1] and board[0] == board[2]:
        return board[0]
    if board[7] == board[8] and board[7] == board[3]:
        return board[7]
    if board[6] == board[5] and board[6] == board[4]:
        return board[6]
    if board[0] == board[7] and board[0] == board[6]:
        return board[0]
    if board[1] == board[8] and board[1] == board[5]:
        return board[1]
    if board[2] == board[3] and board[2] == board[4]:
        return board[2]
    if board[0] == board[8] and board[0] == board[4]:
        return board[0]
    if board[6] == board[8] and board[6] == board[2]:
        return board[6]
    for x in range(9):
        if board[x] != "X" and board[x] != "O":
            return ""
    return "Cats"


def takePlayerTurn():
    global player
    printBoard(gameBoard)
    pMove = 0
    tempFlag = False
    while int(pMove) < 1 or int(pMove) > 9:
        try:
            pMove = int(input("Which space would you like to choose? "))
        except ValueError:
            print("Please answer only with a whole number between 1 and 9!")
            tempFlag = True
        if (pMove < 1 or pMove > 9) and not tempFlag:
            print("Please answer only with a whole number between 1 and 9!")
        elif 0 < pMove < 10:
            try:
                gameBoard[gameBoard.index(str(pMove))] = player
            except ValueError:
                print("That space has already been chosen! Please choose a different space.")
                pMove = 0
        tempFlag = False
    printBoard(gameBoard)


def takeComputerTurn():
    global player
    global computer

    # We need to reset our decision path each time the computer takes a new move
    possChoices = []

    # Generate a list of possible moves and store them in possChoices
    for x in gameBoard:
        if x != "X" and x != "O":
            possChoices += [x]

    # resultsX is going to store the current best move on the back end of each for loop.  Once resultsX is fully
    # populated, it will be used to determine if the first move results in a win, loss, or draw, and that final
    # result will be stored in results so that resultsX can be reused for the next move.
    results = [""] * len(possChoices)
    resultsX = [""] * len(possChoices)

    # Here starts the nested for loops.  Within each loop, we will choose the next available move out of all possible
    # choices, populate that move into a temporary copy of the actual game board, check to see if that move ends the
    # game, and if so, break from that particular loop after updating either the results or resultsX array.
    for move1 in possChoices:
        break1 = False
        resultsIndex = possChoices.index(move1)  # This variable isn't necessary, just makes the code less confusing
        tempBoard = list(gameBoard)  # For each new 1st move, we need to reset the tempBoard to avoid a false early win
        tempBoard[gameBoard.index(move1)] = computer  # computer is either "X" or "O" depending on who went first
        if checkWin(tempBoard) == computer:  # We don't check for a loss because the computer can't lose after moving
            results[resultsIndex] = "Win"
            break1 = True  # Creating this boolean allows us to avoid calling the checkWin function again later
        elif checkWin(tempBoard) == "Cats":
            results[resultsIndex] = "Cats"
        for i in range(len(possChoices) - 1):  # We are considering a new first move, so previous results don't apply
            resultsX[i] = ""
        # We are not ever going to break the outermost loop because we will consider all possible moves even if we
        # have already found a winning move, because we don't want the computer to do the same thing every time
        # ---------------------------------------------------------------------------------------------------------
        for move2 in possChoices:
            if len(possChoices) < 2:
                break
            # This goes here because we would want to break the move2 loop, not the move1 loop
            if break1:
                break
            if resultsX[0] == "Loss":
                break
            if move2 == move1:  # You can't choose a square that's already been chosen
                continue
            tempBoard2 = list(tempBoard)  # For each new 2nd move, we need to reset the tempBoard to its original state
            tempBoard2[gameBoard.index(move2)] = player  # player is either "X" or "O" depending on who went first
            if checkWin(tempBoard2) == player:  # We don't check for a win because the computer can't win after
                resultsX[0] = "Loss"            # the player's move
                break  # From here on we are okay with breaking right away because we wouldn't consider other moves
            if checkWin(tempBoard2) == "Cats":
                resultsX[0] = "Cats"  # "Cats" should never replace "Loss", but "Loss" results in a break @ line 105
            for i in range(len(possChoices) - 2):    # We are considering a new second move,
                resultsX[i+1] = ""                  # so the previous results of moves 3-9 do not apply
            # ------------------------------------------------------------------------------------------------------
            for move3 in possChoices:
                if len(possChoices) < 3:
                    break
                if resultsX[1] == "Win":
                    break
                if move3 == move1 or move3 == move2:
                    continue
                tempBoard3 = list(tempBoard2)  # The pattern continues -- Again, we need to reset the tempBoard
                tempBoard3[gameBoard.index(move3)] = computer
                if checkWin(tempBoard3) == computer:
                    resultsX[1] = "Win"
                    break
                if checkWin(tempBoard3) == "Cats":
                    resultsX[1] = "Cats"  # "Cats" should never replace "Win", but "Win" results in a break @ line 120
                for i in range(len(possChoices) - 3):  # The pattern continues -- Again, previous results are now n/a
                    resultsX[i+2] = ""
                # --------------------------------------------------------------------------------------------------
                for move4 in possChoices:
                    if len(possChoices) < 4:
                        break
                    if resultsX[2] == "Loss":
                        break
                    if move4 == move1 or move4 == move2 or move4 == move3:
                        continue
                    tempBoard4 = list(tempBoard3)
                    tempBoard4[gameBoard.index(move4)] = player
                    if checkWin(tempBoard4) == player:
                        resultsX[2] = "Loss"
                        break
                    if checkWin(tempBoard4) == "Cats":
                        resultsX[2] = "Cats"
                    for i in range(len(possChoices) - 4):
                        resultsX[i+3] = ""
                    # -----------------------------------------------------------------------------------------------
                    for move5 in possChoices:
                        if len(possChoices) < 5:
                            break
                        if resultsX[3] == "Win":
                            break
                        if move5 == move1 or move5 == move2 or move5 == move3 or move5 == move4:
                            continue
                        tempBoard5 = list(tempBoard4)
                        tempBoard5[gameBoard.index(move5)] = computer
                        if checkWin(tempBoard5) == computer:
                            resultsX[3] = "Win"
                            break
                        if checkWin(tempBoard5) == "Cats":
                            resultsX[3] = "Cats"
                        for i in range(len(possChoices) - 5):
                            resultsX[i+4] = ""
                        # -------------------------------------------------------------------------------------------
                        for move6 in possChoices:
                            if len(possChoices) < 6:
                                break
                            if resultsX[4] == "Loss":
                                break
                            if move6 == move1 or move6 == move2 or move6 == move3 or move6 == move4 or move6 == move5:
                                continue
                            tempBoard6 = list(tempBoard5)
                            tempBoard6[gameBoard.index(move6)] = player
                            if checkWin(tempBoard6) == player:
                                resultsX[4] = "Loss"
                                break
                            if checkWin(tempBoard6) == "Cats":
                                resultsX[4] = "Cats"
                            for i in range(len(possChoices) - 6):
                                resultsX[i+5] = ""
                            # ---------------------------------------------------------------------------------------
                            for move7 in possChoices:
                                if len(possChoices) < 7:
                                    break
                                if resultsX[5] == "Win":
                                    break
                                if (move7 == move1 or move7 == move2 or move7 == move3 or move7 == move4 or
                                        move7 == move5 or move7 == move6):
                                    continue
                                tempBoard7 = list(tempBoard6)
                                tempBoard7[gameBoard.index(move7)] = computer
                                if checkWin(tempBoard7) == computer:
                                    resultsX[5] = "Win"
                                    break
                                if checkWin(tempBoard7) == "Cats":
                                    resultsX[5] = "Cats"
                                for i in range(len(possChoices) - 7):
                                    resultsX[i+6] = ""
                                # -----------------------------------------------------------------------------------
                                for move8 in possChoices:
                                    if len(possChoices) < 8:
                                        break
                                    if resultsX[6] == "Loss":
                                        break
                                    if (move8 == move1 or move8 == move2 or move8 == move3 or move8 == move4 or
                                            move8 == move5 or move8 == move6 or move8 == move7):
                                        continue
                                    tempBoard8 = list(tempBoard7)
                                    tempBoard8[gameBoard.index(move8)] = player
                                    if checkWin(tempBoard8) == player:
                                        resultsX[6] = "Loss"
                                        break
                                    if checkWin(tempBoard8) == "Cats":
                                        resultsX[6] = "Cats"
                                    for i in range(len(possChoices) - 8):
                                        resultsX[7] = ""
                                    # -------------------------------------------------------------------------------
                                    for move9 in possChoices:
                                        if len(possChoices) < 9:
                                            break
                                        if (move9 == move1 or move9 == move2 or move9 == move3 or move9 == move4 or
                                                move9 == move5 or move9 == move6 or move9 == move7 or move9 == move8):
                                            continue
                                        tempBoard8[gameBoard.index(move9)] = computer
                                        if checkWin(tempBoard8) == computer and resultsX[7] != "Cats":
                                            resultsX[7] = "Win"  # "Win" should not replace "Cats"
                                        elif checkWin(tempBoard8) == "Cats":
                                            resultsX[7] = "Cats"  # "Cats" should replace "Win"
                                        break
                                    # Continuation of the move8 for loop
                                    if resultsX[7] == "Win" and resultsX[6] == "":
                                        resultsX[6] = "Win"  # "Win" should not replace "Cats" or "Loss"
                                    if resultsX[7] == "Cats" and resultsX[6] != "Loss":
                                        resultsX[6] = "Cats"  # "Cats" should replace "Win", but not "Loss"
                                # Continuation of the move7 for loop
                                if resultsX[6] == "Loss" and resultsX[5] == "":
                                    resultsX[5] = "Loss"  # "Loss" should not replace "Cats" or "Win"
                                elif resultsX[6] == "Cats" and resultsX[5] != "Win":
                                    resultsX[5] = "Cats"  # "Cats" should replace "Loss", but not "Win"
                                elif resultsX[6] == "Win":
                                    resultsX[5] = "Win"  # "Win" should replace "Loss" and "Cats"
                            # Continuation of the move6 for loop
                            if resultsX[5] == "Win" and resultsX[4] == "":
                                resultsX[4] = "Win"  # The pattern continues for all even numbered loops
                            elif resultsX[5] == "Cats" and resultsX[4] != "Loss":
                                resultsX[4] = "Cats"
                            elif resultsX[5] == "Loss":
                                resultsX[4] = "Loss"  # "Loss" should replace "Win" and "Cats"
                        # Continuation of the move5 for loop
                        if resultsX[4] == "Loss" and resultsX[3] == "":
                            resultsX[3] = "Loss"  # The pattern continues for all odd numbered loops
                        elif resultsX[4] == "Cats" and resultsX[3] != "Win":
                            resultsX[3] = "Cats"
                        elif resultsX[4] == "Win":
                            resultsX[3] = "Win"
                    # Continuation of the move4 for loop
                    if resultsX[3] == "Win" and resultsX[2] == "":
                        resultsX[2] = "Win"
                    elif resultsX[3] == "Cats" and resultsX[2] != "Loss":
                        resultsX[2] = "Cats"
                    elif resultsX[3] == "Loss":
                        resultsX[2] = "Loss"
                # Continuation of the move3 for loop
                if resultsX[2] == "Loss" and resultsX[1] == "":
                    resultsX[1] = "Loss"
                elif resultsX[2] == "Cats" and resultsX[1] != "Win":
                    resultsX[1] = "Cats"
                elif resultsX[2] == "Win":
                    resultsX[1] = "Win"
            # Continuation of the move2 for loop
            if resultsX[1] == "Win" and resultsX[0] == "":
                resultsX[0] = "Win"
            elif resultsX[1] == "Cats" and resultsX[0] != "Loss":
                resultsX[0] = "Cats"
            elif resultsX[1] == "Loss":
                resultsX[0] = "Loss"
        # Continuation of the move1 for loop
        if resultsX[0] == "Loss":
            results[resultsIndex] = "Loss"
        elif resultsX[0] == "Cats":
            results[resultsIndex] = "Cats"
        elif resultsX[0] == "Win":
            results[resultsIndex] = "Win"

    # At this point, all of the for loops are done, and results[] is populated with the true end results of each move
    from random import randint
    randWin = []  # Will store all winning moves
    randCats = []  # Will store all moves which end in a cat's-game
    randLoss = []  # Will store all losing moves
    for moves in range(len(results)):
        if results[moves] == "Win":
            randWin += [possChoices[moves]]
        elif results[moves] == "Cats":
            randCats += [possChoices[moves]]
        elif results[moves] == "Loss":
            randLoss += [possChoices[moves]]
    if len(randWin) > 0:
        gameBoard[gameBoard.index(randWin[randint(0, len(randWin) - 1)])] = computer  # Makes a random winning move
    elif len(randCats) > 0:
        gameBoard[gameBoard.index(randCats[randint(0, len(randCats) - 1)])] = computer  # Makes a random cat's game move
    elif len(randLoss) > 0:  # Theoretically this would never happen
        gameBoard[gameBoard.index(randLoss[randint(0, len(randLoss) - 1)])] = computer  # Makes a random losing move


gameEnd = False
playAgain = True
while playAgain:
    gameBoard = ["1", "2", "3", "6", "9", "8", "7", "4", "5"]
    msg = ""
    computersTurn = False
    playerTurn = ""

    while playerTurn.lower() != "y" and playerTurn.lower() != "n":
        playerTurn = input("Would you like to go first (Y/N)? ")
        if playerTurn.lower() != "y" and playerTurn.lower() != "n":
            print("Please answer only with \"Y\" or \"N\"!")

    if playerTurn.lower() == "y":
        player = "X"
        computer = "O"
        takePlayerTurn()
        computersTurn = True
    else:
        computer = "X"
        player = "O"
        takeComputerTurn()

    while checkWin(gameBoard) == "":
        if computersTurn:
            takeComputerTurn()
            computersTurn = False
        else:
            takePlayerTurn()
            computersTurn = True

    if checkWin(gameBoard) == player:
        printBoard(gameBoard)
        print("Congratulations! You have done the impossible!")     # Theoretically this will never happen
    elif checkWin(gameBoard) == computer:
        printBoard(gameBoard)
        print("Sorry, you lose! Better luck next time!")
    else:
        printBoard(gameBoard)
        print("It's a cat's game!")
    while msg.lower() != "y" and msg.lower() != "n":
        msg = input("Would you like to play again (Y/N)? ")
        if msg.lower() != "y" and msg.lower() != "n":
            print("Please answer only with \"Y\" or \"N\"!")
        if msg.lower() == "n":
            playAgain = False
            print("Thank you for playing! Goodbye.")
