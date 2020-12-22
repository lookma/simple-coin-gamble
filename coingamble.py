#!/usr/bin/env python3
import argparse
from typing import cast, Any
import matplotlib.pyplot as plt
from gamble import gamble as g


def progress_cli(round_index:int, total_number_of_rounds:int) -> None:
    """Callback function to display the progress of the game for command line interfaces."""
    print(f"Round {round_index} of {total_number_of_rounds} ({round_index * 100 / total_number_of_rounds:.0f}%)")

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
    return args

def print_results(gamble: g.Gamble)-> None:
    results = gamble.results
    for round in range(0, results.number_of_rounds + 1):
        print(f"{round}: winners {results.winner_percentages[round]:.2f}%, total {results.total_amounts[round]:.2f}")

def plot_results(gamble: g.Gamble):
    results = gamble.results

    fig, axs = plt.subplots(2,1)
    fig = fig

    cast(Any, axs)[0].plot(results.total_amounts, label="Total")
    cast(Any, axs)[0].plot(results.min_amounts, label="Min")
    cast(Any, axs)[0].plot(results.max_amounts, label="Max")
    cast(Any, axs)[0].plot(results.avg_amounts, label="Avg")
    cast(Any, axs)[0].set_yscale("log")
    cast(Any, axs)[0].set_xlabel("Round")
    cast(Any, axs)[0].set_ylabel("Amount")
    cast(Any, axs)[0].set_title("Amounts")
    cast(Any, axs)[0].legend()
    cast(Any, axs)[0].grid()

    cast(Any, axs)[1].plot(results.number_of_winners, label="Winners")
    cast(Any, axs)[1].plot(results.number_of_losers, label="Losers")
    cast(Any, axs)[1].set_xlabel("Round")
    cast(Any, axs)[1].set_ylabel("Count")
    cast(Any, axs)[1].set_title("Winners & Losers")
    cast(Any, axs)[1].legend()
    cast(Any, axs)[1].grid()

    plt.tight_layout()
    plt.show()

def main():
    args = parse_args()
    game = g.Gamble(
        number_of_players=args.player_count,
        number_of_rounds=args.round_count,
        bet_amount=args.initial_bet,
        gain_percentage=args.gain_percentage,
        loss_percentage=args.loss_percentage,
        _progress_callback=progress_cli,
    )
    game.play()
    #print_results(game)
    plot_results(game)
    return


if __name__ == "__main__":
    main()
