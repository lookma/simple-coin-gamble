#!/usr/bin/env python3
import argparse
from typing import cast, Any, List
import matplotlib.pyplot as plt
from gamble import gamble as g
from gamble import cooperative_gamble as cg


def progress_cli(name: str, round_index: int, total_number_of_rounds: int) -> None:
    """Callback function to display the progress of the game for command line interfaces."""
    if round_index % 10 == 0:
        print(
            f"{name}: round {round_index} of {total_number_of_rounds} ({round_index * 100 / total_number_of_rounds:.0f}%)"
        )
    return


def parse_args():
    parser = argparse.ArgumentParser(
        description="Simulator for the coin game.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--players",
        dest="player_count",
        help="Number of players.",
        metavar="N",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--rounds",
        dest="round_count",
        help="Number of rounds to play.",
        metavar="N",
        type=int,
        default=100,
    )
    parser.add_argument(
        "--bet",
        dest="initial_bet",
        help="Initial bet of a player.",
        metavar="N",
        type=float,
        default=100.0,
    )
    parser.add_argument(
        "--gain",
        dest="gain_percentage",
        help="Gain percentage in case of coin shows heads.",
        metavar="P",
        type=int,
        default=50,
    )
    parser.add_argument(
        "--loss",
        dest="loss_percentage",
        help="Loss percentage in case of coin shows tails.",
        metavar="P",
        type=int,
        default=40,
    )
    parser.add_argument(
        "--coordination-fee",
        dest="coordination_fee",
        help="Percentage to be spend for coordination (only for cooperative gamble).",
        metavar="P",
        type=float,
        default=0,
    )
    parser.add_argument(
        dest="modes",
        choices=["simple", "cooperative"],
        nargs="*",
        default="simple",
    )
    args = parser.parse_args()

    if args.player_count <= 0:
        parser.error("Player count must be greater than zero!")
    if args.round_count <= 0:
        parser.error("Round count must be greater than zero!")
    if args.gain_percentage < 0:
        parser.error("Gain percentage must not be negative!")
    if args.loss_percentage < 0:
        parser.error("Loss percentage must not be negatove!")
    if args.loss_percentage > 100:
        parser.error("Loss percentage must not be greater than 100!")
    if args.initial_bet <= 0.0:
        parser.error("Bet must be greater than zero!")
    if args.coordination_fee < 0:
        parser.error("Coordination fee must not be less than zero!")
    if args.coordination_fee > 100:
        parser.error("Coordination fee must not be greater than 100!")
    return args


def _plot_amounts(ax: Any, gamble: g.Gamble, max_amount: float):
    results: g.RoundResults = gamble.results
    ax.plot(results.total_amounts, label="Total")
    ax.plot(results.min_amounts, label="Min")
    ax.plot(results.max_amounts, label="Max")
    ax.plot(results.avg_amounts, label="Avg")
    ax.set_yscale("log")
    ax.set_xlabel("Round")
    ax.set_ylabel("Amount")
    ax.set_title(gamble.name)
    ax.legend()
    ax.grid()
    ax.set_ylim(0.01, max_amount * 100)


def _plot_winners_and_losers(ax: Any, gamble: g.Gamble):
    results: g.RoundResults = gamble.results

    ax.plot(results.number_of_winners, label="Winners")
    ax.plot(results.number_of_losers, label="Losers")
    ax.plot(results.number_of_total_losses, label="Total Losses")
    ax.set_xlabel("Round")
    ax.set_ylabel("Count")
    ax.set_title("Winners & Losers")
    ax.legend()
    ax.grid()


def plot_results(gambles: List[g.Gamble]):

    _, axs = plt.subplots(2, len(gambles))

    max_amount: float = 0
    for gamble in gambles:
        max_amount = max(max_amount, gamble.max_amount)

    if len(gambles) > 1:
        index: int = 0
        for gamble in gambles:
            _plot_amounts(cast(Any, axs)[0, index], gamble, max_amount)
            _plot_winners_and_losers(cast(Any, axs)[1, index], gamble)

            index += 1
        plt.suptitle("Coin Gambles")
    else:
        _plot_amounts(cast(Any, axs)[0], gambles[0], max_amount)
        _plot_winners_and_losers(cast(Any, axs)[1], gambles[0])

    plt.tight_layout()
    plt.show()


def main():
    args = parse_args()

    gambles: List[g.Gamble] = []

    if "simple" in args.modes:
        gambles.append(
            g.Gamble(
                name="Simple Gamble",
                number_of_players=args.player_count,
                number_of_rounds=args.round_count,
                bet_amount=args.initial_bet,
                gain_percentage=args.gain_percentage,
                loss_percentage=args.loss_percentage,
            )
        )

    if "cooperative" in args.modes:
        gambles.append(
            cg.CooperativeGamble(
                name="Cooperative Gamble",
                number_of_players=args.player_count,
                number_of_rounds=args.round_count,
                bet_amount=args.initial_bet,
                gain_percentage=args.gain_percentage,
                loss_percentage=args.loss_percentage,
                coordination_fee=args.coordination_fee,
            )
        )

    for gamble in gambles:
        gamble.set_progress_callback(progress_cli)
        gamble.play()

    plot_results(gambles)
    return


if __name__ == "__main__":
    main()
