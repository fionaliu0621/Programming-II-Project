#ifndef PUZZLE_H
#define PUZZLE_H

#include <stddef.h>

#define MAX_PUZZLES     16
#define HINT_INTERVAL   240   /* seconds between hints  (4 min) */
#define HINT_COUNT       3    /* hints per puzzle               */
#define PUZZLE_TIME_SEC 900   /* total time limit       (15 min)*/
#define MAX_SCORE        4    /* full marks per puzzle          */

/* Which hints have been unlocked (bit-flags: bit0=hint1, bit1=hint2, bit2=hint3) */
typedef unsigned int HintMask;

typedef struct {
    int  id;
    char location[64];    /* 地點                        */
    char title[64];       /* 題目標題                    */
    char question[1024];  /* 謎題說明（顯示給玩家）      */
    char answer[128];     /* 正確答案（大寫，無空白）     */
    char hint[HINT_COUNT][256]; /* 三則提示               */
    int  max_score;       /* 滿分（通常 4）               */

    /* runtime */
    int      solved;
    int      score_earned;
    HintMask hints_unlocked; /* bitfield                 */
} Puzzle;

typedef enum {
    PUZZLE_CORRECT = 0,
    PUZZLE_WRONG   = 1
} PuzzleResult;

/* Load puzzle data from pipe-delimited text file.
   Returns number loaded, or -1 on error. */
int          load_puzzles    (const char *path, Puzzle out[], int max);

/* Case-insensitive, whitespace-stripped comparison.
   Sets p->solved = 1 on success. */
PuzzleResult validate_answer (Puzzle *p, const char *user_input);

/* Return which hints should be visible given elapsed seconds.
   Also updates p->hints_unlocked. */
HintMask     unlock_hints    (Puzzle *p, int elapsed_sec);

/* Compute score from elapsed seconds (4/3/2/1/0). */
int          calc_score      (int elapsed_sec);

/* Return hint text by 0-based index, or NULL if not yet unlocked. */
const char  *get_hint        (const Puzzle *p, int hint_index);

void         print_puzzle    (const Puzzle *p);

#endif /* PUZZLE_H */
