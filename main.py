import numpy

from random import choices


class Agent:

    def __init__(self, number_of_rounds):
        self.number_of_rounds = number_of_rounds

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

    def main(self):
        while self.number_of_rounds:
            self.make_move()  # think of how to pass opponent's move
            self.number_of_rounds -= 1


class ZubZaZub(Agent):
    """ simplest algorithm of its kind,
     starts with  cooperation strategy by default,
      then copies opponent's last move"""

    def __init__(self, number_of_rounds: int = 100):
        super().__init__(number_of_rounds)
        self.opponents_last_move = True

    def make_move(self, rivals_last_move: bool = None) -> bool:
        if rivals_last_move is None:
            return True
        else:
            # exclusive OR
            return True if rivals_last_move != \
                           self.invert_signal() else False
            # if self.invert_signal():
            #     return False if rivals_last_move else True
            #
            # return rivals_last_move


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