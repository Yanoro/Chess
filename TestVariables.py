from ChessPieces import *


#--------------CheckMateTest Variables--------------------
Position1 = [[Pawn, [], ["D7", "E7", "F7"]], [Tower, ["G1"], ["H8"]], [King, ["E1"], ["E8"]]]

Position2 = [[Pawn, [], ["D7", "E7", "F7"]], [Tower, ["G1"], []], [King, ["E1"], ["E8"]]]

Position3 = [[Pawn, ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"], ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]], [Horse, ["B1", "G1"], ["B8", "G8"]], [Tower, ["A1", "H1"], ["A8", "H8"]], [Bishop, ["C1", "F1"], ["C8", "F8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["D8"]]]

Position4 = [[King, ["D4"], ["H8"]], [Tower, ["B7", "A6"], []]]

Position5 = [[King, ["D4"], ["H8"]], [Tower, ["B7", "A1"], []]]

Position6 = [[Pawn, [], ["C7","D5", "E7", "F7"]], [Bishop, ["D3"], ["C8", "F8"]], [Queen, [], ["D8"]], [King, ["E1"], ["E8"]]]

KingTest = [[King, ["D4"], ["F6"]]]

Position7 = [[Pawn, ["E6"], []], [King, ["E1"], ["E8"]]]

MovementTest = [[Pawn, ["A4", "B2", "C2", "D2", "D3", "F2", "G3", "H3"], ["A7", "B5", "C7", "E6", "F6", "G5", "H7"]], [Horse, ["B1", "F3"], ["B8", "G8"]], [Tower, ["D8", "H1"], ["A8", "H8"]], [Bishop, ["C3", "F1"], ["D6", "F8"]], [King, ["E1"], ["E8"]], [Queen, ["D1"], ["C5"]]]

TowerCheckMate = [[Tower, ["A3"], []], [Pawn, [], ["F7", "G7", "H7"]], [King, ["A2"], ["G8"]]]

LastTest1 = [[Pawn, ["D5", "E3", "F2", "G2"], ["A5", "B6", "F5", "H5"]], [Tower, [], ["C8"]], [Horse, ["D2", "A3"], ["E5"]], [Bishop, [], ["A4", "G5"]], [King, ["E2"], ["D6"]]]

LastTest2 = [[Pawn, ["D5", "E3", "F2", "G2"], ["A5", "B6", "F5", "H5"]], [Tower, [], ["C8"]], [Horse, ["D2", "B5"], ["E5"]], [Bishop, [], ["A4", "G5"]], [King, ["E2"], ["D6"]]]

AllCheckMates = [Position1, Position2, Position3, Position4, Position5, Position6, Position7,  TowerCheckMate]

PossibleTests1 = [[Pawn, ["E2"], ["D3", "F3"]]]

CorrectResults = [False, True, False, True, False, False, False, True]

#--------------MovementTest Variables--------------------

DiagonalMoves = ["A1", "A7", "H8", "G1"]

VerticalAndHorizontalMoves = ["H4", "A4", "D8", "D1"]

WhitePawnTests = [["D5"], DiagonalMoves + VerticalAndHorizontalMoves]
#BlackPawnTests = [["D3"], [DiagonalTests + VerticalAndHorizontalMoves]]

HorseTests = [["E6", "E2", "C6", "C2", "B3", "B5", "F3", "F5"], DiagonalMoves + VerticalAndHorizontalMoves]

BishopTests = [DiagonalMoves, VerticalAndHorizontalMoves]

TowerTests = [VerticalAndHorizontalMoves, DiagonalMoves]

QueenTests = [DiagonalMoves + VerticalAndHorizontalMoves, ["F5", "A2", "C8"]]

KingTests = [["C5", "D5", "E5", "C4", "E4", "C3", "D3", "E3"], DiagonalMoves + VerticalAndHorizontalMoves]
