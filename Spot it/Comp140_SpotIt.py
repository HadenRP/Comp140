"""
Create a deck of spotit cards
"""
import comp140_module2 as spotit


def equivalent(point1, point2, mod):
    """
    Return True if the points are equivalent under projective geometry, else False.
    """
    cross = (
        (point1[1] * point2[2] - point1[2] * point2[1]) % mod,
        (point1[2] * point2[0] - point1[0] * point2[2]) % mod,
        (point1[0] * point2[1] - point1[1] * point2[0]) % mod
    )
    print(cross)
    if point1 != point2:
        if cross == (0, 0, 0):
            return True
        return False
    return True


def incident(point, line, mod):
    """
    Return True if the point lies on the line, otherwise False.
    """
    product = (point[0] * line[0] + point[1] * line[1] + point[2] * line[2]) % mod
    return product == 0


def generate_all_points(mod):
    """
    Generate all unique points in the projective plane over F_mod.
    """
    points = []
    for xvalue in range(mod):
        for yvalue in range(mod):
            for zvalue in range(mod):
                points.append((xvalue, yvalue, zvalue))
    points.remove((0, 0, 0))
    unique_points = []
    for items in points:
        if not any(equivalent(items, next_item, mod) for next_item in unique_points):
            unique_points.append(items)
    return unique_points


def create_cards(points, lines, mod):
    """
    Create Spot It! cards, where each card is a list of point indices incident to a line.
    """
    deck = []
    for line in lines:
        card = []
        for index, point in enumerate(points):
            if incident(point, line, mod):
                card.append(index)
        deck.append(card)
    return deck


def run():
    """
    Create the deck and play the Spot It! game using a GUI.
    """
    # Prime modulus (set to 2 or 3 for development; 7 for full game)
    modulus = 7

    # Generate all unique points for the given modulus
    points = generate_all_points(modulus)
    # Lines are the same as points, so make a copy
    lines = points[:]
    # Generate a deck of cards given the points and lines
    deck = create_cards(points, lines, modulus)

    # Run GUI (modulus > 7 may break the GUI)
    spotit.start(deck)


# Uncomment to run the game using the run() function.
run()
