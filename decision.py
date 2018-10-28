import heuristic as hs
import math
from typing import List
import pisqpipe as pp
import time


class Decision:

    """
    Objet représentant le processus de reflextion de l'ia pour jouer

    Attributes:
    :type ai_value: any             => valeur des pionts représentant l'ia
    :type play_cell: Cell           => cellue ou l'ia doit jouer , set après utilisation de la fonction minmax
    :type rescue_cell: Cell         => cellule à jouer si l'ia n'a pas eu le temps de refléchir
    :type enmy_value: any           => valeur des pionts représentant le joueur adverse
    :type time_limit: int           => temps limite de reflexion em milliseconde
    """

    def __init__(self, ai: any, black: any, white: any, empty: any) -> None:
        super().__init__()
        self.ai_value = ai
        hs.BLACK_CELL = black
        hs.WHITE_CELL = white
        hs.EMPTY_CELL = empty
        self.time_limit = 0
        self.time_start = 0
        self.play_cell = None
        self.rescue_cell = None
        if self.ai_value == hs.BLACK_CELL:
            self.enmy_value = hs.WHITE_CELL
        else:
            self.enmy_value = hs.BLACK_CELL

    def min_max(self, depth: int, values_map: List[List[any]],
                turn=True, played_cell: hs.Cell = None, start=True,
                calculus=10, reduction=3, alpha=-math.inf, beta=+math.inf) -> float:
        """
        :arg depth: int                             => profondeur de l'arbre de recherche
        :arg values_map: List[List[any]]            => double tableu des valeur de la carte
        :arg turn: bool                             => défini si c'est le tour du joeur ou non
        :arg played_cell: Cell                      => Cellule qui à été joué lors du tour
        :arg start: bool                            => permet de déterminer si c'est la node de départ ou non
        :arg calculus: int                          => nombre de cellules maximum a checker dans le premier etage de l'arbre , diminué par reduction a chaque profondeur, by default  it's 15
        :arg reduction: int                         => determine la reduction du calculus à chaque profondeur de l'arbre recursif, by default it's 3
        :arg alpha: float                           => valeur d'alpha pour l'alpha-beta prunning, par defaut c'est - l'infini
        :arg beta: float                            => valeur de beta pour l'alpha-beta prunning, par defaut c'est + l'infini
        """

        if start:
            self.time_start = int(round(time.time() * 1000))

        gomoku_map = hs.gen_gomoku_map(values_map)
        if played_cell is not None:
            gomoku_map[played_cell.y][played_cell.x].value = played_cell.value
        eval_ai = hs.Eval(self.ai_value, turn, gomoku_map)
        eval_enmy = hs.Eval(self.enmy_value, not turn, gomoku_map)

        if len(eval_enmy.patterns) <= 0:
            self.start_play(values_map)
            return 0

        if depth == 0 or eval_ai.is_winning() or eval_enmy.is_winning() or calculus <= 0 or self.time_check():
            return eval_ai.score - eval_enmy.score

        playable_cells = hs.cells_classification(eval_ai.ends_cells, eval_enmy.ends_cells,
                                                 self.ai_value if turn else self.enmy_value, calculus)

        if start:
            self.rescue_cell = playable_cells[0]

        if turn:
            best_value = {'cell': None, 'score': -math.inf}
            for cell in playable_cells:

                if self.time_check():
                    break

                cell.value = self.ai_value
                score = self.min_max(depth - 1, values_map, turn=False, played_cell=cell,
                                     start=False, calculus=calculus - reduction,
                                     alpha=alpha, beta=beta)
                alpha = score
                if alpha >= beta:
                    return alpha
                if score > best_value['score']:
                    best_value = {'cell': cell, 'score': score}

        else:
            best_value = {'cell': None, 'score': +math.inf}
            for cell in playable_cells:

                if self.time_check():
                    break

                cell.value = self.enmy_value
                score = self.min_max(depth - 1, values_map, turn=True, played_cell=cell,
                                     start=False, calculus=calculus - reduction,
                                     alpha=alpha, beta=beta)
                beta = score
                if alpha >= beta:
                    return beta
                if score < best_value['score']:
                    best_value = {'cell': cell, 'score': score}

        if start:
            self.play_cell = best_value['cell']
        return best_value['score']

    def start_play(self, values_map: List[List[any]]) -> None:
        x = len(values_map[0]) // 2
        y = len(values_map) // 2
        self.play_cell = hs.Cell(x, y, self.ai_value)

    def time_check(self) -> bool:
        if self.time_limit == 0:
            return False
        now = int(round(time.time() * 1000))
        if (now - self.time_start) >= (self.time_limit - 25):
            pp.pipeOut('MESSAGE time limit warning ' + str(now - self.time_start))
            return True
        return False


