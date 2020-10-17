import argparse
import curses
import time
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from _curses import _CursesWindow
    Window = _CursesWindow
else:
    from typing import Any
    Window = Any


State = Tuple[List[int], List[int], List[int]]


class ctx:
    screen: Window
    n_disks: int
    sleep: float
    waitkey: bool


def main(stdscr: Window):
    parser = argparse.ArgumentParser()
    parser.add_argument('--disks', '-n', type=int, default=4)
    parser.add_argument('--sleep', type=float, default=0.)
    parser.add_argument('--waitkey', action='store_true')
    args = parser.parse_args()

    ctx.screen = stdscr
    ctx.n_disks = args.disks
    ctx.sleep = args.sleep
    ctx.waitkey = args.waitkey

    solve(ctx.n_disks, 0, 2)


s: State = ([], [], [])


def solve(
    n: int,       # 考えるディスクの数
    rodA: int,    # 移動する元のrod
    rodC: int,    # 移動する先のrod
):
    rodB = 3 - (rodA + rodC)
    if n == 0:
        print_state()
    else:
        s[rodA].append(n)
        solve(n - 1, rodA, rodB)
        s[rodA].pop()
        s[rodC].append(n)
        solve(n - 1, rodB, rodC)
        s[rodC].pop()


def print_state():
    #  a rod
    # h1: height = n + 2
    # w1: width  = 2 * n + 3

    #     |
    #    #|#
    #   ##|##
    #  ###|###
    # ---------

    # rods
    # h: height = h1
    # w: width  = 3 * w1

    # +----+----+----+
    # |rod1|rod2|rod3|
    # +----+----+----+

    n_disks = ctx.n_disks
    h1 = n_disks + 1
    w1 = 2 * n_disks + 3

    for rod_i, rod in enumerate(s):
        x0 = rod_i * w1
        ctx.screen.addstr(h1, x0, '-' * w1)
        for i in range(n_disks + 1):
            size = rod[i] if i < len(rod) else 0
            pad = n_disks + 1 - size
            line = ' ' * pad + "#" * size + "|" + "#" * size + ' ' * pad
            ctx.screen.addstr(h1 - i - 1, x0, line)
    ctx.screen.refresh()
    if ctx.waitkey:
        ctx.screen.getkey()
    time.sleep(ctx.sleep)


if __name__ == '__main__':
    curses.wrapper(main)
