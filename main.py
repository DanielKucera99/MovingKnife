import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Player:
    def __init__(self, id, valuation):
        self.id = id
        self.valuation = valuation


def moving_knife(cake_length, players):
    cake_portions = [0] * len(players)
    knife_position = 0
    knife_positions = []

    while knife_position < cake_length:
        knife_positions.append(knife_position)

        valuations = [player.valuation(knife_position) for player in players]

        if any(val <= (knife_position + 1e-9) / len(players) for val in valuations):
            stop_callers = [player for player, val in zip(players, valuations) if
                            val <= (knife_position + 1e-9) / len(players)]

            chosen_player = random.choice(stop_callers)
            portion = min(1 / len(players), cake_length - knife_position)
            cake_portions[chosen_player.id] += portion
            knife_position += portion * cake_length
        else:
            knife_position += 0.001

    return cake_portions, knife_positions


# Example usage
if __name__ == "__main__":
    def valuation1(position):
        return 0.3 * position


    def valuation2(position):
        return 0.5 * position


    def valuation3(position):
        return 0.2 * position


    players = [Player(i, valuation) for i, valuation in enumerate([valuation1, valuation2, valuation3])]

    cake_length = 1

    cake_portions, _ = moving_knife(cake_length, players)

    colors = ['blue', 'green', 'red']

    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    ax.set_aspect('equal')
    plt.axis('off')

    circle = plt.Circle((0.5, 0.5), 0.5, color='orange', fill=True)
    ax.add_artist(circle)

    start_angle = 0
    for i, portion in enumerate(cake_portions):
        end_angle = start_angle + portion * 360
        wedge = patches.Wedge((0.5, 0.5), 0.5, start_angle, end_angle, color=colors[i], alpha=0.7,
                              label=f'Player {i + 1}')
        ax.add_patch(wedge)
        start_angle = end_angle

    plt.legend()
    plt.title('Cake Division')
    plt.show()
