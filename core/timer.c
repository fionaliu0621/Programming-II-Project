#define _POSIX_C_SOURCE 200809L
#include "timer.h"
#include <stdio.h>
#include <string.h>

/* ── platform clock ───────────────────────────────────────────── */
#ifdef _WIN32
#  include <windows.h>
static double _now(void) {
    LARGE_INTEGER f, c;
    QueryPerformanceFrequency(&f);
    QueryPerformanceCounter(&c);
    return (double)c.QuadPart / (double)f.QuadPart;
}
#else
#  include <time.h>
static double _now(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}
#endif

/* ── internal: total elapsed as double ───────────────────────── */
static double _elapsed(const Timer *t) {
    if (!t) return 0.0;
    if (t->state == TIMER_RUNNING)
        return t->accum_sec + (_now() - t->start_epoch);
    return t->accum_sec; /* PAUSED or STOPPED */
}

/* ── lifecycle ────────────────────────────────────────────────── */

void timer_init(Timer *t, int limit_sec) {
    if (!t) return;
    memset(t, 0, sizeof(Timer));
    t->limit_sec = limit_sec;
    t->state     = TIMER_IDLE;
}

void timer_start(Timer *t) {
    if (!t) return;
    t->accum_sec  = 0.0;
    t->start_epoch = _now();
    t->state       = TIMER_RUNNING;
}

void timer_pause(Timer *t) {
    if (!t || t->state != TIMER_RUNNING) return;
    t->accum_sec += _now() - t->start_epoch;
    t->state      = TIMER_PAUSED;
}

void timer_resume(Timer *t) {
    if (!t || t->state != TIMER_PAUSED) return;
    t->start_epoch = _now();
    t->state       = TIMER_RUNNING;
}

void timer_stop(Timer *t) {
    if (!t) return;
    if (t->state == TIMER_RUNNING)
        t->accum_sec += _now() - t->start_epoch;
    t->state = TIMER_STOPPED;
}

void timer_reset(Timer *t) {
    if (!t) return;
    int lim = t->limit_sec;
    timer_init(t, lim);
}

/* ── query ────────────────────────────────────────────────────── */

double timer_elapsed(const Timer *t)     { return _elapsed(t); }
int    timer_elapsed_int(const Timer *t) { return (int)_elapsed(t); }

int timer_remaining_sec(const Timer *t) {
    if (!t || t->limit_sec <= 0) return -1;
    int rem = t->limit_sec - (int)_elapsed(t);
    return rem < 0 ? 0 : rem;
}

int timer_expired(const Timer *t) {
    if (!t || t->limit_sec <= 0) return 0;
    return _elapsed(t) >= (double)t->limit_sec;
}

float timer_pct_remaining(const Timer *t) {
    if (!t || t->limit_sec <= 0) return 1.0f;
    float pct = 1.0f - (float)(_elapsed(t) / (double)t->limit_sec);
    return pct < 0.0f ? 0.0f : (pct > 1.0f ? 1.0f : pct);
}

/* ── formatting ───────────────────────────────────────────────── */

static void _fmt_sec(int total, char *buf, size_t n) {
    int m = total / 60, s = total % 60;
    snprintf(buf, n, "%02d:%02d", m < 0 ? 0 : m, s < 0 ? 0 : s);
}

void timer_fmt_elapsed  (const Timer *t, char *buf, size_t n) {
    _fmt_sec((int)_elapsed(t), buf, n);
}

void timer_fmt_remaining(const Timer *t, char *buf, size_t n) {
    _fmt_sec(timer_remaining_sec(t), buf, n);
}

/* ── hint scheduling ──────────────────────────────────────────── */

/*
 * Returns how many hints have become available.
 * e.g. at t=250s with interval=240: returns 1
 *      at t=490s with interval=240: returns 2
 */
int timer_hints_due(const Timer *t, int interval_sec) {
    if (!t || interval_sec <= 0) return 0;
    int e = (int)_elapsed(t);
    int due = e / interval_sec;
    /* cap at 3 (max hints) */
    return due > 3 ? 3 : due;
}
