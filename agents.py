# import numpy
from random import choices, random

cost_matrix = [[-1, 2], [-2, 1]]

def randomBool():
    return (random() - .5) >= 0

class Agent:

    def __init__(self, number_of_rounds):
        self.number_of_rounds = number_of_rounds
        self.current_move_ind = 0
        self.last_move = None
        self.score = 0


    @staticmethod
    def invert_signal(prob: float = 0.2) -> bool:
        """ 
        :param prob: probability
        with which signal should be inverted
        :return: True if signal should be
         inverted, False otherwise
        """
        return choices([True, False], weights=(prob, 1-prob), k=1)

    def make_move(self):
        raise NotImplementedError

    def on_post_move(self, opponents_last_move):
        self.opponents_last_move = opponents_last_move
        i = 1 if self.last_move else 0
        j = 1 if self.opponents_last_move else 0
        self.score += cost_matrix[i][j]


class TitForTat(Agent):
    """ simplest algorithm of its kind,
     starts with  cooperation strategy by default,
      then copies opponent's last move"""

    def __init__(self, number_of_rounds: int = 100):
        super().__init__(number_of_rounds)
        self.opponents_last_move = None

    def make_move(self) -> bool:
        res = None
        if self.opponents_last_move is None:
            res = True
        elif self.current_move_ind == self.number_of_rounds - 1:
            # stab in the back on last one!
            res = False
        else:
            res = self.opponents_last_move
        self.current_move_ind += 1
        self.last_move = res
        return res

    # def on_post_move(self, opponents_last_move : bool = None) -> None:
    #     super.on_po
    def on_post_move(self, opponents_last_move):
        super().on_post_move(opponents_last_move)


class Forgiver(Agent):
    """ starts with cooperation strategy by default,
      then copies opponent's last move;
      tries to cooperate after several treacherous
      moves in a row, to prevent false signal effects """

    def __init__(self, number_of_rounds: int = 100, max_cheats: int = 5):
        super().__init__(number_of_rounds)
        self.max_cheats = max_cheats
        self.current_cheats = 0

    def forgive(self) -> bool:
        if self.current_cheats >= self.max_cheats:
            self.current_cheats = 0
            return True
        else:
            return False

    def make_move(self, rivals_last_move: bool = None) -> bool:
        if rivals_last_move is None:
            return True
        else:
            if not rivals_last_move:
                self.current_cheats += 1

            need_to_forgive = self.forgive()
            if need_to_forgive:
                return False if self.invert_signal() else True
            else:
                # exclusive OR
                return True if rivals_last_move !=\
                               self.invert_signal() else False


class Truster(Agent):
    def __init__(self, number_of_rounds: int = 100, max_cheats: int = 5, rounds_before_trust: int = 10):
        super().__init__(number_of_rounds)
        self.rounds_before_trust = rounds_before_trust
        self.rounds_passed = 0
        self.max_cheats = max_cheats
        self.current_cheats = 0

    def forgive(self) -> bool:
        if self.current_cheats >= self.max_cheats:
            self.current_cheats = 0
            return True
        else:
            return False

    #redo, strange strategy
    def make_move(self, rivals_last_move: bool = None) -> bool:
        if rivals_last_move is None:
            return True
        if self.rounds_passed <= self.rounds_before_trust:
            self.rounds_passed += 1
            # exclusive OR
            return True if rivals_last_move != \
                           self.invert_signal() else False

        else:
            if not rivals_last_move:
                self.current_cheats += 1

            need_to_forgive = self.forgive()
            if need_to_forgive:
                return False if self.invert_signal() else True
            else:
                # exclusive OR
                return True if rivals_last_move !=\
                               self.invert_signal() else False



def main():
    NUM_OF_MOVES = 10

    a0 = TitForTat(NUM_OF_MOVES)
    a1 = TitForTat(NUM_OF_MOVES)

    for i in range(NUM_OF_MOVES):
        a0_move = a0.make_move()
        a1_move = a1.make_move()
        # process output of the opponent
        a0.on_post_move(a1_move)
        a1.on_post_move(a0_move)
        print(f"a0 : {a0_move}, a1 : {a1_move}")



if __name__ == "__main__":
    main()