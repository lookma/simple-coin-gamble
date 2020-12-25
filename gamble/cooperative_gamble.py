from .gamble import Gamble


class CooperativeGamble(Gamble):
    """
    Cooperative way of gambling.
    For each round the total available amount is distributed to all players.
    """

    def __init__(
        self,
        name: str,
        number_of_players: int,
        number_of_rounds: int,
        bet_amount: float,
        gain_percentage: int,
        loss_percentage: int,
        coordination_fee: int,
    ):
        super().__init__(
            name=name,
            number_of_players=number_of_players,
            number_of_rounds=number_of_rounds,
            bet_amount=bet_amount,
            gain_percentage=gain_percentage,
            loss_percentage=loss_percentage,
        )
        self.__coordination_factor: float = 1.0 - coordination_fee / 100

    def _play_round(self, round_index: int) -> None:
        amount: float = (
            self.results.total_amounts[-1] * self.__coordination_factor
        ) / len(self.players)
        for player in self.players:
            new_amount: float = self._apply_rule(amount)
            player.add_new_amount(new_amount)
        return
