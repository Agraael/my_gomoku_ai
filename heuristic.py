from itertools import tee, islice, chain
from typing import List

EMPTY_CELL = 0
WHITE_CELL = 1
BLACK_CELL = 2


def prev_and_next(iterator):

    """
    function à utiliser dans un for each , qui permet d'avoir l'element prev , actuell et suivant
    exemple :  for prev_cell, cell, next_cell in prev_and_next(row):
    """

    # pprevs, prevs, items, nexts, nnexts = tee(iterator, 5)
    prevs, items, nexts = tee(iterator, 3)
    prevs = chain([None], prevs)
    # pprevs = chain([None], [None], pprevs)
    nexts = chain(islice(nexts, 1, None), [None])
    # nnexts = chain(islice(nnexts, 2, None), [None])
    return zip(prevs, items, nexts)


def rotate_90_matrix(item: List[List[any]]) -> List[List[any]]:

    """
    cette function permet d'effectuer une rotation d'une matrix (ou tableau à deux dimension)
    elle retourne la nouvelle matrix obtenu
    """

    return [list(elem) for elem in zip(*item[::-1])]


def diagonal_right_matrix(item: List[List[any]]) -> List[List[any]]:

    """
    cette function permet de creer une list de list contenant toute les diogonales de la matrix
    (les diagonales ici sont des diagonales droite , elle partent donc de enhaut à gauche à en bas à droite)
    """

    new_item = []
    size = len(item)

    for j in range(size - 1, 0, -1):
        new_item.append([item[i + j][i] for i in range(0, size - j)])
    for j in range(0, size):
        new_item.append([item[i][i + j] for i in range(0, size - j)])
    return new_item


class Cell:

    """
    Objet représentant une case du jeu

    Attributes:
    :type x: int                    => position x sur la map
    :type y: int                    => position y sur la map
    :type value: any                => valeur de la cellule
    :type __parents: List[Pattern]  => liste des pattern parent de cette cellule
    """

    def __init__(self, x: int, y: int, value: any) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.value = value
        self.__parents = []

    def __eq__(self, value: any) -> bool:
        if isinstance(value, type(self.value)):
            return self.value == value
        return NotImplemented

    def __ne__(self, value: any) -> bool:
        if isinstance(value, type(self.value)):
            return self.value != value
        return NotImplemented

    def add_parent(self, item: object) -> None:

        """
        method pour ajouter un pattern parent à la liste de la cellule
        cette list servira a la methode d'évaluation de la cellule

        :param item: Pattern            => pattern parent à ajouter
        """

        if item not in self.__parents:
            self.__parents.append(item)

    def eval(self, value: any) -> float:

        """
        method qui permet d'évaluer la value de la cellue en fonction des patterns auquel elle apartient
        ainsi qu'en fonction des pattern possible a partir de cette cellule

        :param value: any             => valeur des piont du joeur, permet de determiner à quel est le joeur qui joue pour evaluer les patterns
        """

        result = 0
        hz = []
        vt = []
        dl = []
        dr = []
        patterns_list = [hz, vt, dl, dr]
        for elem in self.__parents:
            if elem.type == value:
                result += (elem.eval(True) / 10)
            else:
                result += (elem.eval(False) / 10)
            if elem.angle == 'Hz':
                hz.append(elem)
            if elem.angle == 'Vt':
                vt.append(elem)
            if elem.angle == 'Dl':
                dl.append(elem)
            if elem.angle == 'Dr':
                dr.append(elem)

        for elem in patterns_list:
            if len(elem) >= 2:
                if elem[0].type == elem[1].type:
                    tmp = Pattern([], [], elem[0].angle)
                    tmp.type = elem[0].type
                    tmp.size = elem[0].size + elem[1].size + 1
                    tmp.ends_nb = (elem[0].ends_nb - 1) + (elem[1].ends_nb - 1)
                    if tmp.type == value:
                        result += (tmp.eval(True) / 10)
                    else:
                        result += (tmp.eval(False) / 10)
        return result

    def dump(self) -> None:
        print("([x:%d|y:%d] =>" % (self.x, self.y), end=' ')
        print(self.value, end=')\n')


Gomoku_map_t = List[List[Cell]]


