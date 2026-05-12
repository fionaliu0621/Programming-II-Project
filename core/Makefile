# ── Too Close to Home — C core Makefile ──────────────────────────
# Output: libtcth_core.so / .dylib / .dll
# Called by bridge.py via ctypes.
#
#   make          → shared library
#   make test     → build + run self-test
#   make clean    → remove build artefacts
# ─────────────────────────────────────────────────────────────────

CC      := gcc
CFLAGS  := -Wall -Wextra -O2 -fPIC -std=c11
SRCS    := puzzle.c timer.c save.c
OBJS    := $(SRCS:.c=.o)

# Platform
UNAME := $(shell uname -s 2>/dev/null || echo Windows)
ifeq ($(UNAME), Darwin)
    EXT    := dylib
    SHARED := -dynamiclib
    LIBS   := -lm
else ifeq ($(UNAME), Linux)
    EXT    := so
    SHARED := -shared
    LIBS   := -lm -lrt
else
    EXT    := dll
    SHARED := -shared
    LIBS   :=
endif

LIB := libtcth_core.$(EXT)

.PHONY: all test clean

all: $(LIB)

$(LIB): $(OBJS)
	$(CC) $(SHARED) -o $@ $^ $(LIBS)
	@echo "[✓] Built $(LIB)"

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# ── Self-test ─────────────────────────────────────────────────────
TEST_SRC := test_main.c

test: $(TEST_SRC) $(OBJS)
	$(CC) $(CFLAGS) -o tcth_test $(TEST_SRC) $(OBJS) $(LIBS)
	./tcth_test

$(TEST_SRC):
	@printf '#include <stdio.h>\n#include "puzzle.h"\n#include "timer.h"\n#include "save.h"\n\nint main(void) {\n' > $@
	@printf '    puts("=== puzzle load ===");\n' >> $@
	@printf '    Puzzle ps[MAX_PUZZLES];\n' >> $@
	@printf '    int n = load_puzzles("../data/puzzles.txt", ps, MAX_PUZZLES);\n' >> $@
	@printf '    printf("Loaded %%d puzzles\\n", n);\n' >> $@
	@printf '    for (int i=0;i<n;i++) print_puzzle(&ps[i]);\n' >> $@
	@printf '\n    puts("\\n=== validate ===");\n' >> $@
	@printf '    PuzzleResult r = validate_answer(&ps[0], "20584");\n' >> $@
	@printf '    printf("Puzzle 1 (20584): %%s\\n", r==PUZZLE_CORRECT?"CORRECT":"WRONG");\n' >> $@
	@printf '    r = validate_answer(&ps[1], "beacon");\n' >> $@
	@printf '    printf("Puzzle 2 (beacon): %%s\\n", r==PUZZLE_CORRECT?"CORRECT":"WRONG");\n' >> $@
	@printf '    r = validate_answer(&ps[2], "white");\n' >> $@
	@printf '    printf("Puzzle 3 (white): %%s\\n", r==PUZZLE_CORRECT?"CORRECT":"WRONG");\n' >> $@
	@printf '    r = validate_answer(&ps[3], "25, 121");\n' >> $@
	@printf '    printf("Puzzle 4 (25, 121): %%s\\n", r==PUZZLE_CORRECT?"CORRECT":"WRONG");\n' >> $@
	@printf '\n    puts("\\n=== timer ===");\n' >> $@
	@printf '    Timer t; timer_init(&t, PUZZLE_TIME_SEC); timer_start(&t);\n' >> $@
	@printf '    char buf[16]; timer_fmt_remaining(&t, buf, 16);\n' >> $@
	@printf '    printf("Remaining: %%s\\n", buf);\n' >> $@
	@printf '    printf("Score now: %%d\\n", calc_score(timer_elapsed_int(&t)));\n' >> $@
	@printf '\n    puts("\\n=== save/load ===");\n' >> $@
	@printf '    SaveFile sf;\n' >> $@
	@printf '    save_init(&sf, "TestPlayer", n);\n' >> $@
	@printf '    save_set_puzzle(&sf, 1, 1, 4, 120, 0);\n' >> $@
	@printf '    save_write("/tmp/tcth_test.bin", &sf);\n' >> $@
	@printf '    SaveFile sf2; save_read("/tmp/tcth_test.bin", &sf2);\n' >> $@
	@printf '    printf("Loaded player: %%s, puzzle_count: %%d\\n", sf2.player, sf2.puzzle_count);\n' >> $@
	@printf '    puts("\\n[ALL DONE]");\n' >> $@
	@printf '    return 0;\n}\n' >> $@

clean:
	rm -f $(OBJS) $(LIB) tcth_test $(TEST_SRC)
