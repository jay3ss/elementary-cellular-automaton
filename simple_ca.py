"""
Simple CA from Section 7.3 of
https://natureofcode.com/book/chapter-7-cellular-automata/
"""
import argparse
import random
import time

import pygame

import automaton


def main(ruleset, rand, density):
    # set our screen's width and height
    screen_width, screen_height = (1001, 1000)

    pygame.init()

    pygame.display.set_caption("Cellular Automata - Simple Rule")
    screen = pygame.display.set_mode((screen_width, screen_height))

    running = True

    white = (255, 255, 255)
    black = (0, 0, 0)
    square = 1
    width = int(screen_width/square)
    print(f'Rule {ruleset}')
    delay = 1e-4
    ca = automaton.CellularAutomaton(
        width=width, ruleset=ruleset, rand=(rand, density)
    )
    frame_rate = 60/1000 # convert to milliseconds
    while running:
        events = pygame.event.get()

        for event in pygame.event.get():
            # exit loop if user clicks 'x'
            if event.type == pygame.QUIT:
                pygame.image.save(screen, 'simulation.png')
                running = False

            elif event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                # draw only is user presses spacebar
                if key[pygame.K_SPACE]:
                    print('Drawing a new generation')
                    screen.fill(black)
                    cell_num = 0
                    for y in range(0, screen_width, square):
                        for x in range(0, screen_height, square):
                            cell = ca.row[cell_num]
                            if cell.state:
                                screen.set_at((x, y), white)
                                # screen.fill(white, (x, y, x+square, y+square))
                                # pygame.draw.rect(screen, white, (x, y, x+square, y+square))
                            else:
                                screen.set_at((x, y), black)
                                # screen.fill(black, (x, y, x+square, y+square))
                                # pygame.draw.rect(screen, black, (x, y, x+square, y+square))
                            cell_num += 1
                        pygame.display.update()
                        ca.generate()
                        cell_num = 0
                        # time.sleep(delay)
                        # update the display
                # quit if the user presses the spacebar
                if key[pygame.K_q]:
                    exit()
        # update the display
        # pygame.display.flip()


def get_ruleset(rule_str):
    rule = list(format(int(rule_str), '08b'))
    ruleset = [False if r == '0' else True for r in rule]
    return ruleset


def generate_random_ruleset():
    ruleset = [random.random() < 0.5 for r in range(8)]
    return ruleset


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ruleset', help='Ruleset (as int) for a 256-bit cellular automaton')
    parser.add_argument('--random', help='Start with a randomly initialized CA', action='store_true', default=False)
    parser.add_argument('--density', help='Density of randomly generated initial state', default=0.5, type=float)
    args = parser.parse_args()
    ruleset = get_ruleset(args.ruleset)
    rand = args.random
    density = args.density
    start_msg = f'Using Rule {args.ruleset}'
    if rand:
        start_msg += f' with a random initialization'
    print(start_msg)
    main(ruleset, rand, density)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('ruleset', help='Ruleset (as int) for a 256-bit cellular automaton')
#     parser.add_argument('--random', help='Start with a randomly initialized CA', action='store_true', default=False)
#     parser.add_argument('--size', help='Square size', default=1, type=int)
#     args = parser.parse_args()
#     ruleset = get_ruleset(args.ruleset)
#     rand = args.random
#     # size = int(args.size)
#     size = int(args.size)
#     main(ruleset, random, size)
