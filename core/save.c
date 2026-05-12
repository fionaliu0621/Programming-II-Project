#include "save.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define SAVE_VERSION 1

void save_init(SaveFile *sf, const char *player, int puzzle_count) {
    memset(sf, 0, sizeof(SaveFile));
    strncpy(sf->magic, SAVE_FILE_MAGIC, sizeof(sf->magic) - 1);
    sf->version        = SAVE_VERSION;
    sf->timestamp      = (long)time(NULL);
    sf->current_puzzle = 1;
    sf->puzzle_count   = puzzle_count;
    strncpy(sf->player, player ? player : "玩家", sizeof(sf->player) - 1);
}

int save_write(const char *path, const SaveFile *sf) {
    FILE *fp = fopen(path, "wb");
    if (!fp) { fprintf(stderr, "[save] write failed: %s\n", path); return -1; }

    SaveFile out = *sf;
    out.timestamp = (long)time(NULL); /* always refresh on write */
    fwrite(&out, sizeof(SaveFile), 1, fp);
    fclose(fp);
    return 0;
}

int save_read(const char *path, SaveFile *sf) {
    FILE *fp = fopen(path, "rb");
    if (!fp) { fprintf(stderr, "[save] read failed: %s\n", path); return -1; }

    size_t _r = fread(sf, sizeof(SaveFile), 1, fp); (void)_r;
    fclose(fp);

    /* integrity check */
    if (strncmp(sf->magic, SAVE_FILE_MAGIC, 6) != 0) {
        fprintf(stderr, "[save] bad magic in %s\n", path);
        return -1;
    }
    if (sf->version != SAVE_VERSION) {
        fprintf(stderr, "[save] incompatible version %d\n", sf->version);
        return -1;
    }
    return 0;
}

int save_exists(const char *path) {
    FILE *fp = fopen(path, "rb");
    if (!fp) return 0;
    fclose(fp);
    return 1;
}

void save_delete(const char *path) { remove(path); }

void save_set_puzzle(SaveFile *sf, int puzzle_id, int solved,
                     int score, int elapsed_sec, int hints_shown) {
    if (!sf) return;
    for (int i = 0; i < sf->puzzle_count && i < MAX_PUZZLES; i++) {
        if (sf->puzzles[i].puzzle_id == puzzle_id ||
            sf->puzzles[i].puzzle_id == 0) {
            sf->puzzles[i].puzzle_id  = puzzle_id;
            sf->puzzles[i].solved     = solved;
            sf->puzzles[i].score      = score;
            sf->puzzles[i].elapsed_sec = elapsed_sec;
            sf->puzzles[i].hints_shown = hints_shown;
            return;
        }
    }
}
