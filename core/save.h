#ifndef SAVE_H
#define SAVE_H

#include <time.h>
#include "puzzle.h"

#define SAVE_FILE_MAGIC "TCTH01"

/* Per-puzzle result stored in a save file */
typedef struct {
    int puzzle_id;
    int solved;       /* 0 or 1            */
    int score;        /* 0-4               */
    int elapsed_sec;  /* seconds taken     */
    int hints_shown;  /* bitmask 0b000-0b111 */
} PuzzleSave;

typedef struct {
    char        magic[8];
    int         version;        /* format version = 1          */
    long        timestamp;      /* unix time of last save      */
    char        player[64];
    int         current_puzzle; /* 1-based index of next puzzle */
    int         total_score;
    int         total_elapsed;  /* cumulative seconds          */
    int         puzzle_count;
    PuzzleSave  puzzles[MAX_PUZZLES];
} SaveFile;

/* Returns 0 on success, -1 on failure */
int  save_write   (const char *path, const SaveFile *sf);
int  save_read    (const char *path, SaveFile *sf);

/* Helpers */
void save_init    (SaveFile *sf, const char *player, int puzzle_count);
int  save_exists  (const char *path);
void save_delete  (const char *path);

/* Sync a single puzzle result into sf->puzzles[] */
void save_set_puzzle(SaveFile *sf, int puzzle_id, int solved,
                     int score, int elapsed_sec, int hints_shown);

#endif /* SAVE_H */
