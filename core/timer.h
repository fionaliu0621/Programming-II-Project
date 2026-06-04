#ifndef TIMER_H
#define TIMER_H

#include <stddef.h>

typedef enum {
    TIMER_IDLE    = 0,
    TIMER_RUNNING = 1,
    TIMER_PAUSED  = 2,
    TIMER_STOPPED = 3
} TimerState;

typedef struct {
    double     start_epoch;   /* wall-clock seconds at last start/resume */
    double     accum_sec;     /* total elapsed across all run intervals   */
    int        limit_sec;     /* countdown ceiling; 0 = no limit          */
    TimerState state;
} Timer;

/* Lifecycle */
void   timer_init    (Timer *t, int limit_sec);
void   timer_start   (Timer *t);
void   timer_pause   (Timer *t);
void   timer_resume  (Timer *t);
void   timer_stop    (Timer *t);
void   timer_reset   (Timer *t);

/* Query */
double timer_elapsed        (const Timer *t);          /* seconds (float)  */
int    timer_elapsed_int    (const Timer *t);          /* seconds (int)    */
int    timer_remaining_sec  (const Timer *t);          /* -1 if no limit   */
int    timer_expired        (const Timer *t);
float  timer_pct_remaining  (const Timer *t);          /* 1.0 → 0.0        */

/* Formatting for HUD */
void   timer_fmt_elapsed    (const Timer *t, char *buf, size_t n); /* MM:SS */
void   timer_fmt_remaining  (const Timer *t, char *buf, size_t n); /* MM:SS */

/* Hint timing: returns 0/1/2/3 (number of hints due so far) */
int    timer_hints_due      (const Timer *t, int interval_sec);

#endif /* TIMER_H */