class Pattern:

    """
    Objet représentant un pattern de cellules avec la meme {value} (4, 3, 2, ou 1)
    ainsi que les cellules jouable à ses extrémités

    Attributes:
    :type size: int             => taille du partern
    :type ends_nb: int          => nombre d'embout vide aux extrémité du pattern
    :type angle: str            => sens du pattern : Hz, Vt, Dr, Dl
    :type cells: List[Cell]     => liste des cellules qui compose le pattern
    :type ends: List[Cell]      => liste des cellules d'embout du pattern
    :type type: any             => Valeur de cellules du pattern
    """

    def __init__(self, cells: List[Cell], ends: List[Cell], angle: str) -> None:
        super().__init__()
        self.size = len(cells)
        self.ends_nb = len(ends)
        self.angle = angle
        self.cells = cells
        self.ends = ends
        if self.ends_nb > 2:
            self.ends_nb = 2
        if self.ends_nb >= 1:
            self.type = cells[0].value
        for elem in self.ends:
            elem.add_parent(self)

    def eval(self, current_turn: bool) -> float:

        """
        cette method permet d'evaluer un pattern selon le tour du joueur
        elle revoie se score en float

        :param current_turn: bool           => détermine si c'est le tour du joueur ou non
        :return: float                      => score d'évaluation du pattern
        """

        if self.ends_nb == 0 and self.size < 5:
            return 0
        if self.size >= 5:
            return 50000
        return {
            4: {  # size of 4
                1: {True: 10000, False: 2},  # one open end current turn or not
                2: {True: 15000, False: 10000}  # two open end current turn or not
            },
            3: {  # size of 3
                1: {True: 0.07, False: 0.05},  # one open end current turn or not
                2: {True: 9000, False: 5000}  # two open end current turn or not
            },
            2: {  # size of 2
                1: {True: 0.02, False: 0.02},  # one open end current turn or not
                2: {True: 0.05, False: 0.05}  # two open end current turn or not
            },
            1: {  # size of 1
                1: {True: 0.005, False: 0.005},  # one open end current turn or not
                2: {True: 0.01, False: 0.01}  # two open end current turn or not
            }
        }[self.size][self.ends_nb][current_turn]

    def dump(self) -> None:
        print("(size : %d | ends : %d | angle : %s)" % (self.size, self.ends_nb, self.angle))

    def full_dump(self) -> None:
        print('{')
        print(' ', end=' ')
        self.dump()
        print('   Cells :')
        for cell in self.cells:
            print('   ', end=' ')
            cell.dump()
        print('   Ends :')
        for end in self.ends:
            print('   ', end=' ')
            end.dump()
        print('}')


Pattern_list_t = List[Pattern]


def horizontal_patterns(game_map: Gomoku_map_t, value, angle='Hz') -> Pattern_list_t:

    """
    cette fonction permet d'etablir une list de tout les pattern horizontaux de la valeur de {value} dans une map de cellule
    elle fonction aussi avec n'importe quel type de List de List

    :param game_map: List[List[any]]        => map dans laquel sera cherché les patterns
    :param value: any                       => valeur des pattern que l'on cherche
    :param angle:                           => determine len type des pattern lors de leur construction
    :return: Pattern_list_t                 => liste des pattern trouvé
    """

    pattern_cells = []
    pattern_ends = []
    patterns_found = []

    for row in game_map:
        for prev_cell, cell, next_cell in prev_and_next(row):

            if cell == value:
                pattern_cells.append(cell)

                if prev_cell == EMPTY_CELL:
                    pattern_ends.append(prev_cell)
                    # if prev_prev_cell == EMPTY_CELL:
                    #     pattern_ends.append(prev_prev_cell)

                if next_cell == EMPTY_CELL:
                    pattern_ends.append(next_cell)
                    # if next_next_cell == EMPTY_CELL:
                    #     pattern_ends.append(next_next_cell)

                if next_cell != value:
                    patterns_found.append(Pattern(pattern_cells,
                                                  pattern_ends,
                                                  angle))
                    pattern_ends = []
                    pattern_cells = []

        pattern_ends = []
        pattern_cells = []
    return patterns_found


def vertical_patterns(game_map: Gomoku_map_t, value, angle='Vt') -> Pattern_list_t:

    """
    cette fonction rempli le meme role que horizontal_patterns , sauf que ici nous cherchons les pattern verticaux
    en faisant un rotation à 90 degre de la map (malin non ?)
    """

    return horizontal_patterns(rotate_90_matrix(game_map), value, angle=angle)


def diagonal_right_patterns(game_map: Gomoku_map_t, value, angle='Dr') -> Pattern_list_t:

    """
    cette fonction rempli le meme role que horizontal_patterns , sauf que ici nous cherchons les pattern en diagonal droite
    (en partant de en haut à gauche à en bas à DROITE) ici on utilise la fonction diagonal_right_matrix
    pour ensuite trouver les pattern "horizontaux" dedans
    """

    return horizontal_patterns(diagonal_right_matrix(game_map), value, angle)


