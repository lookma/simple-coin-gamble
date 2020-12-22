from random import randint
from typing import Callable, List, Optional

class Coin:
    """Simulates a coin."""
    __head = False
    __toss_count = 0
    __head_count = 0

    def toss(self) -> None:
        """Toss a coin."""
        r = randint(1, 2)
        self.__head = True if r == 1 else False
        self.__toss_count += 1
        if self.__head:
            self.__head_count += 1

    def get_head_percentage(self) -> float:
        """Returns the percentages of heads relative to the total umber of coin tosses."""
        return self.__head_count * 100 / self.__toss_count

    def is_head(self) -> bool:
        """Check if the coins shows heads."""
        return self.__head

    def get_head_count(self) -> int:
        """Return the number of tossed heads."""
        return self.__head_count

    def get_toss_count(self) -> int:
        """Return the number of tosses."""
        return self.__toss_count

class Player:
    def __init__(self, name: str, bet_amount: float) -> None:
        self.__name = name
        self.__amounts = [bet_amount]

    @property
    def name(self) -> str:
        """Name of the player."""
        return self.__name

    @property
    def is_winner(self) -> bool:
        """
        Check if the player is a winner.

        If the current amount of a player is greater or equal to the initial amount it is a winner.
        """
        return self.__amounts[-1] >= self.__amounts[0]

    @property
    def amount(self) -> float:
        """
        Current amount of the player.
        """
        return self.__amounts[-1]

    @property
    def amounts(self) -> List[float]:
        """
        The amounts for all rounds of the player.

        The initial amount (bet) is stored at index 0.
        """
        return self.__amounts

    def add_new_amount(self, amount:float) -> None:
        self.__amounts.append(amount)


class RoundResults:
    __total_amounts:List[float] = []
    __number_of_winners:List[int] = []
    __number_of_losers:List[int] = []
    __winner_percentages:List[float] = []
    __min_amounts:List[float] = []
    __max_amounts:List[float] = []
    __avg_amounts:List[float] = []

    def __init__(self, players:List[Player]) -> None:
        self.add_round(players)

    def add_round(self, players:List[Player]) -> None:
        total_amount = 0
        number_of_winners = 0
        min_amount = players[0].amount
        max_amount = 0
        for player in players:
            total_amount += player.amount
            min_amount = min(player.amount, min_amount)
            max_amount = max(player.amount, max_amount)
            if player.is_winner:
                number_of_winners += 1
        winner_percentage = number_of_winners * 100 / len(players)

        self.__total_amounts.append(total_amount)
        self.__number_of_winners.append(number_of_winners)
        self.__number_of_losers.append(len(players) - number_of_winners)
        self.__winner_percentages.append(winner_percentage)
        self.__min_amounts.append(min_amount)
        self.__max_amounts.append(max_amount)
        self.__avg_amounts.append(total_amount / len(players))

    @property
    def number_of_rounds(self) -> int:
        return len(self.__total_amounts) - 1

    @property
    def total_amounts(self) -> List[float]:
        return self.__total_amounts

    @property
    def avg_amounts(self) -> List[float]:
        return self.__avg_amounts

    @property
    def number_of_winners(self) -> List[int]:
        return self.__number_of_winners

    @property
    def number_of_losers(self) -> List[int]:
        return self.__number_of_losers
    
    @property
    def winner_percentages(self) -> List[float]:
        return self.__winner_percentages
    
    @property
    def min_amounts(self) -> List[float]:
        return self.__min_amounts
    
    @property
    def max_amounts(self) -> List[float]:
        return self.__max_amounts

class Gamble:
    __coin = Coin()

    def __init__(
        self,
        number_of_players:int=10,
        number_of_rounds:int=100,
        bet_amount:float=100.0,
        gain_percentage:int=50,
        loss_percentage:int=40,
        _progress_callback:Optional[Callable[[int,int], None]]=None,
    ) -> None:
        assert number_of_players > 0
        assert number_of_rounds > 0
        assert bet_amount > 0
        assert gain_percentage >= 0
        assert loss_percentage >= 0 and loss_percentage <= 100

        self.__gain_factor = 1.0 + gain_percentage / 100.0
        self.__loss_factor = 1.0 - loss_percentage / 100.0
        self.__number_of_rounds = number_of_rounds
        self.__progress_callback = _progress_callback

        self.__players = []
        for i in range(1, number_of_players + 1):
            self.__players.append(Player(name="p" + str(i), bet_amount=bet_amount))
        self.__round_results = RoundResults(self.__players)

    def _apply_rule(self, amount:float) -> float:
        self.__coin.toss()
        amount = (
            amount * self.__gain_factor
            if self.__coin.is_head()
            else amount * self.__loss_factor
        )
        return round(amount, 2)

    def _play_round(self, round_index: int) -> None:
        for player in self.__players:
            player.add_new_amount(self._apply_rule(player.amount))
        return

    def play(self) -> None:
        for index in range(1, self.__number_of_rounds + 1):
            self._play_round(index)
            self.__round_results.add_round(self.__players)
            if self.__progress_callback:
                self.__progress_callback(index, self.__number_of_rounds)
        return
    
    @property
    def results(self) -> RoundResults:
        return self.__round_results

    @property
    def players(self) -> List[Player]:
        return self.__players
