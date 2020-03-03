import pygame
from ChessPieces import *

def WaitUntilInput():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

def TestMovements():
    InitializeBoard(MovementTest)
    TestedPiecesTiles = ["A4", "A4", "C2", "C5", "C5", "C5", "F3", "F3", "F3", "C3", "C3", "D8", "D8", "E8", "E8"]
    Movements = ["B5", "A6", "C4", "C3", "A6", "F2", "G5", "D2", "H2", "F6", "C4", "D6", "E7", "E7", "G7"]
    Answers = [True, False, False, True, False, True, True, False, True, True, False, True, False, True, False]
    Index = 0
    CurrentTest = 0
    PreviousPiece = 0
    AllTestsPassed = True
    for Tile in TestedPiecesTiles:
        Piece = GetPieceInsideTile(Tile)
        if Piece.PieceName != PreviousPiece:
            CurrentTest = 0
        PreviousPiece = Piece.PieceName
        Path = CreateTilePath(Piece, *GetMovement(Piece.Tile, Movements[Index]))
        if not Piece.ValidMove(Path) == Answers[Index]:
            print("[-] {} Test Number {} : Test Failed".format(Piece.PieceName, CurrentTest))
            AllTestsPassed = False
        Index += 1
        CurrentTest += 1
    return AllTestsPassed

def PossibleMovesTesting():
    screen.blit(Board, BoardRect)
    InitializeBoard()

    CorrectTiles = ["D3", "F3", "E3", "E4"]
    TestedPiece = GetPieceInsideTile("E2")
    Results = TestedPiece.GetPossibleMoves()
    PassedTest = True
    FailedTests = 0
    for Movement in Results:
        CorrectMove = False
        if Movement in CorrectTiles:
            CorrectMove = True
        else:
            PassedTest = False
            FailedTests += 1
    if not PassedTest:
        print("[-] PossibleMovesCheck\nCorrect Tiles: {}\nReceived Tile: {}\nAmount of FailedTests: {}".format(CorrectTiles, Results, FailedTests))
    else:
        print("[+] PossibleMovesCheck Passed")
    return PassedTest

def CheckMateTesting():
    Index = 0
    AllPassed = True
    for CheckMateSetup in AllCheckMates:
        Message = "CheckMate" if CorrectResults[Index] is True else "Not Check Mate"
        screen.blit(Board, BoardRect)
        InitializeBoard(CheckMateSetup)
        GetKings()
        Check()
        try:
            IsCheck = CheckMate()
        except:
            IsCheck = False
        if IsCheck == CorrectResults[Index]:
            print("[+] Success With CheckMateSetup {}: {}".format(Index + 1, Message))
        else:
            print("[-] Error With CheckMateSetup {}: {}".format(Index + 1, Message))
            AllPassed = False
        Index += 1
        if Show:
            WaitUntilInput()
        ResetPieces()

def Testing():
    CheckMateStatus = CheckMateTesting()
    MovementsStatus = TestMovements()
    PossibleMovesStatus = PossibleMovesTesting()
    return CheckMateStatus and MovementStatus and PossibleMovesStatus


Position1 = [[Pawn, [], ["D7", "E7", "F7"]], [Tower, ["G8"], ["H8"]], [King, ["E1"], ["E8"]]]

Position2 = [[Pawn, [], ["D7", "E7", "F7"]], [Tower, ["G8"], []], [King, ["E1"], ["E8"]]]

Position3 = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]], [Horse, ["B1", "G1"], ["B8", "G8"]], [Tower, ["A1", "H1"], ["A8", "H8"]], [Bishop, ["C1", "F1"], ["C8", "F8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["D8"]]]

Position4 = [[King, ["D4"], ["H8"]], [Tower, ["B7", "B8"], []]]

Position5 = [[King, ["D4"], ["H8"]], [Tower, ["B7", "A6"], []]]

Position6 = [[Pawn, [], ["C7","D5", "E7", "F7"]], [Bishop, ["B5"], ["C8", "F8"]], [Queen, [], ["D8"]], [King, ["E1"], ["E8"]]]

KingTest = [[King, ["D4"], ["F6"]]]

Position7 = [[Pawn, ["E7"], []], [King, ["E1"], ["E8"]]]

MovementTest = [[Pawn, ["A4", "B2", "C2", "D2", "D3", "F2", "G3", "H3"], ["A7", "B5", "C7", "E6", "F6", "G5", "H7"]], [Horse, ["B1", "F3"], ["B8", "G8"]], [Tower, ["D8", "H1"], ["A8", "H8"]], [Bishop, ["C3", "F1"], ["D6", "F8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["C5"]]]

TowerCheckMate = [[Tower, ["A8"], []], [Pawn, [], ["F7", "G7", "H7"]], [King, ["A2"], ["G8"]]]

AllCheckMates = [Position1, Position2, Position3, Position4, Position5, Position6, Position7,  TowerCheckMate]

PossibleMoves1 = [[Pawn, ["E2"], ["D3", "F3"]]]

CorrectResults = [False, True, False, True, False, False, False, True]

Show = True

if __name__ == "__main__":
    from Chess import *
    if Testing():
        print("[+] All Tests Passed")
    else:
        print("[-] One or More Tests Failed")