def diagonal_left_patterns(game_map: Gomoku_map_t, value, angle='Dl') -> Pattern_list_t:

    """
    meme chose que diagonal_right_patterns , mais cette fois si c'est les pattern diagonaux gauche
    (en partant de en haut à droite à en bas à GAUCHE)
    ici on rotate la map , puis on prend les diagonales ,puis on cherche les patterns horizontaux (hehehe)
    """

    return horizontal_patterns(diagonal_right_matrix(rotate_90_matrix(game_map)), value, angle=angle)


def patterns_find(game_map: Gomoku_map_t, value) -> Pattern_list_t:

    """
    ici on utilise les 4 fonction de recherche de pattern et on rassemble les data
    """

    patterns = []

    patterns.extend(horizontal_patterns(game_map, value))
    patterns.extend(vertical_patterns(game_map, value))
    patterns.extend(diagonal_right_patterns(game_map, value))
    patterns.extend(diagonal_left_patterns(game_map, value))

    return patterns


def eval_player(value: any, current_turn: bool, game_map: Gomoku_map_t) -> float:

    """
    trouve tout les pattern correspondant au joueur , puis les evalue et renvoie la somme

    :param value: any               => valeur des piont correspondant au joueur
    :param current_turn: bool       => détermine si c'est le tour du joueur au non
    :param game_map: Gomoku_map_t   => map sur laquel faire l'évaluation
    :return: float                  => resultat de l'evaluation
    """

    patterns = patterns_find(game_map, value)
    return sum(elem.eval(current_turn) for elem in patterns)


def clean_doublon(item: List[any]) -> List[any]:
    new_item = []
    for elem in item:
        if elem not in new_item:
            new_item.append(elem)
    return new_item


def cells_classification(ai_cells: List[Cell], enmy_cells: List[Cell], value: any, nb: int) -> List[Cell]:

    """
    Cette fonction est utiliser pour evaluer et classer les cellules d'enbout des pattern de chaque joueur
    ce qui correspond à la liste des cellules jouable pendant le tour.
    cette liste est ensuite classé par rapport à leur evaluation
    puis selectionne les nb première cellues

    :param ai_cells: List[Cell]             => cellules d'enbout de pattern de l'ia
    :param enmy_cells: List[Cell]           => cellules d'enbout de pattern du joueur adverse
    :param value: any                       => valeur des piont de l'ia , sert à l'evalutation des cellules
    :param nb: int                          => nombre pour la selection des n première cellules
    :return: List[Cell]                     => list des cellues classé
    """
    result = ai_cells
    result.extend(enmy_cells)
    result = clean_doublon(result)
    result.sort(key=lambda x: x.eval(value), reverse=True)
    return result[:nb]


class Eval:

    """
    Objet représentant l'evaluation des pattern à un instant du jeu
    Pour un joueur donnée si c'est son tour ou non

    Attributes:
    :type value: any                => valeur correspondante au piont du joueur à evaluer
    :type current_turn: bool        => détermine si c'est au tour du joueur avec les pionts de valeur {value} de jouer
    :type patterns: Pattern_list_t  => liste des pattern appartenant au joueur
    :type score: float              => valeur des pions du joueur (les valeurs sont différent si cést son tour ou non)
    :type ends_cells: List[Cell}    => liste des toutes les cellules d'enbout de tout les pattern (sans doublont)
    :type eval_map: Gomoku_map_t    => reference sur la map utiliser lors de l'evaluation
    """

    def __init__(self, value: any, current_turn: bool, game_map: Gomoku_map_t) -> None:
        super().__init__()
        self.value = value
        self.current_turn = current_turn
        self.patterns = patterns_find(game_map, self.value)
        self.score = sum(elem.eval(current_turn) for elem in self.patterns)
        self.eval_map = game_map
        tmp = []
        for elem in self.patterns:
            tmp.extend(elem.ends)
        self.ends_cells = tmp
        for cell in tmp:
            if cell not in self.ends_cells:
                self.ends_cells.append(cell)

    def is_winning(self) -> bool:
        for elem in self.patterns:
            if elem.size >= 5:
                return True
        return False


def gen_gomoku_map(value_map: List[List[any]]) -> Gomoku_map_t:
    return [[Cell(x, y, value_map[y][x]) for x in range(0, len(value_map[0]))] for y in range(0, len(value_map))]

