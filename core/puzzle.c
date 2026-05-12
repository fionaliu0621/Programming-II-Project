#include "puzzle.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

/* ── helpers ──────────────────────────────────────────────────── */

/* In-place: strip leading/trailing whitespace, uppercase everything */
static void normalise(char *s, size_t cap) {
    /* leading spaces */
    char *p = s;
    while (*p && isspace((unsigned char)*p)) p++;
    if (p != s) memmove(s, p, strlen(p) + 1);

    /* trailing spaces */
    size_t len = strlen(s);
    while (len > 0 && isspace((unsigned char)s[len - 1])) s[--len] = '\0';

    /* uppercase, in-place */
    for (size_t i = 0; s[i] && i < cap - 1; i++)
        s[i] = (char)toupper((unsigned char)s[i]);
}

/* Parse a pipe-delimited line using strtok */
static int parse_line(char *line, Puzzle *p) {
    char *tok;
    char tmp[2048];
    strncpy(tmp, line, sizeof(tmp) - 1);
    tmp[sizeof(tmp) - 1] = '\0';

    /* ID */
    tok = strtok(tmp, "|"); if (!tok) return -1;
    p->id = atoi(tok);

    /* location */
    tok = strtok(NULL, "|"); if (!tok) return -1;
    strncpy(p->location, tok, sizeof(p->location) - 1);

    /* title */
    tok = strtok(NULL, "|"); if (!tok) return -1;
    strncpy(p->title, tok, sizeof(p->title) - 1);

    /* question */
    tok = strtok(NULL, "|"); if (!tok) return -1;
    strncpy(p->question, tok, sizeof(p->question) - 1);

    /* answer — normalise immediately */
    tok = strtok(NULL, "|"); if (!tok) return -1;
    strncpy(p->answer, tok, sizeof(p->answer) - 1);
    normalise(p->answer, sizeof(p->answer));

    /* three hints */
    for (int i = 0; i < HINT_COUNT; i++) {
        tok = strtok(NULL, "|");
        if (tok) strncpy(p->hint[i], tok, sizeof(p->hint[i]) - 1);
        else     strncpy(p->hint[i], "（無提示）", sizeof(p->hint[i]) - 1);
    }

    /* max score */
    tok = strtok(NULL, "|");
    p->max_score = tok ? atoi(tok) : MAX_SCORE;

    return 0;
}

/* ── public API ───────────────────────────────────────────────── */

int load_puzzles(const char *path, Puzzle out[], int max) {
    FILE *fp = fopen(path, "r");
    if (!fp) { fprintf(stderr, "[puzzle] Cannot open %s\n", path); return -1; }

    int count = 0;
    char line[2048];

    while (fgets(line, sizeof(line), fp) && count < max) {
        /* strip newline */
        size_t len = strlen(line);
        while (len > 0 && (line[len-1] == '\n' || line[len-1] == '\r'))
            line[--len] = '\0';

        /* skip comments and blank lines */
        if (len == 0 || line[0] == '#') continue;

        memset(&out[count], 0, sizeof(Puzzle));
        if (parse_line(line, &out[count]) == 0)
            count++;
    }

    fclose(fp);
    return count;
}

PuzzleResult validate_answer(Puzzle *p, const char *user_input) {
    if (!p || !user_input) return PUZZLE_WRONG;

    char user[256];
    strncpy(user, user_input, sizeof(user) - 1);
    user[sizeof(user) - 1] = '\0';
    normalise(user, sizeof(user));

    /* also normalise commas (handle "25, 121" → "25,121") */
    /* remove spaces adjacent to commas */
    char cleaned[256]; int j = 0;
    for (int i = 0; user[i] && j < (int)sizeof(cleaned) - 1; i++) {
        if (user[i] == ' ' && j > 0 && (cleaned[j-1] == ',' ))
            continue; /* skip space after comma */
        if (user[i] == ',' && j > 0 && cleaned[j-1] == ' ')
            { cleaned[--j] = ','; j++; continue; } /* eat space before comma */
        cleaned[j++] = user[i];
    }
    cleaned[j] = '\0';

    if (strcmp(cleaned, p->answer) == 0) {
        p->solved = 1;
        return PUZZLE_CORRECT;
    }
    return PUZZLE_WRONG;
}

/*
 * Scoring rule (from spec):
 *   0  – 240s  → 4 pts
 *   241– 480s  → 3 pts
 *   481– 720s  → 2 pts
 *   721– 900s  → 1 pt
 *   > 900      → 0
 */
int calc_score(int elapsed_sec) {
    if (elapsed_sec < 0)             return 0;
    if (elapsed_sec <= HINT_INTERVAL * 1) return MAX_SCORE;
    if (elapsed_sec <= HINT_INTERVAL * 2) return MAX_SCORE - 1;
    if (elapsed_sec <= HINT_INTERVAL * 3) return MAX_SCORE - 2;
    if (elapsed_sec <= PUZZLE_TIME_SEC)   return 1;
    return 0;
}

HintMask unlock_hints(Puzzle *p, int elapsed_sec) {
    if (!p) return 0;
    HintMask mask = 0;
    for (int i = 0; i < HINT_COUNT; i++) {
        if (elapsed_sec >= HINT_INTERVAL * (i + 1))
            mask |= (1u << i);
    }
    p->hints_unlocked = mask;
    return mask;
}

const char *get_hint(const Puzzle *p, int hint_index) {
    if (!p || hint_index < 0 || hint_index >= HINT_COUNT) return NULL;
    if (!(p->hints_unlocked & (1u << hint_index)))        return NULL;
    return p->hint[hint_index];
}

void print_puzzle(const Puzzle *p) {
    if (!p) return;
    printf("[#%d] %s — %s\n", p->id, p->location, p->title);
    printf("  Solved: %s | Score: %d | Hints: 0x%x\n",
           p->solved ? "YES" : "NO", p->score_earned, p->hints_unlocked);
}
