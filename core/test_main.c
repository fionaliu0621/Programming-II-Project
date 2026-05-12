#include <stdio.h>
#include "puzzle.h"
#include "timer.h"
#include "save.h"

int main(void) {
    puts("=== puzzle load ===");
    Puzzle ps[MAX_PUZZLES];
    int n = load_puzzles("../data/puzzles.txt", ps, MAX_PUZZLES);
    printf("Loaded %d puzzles\n", n);
    for (int i=0;i<n;i++) print_puzzle(&ps[i]);

    puts("\n=== validate ===");
    PuzzleResult r = validate_answer(&ps[0], "20584");
    printf("Puzzle 1 (20584): %s\n", r==PUZZLE_CORRECT?"CORRECT":"WRONG");
    r = validate_answer(&ps[1], "beacon");
    printf("Puzzle 2 (beacon): %s\n", r==PUZZLE_CORRECT?"CORRECT":"WRONG");
    r = validate_answer(&ps[2], "white");
    printf("Puzzle 3 (white): %s\n", r==PUZZLE_CORRECT?"CORRECT":"WRONG");
    r = validate_answer(&ps[3], "25, 121");
    printf("Puzzle 4 (25, 121): %s\n", r==PUZZLE_CORRECT?"CORRECT":"WRONG");

    puts("\n=== timer ===");
    Timer t; timer_init(&t, PUZZLE_TIME_SEC); timer_start(&t);
    char buf[16]; timer_fmt_remaining(&t, buf, 16);
    printf("Remaining: %s\n", buf);
    printf("Score now: %d\n", calc_score(timer_elapsed_int(&t)));

    puts("\n=== save/load ===");
    SaveFile sf;
    save_init(&sf, "TestPlayer", n);
    save_set_puzzle(&sf, 1, 1, 4, 120, 0);
    save_write("/tmp/tcth_test.bin", &sf);
    SaveFile sf2; save_read("/tmp/tcth_test.bin", &sf2);
    printf("Loaded player: %s, puzzle_count: %d\n", sf2.player, sf2.puzzle_count);
    puts("\n[ALL DONE]");
    return 0;
}
