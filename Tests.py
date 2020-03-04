from ChessPieces import *
from Chess import *
from TestVariables import *
import pytest

@pytest.mark.parametrize("Position, Movement, CheckAnswer, CheckMateAnswer", [(Position1, ["G1", "G8"], True, False), (Position2, ["G1", "G8"], True, True), (Position3, ["E2", "E4"], False, False), (Position4, ["A6", "A8"], True, True), (Position5, ["A1", "A6"], False, False), (Position6, ["D3", "B5"], True, False), (Position7, ["E6", "E7"], False, False), (TowerCheckMate, ["A3", "A8"], True, True)])
def test_CheckMate(Position, Movement, CheckAnswer, CheckMateAnswer):
    ResetPieces()
    InitializeBoard(Position)
    MovingPiece = GetPieceInsideTile(Movement[0])
    DestinyTile = Movement[1]
    GetKings()
    print(CheckMateAnswer)
    assert(Check(MovingPiece, DestinyTile) == CheckAnswer)
    assert(CheckMate(MovingPiece, DestinyTile) == CheckMateAnswer)

@pytest.mark.parametrize("TestedPiece, Tests", [[Pawn, WhitePawnTests], [Horse, HorseTests], [Bishop, BishopTests], [Tower, TowerTests], [Queen, QueenTests], [King, KingTests]])
def test_Movement(TestedPiece, Tests):
    ResetPieces()
    InitializeBoard([[TestedPiece, ["D4"], []]])
    TestedPiece = GetPieceInsideTile("D4")
    CorrectMoves = Tests[0]
    IncorrectMoves = Tests[1]
    for Move in CorrectMoves:
        TilePath = CreateTilePath(TestedPiece, *GetMovement(TestedPiece.Tile, Move))
        assert(TestedPiece.ValidMove(TilePath))
    for Move in IncorrectMoves:
        print(Move)
        TilePath = CreateTilePath(TestedPiece, *GetMovement(TestedPiece.Tile, Move))
        assert(not TestedPiece.ValidMove(TilePath))



