import ctypes
import os

# 載入人B編譯好的 .so
_lib_path = os.path.join(os.path.dirname(__file__), '..', 'core', 'libtcth_core.so')
_lib = ctypes.CDLL(_lib_path)

# ── 路徑 ──────────────────────────────────────────────────────────
_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'data.txt')
_SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'save.bin')

# ── C struct 對應 ─────────────────────────────────────────────────
MAX_PUZZLES = 16
HINT_COUNT  = 3

class _PuzzleStruct(ctypes.Structure):
    _fields_ = [
        ('id',              ctypes.c_int),
        ('location',        ctypes.c_char * 64),
        ('title',           ctypes.c_char * 64),
        ('question',        ctypes.c_char * 1024),
        ('answer',          ctypes.c_char * 128),
        ('hint',            (ctypes.c_char * 256) * HINT_COUNT),
        ('max_score',       ctypes.c_int),
        ('solved',          ctypes.c_int),
        ('score_earned',    ctypes.c_int),
        ('hints_unlocked',  ctypes.c_uint),
    ]

class _PuzzleSaveStruct(ctypes.Structure):
    _fields_ = [
        ('puzzle_id',   ctypes.c_int),
        ('solved',      ctypes.c_int),
        ('score',       ctypes.c_int),
        ('elapsed_sec', ctypes.c_int),
        ('hints_shown', ctypes.c_int),
    ]

class _SaveFileStruct(ctypes.Structure):
    _fields_ = [
        ('magic',          ctypes.c_char * 8),
        ('version',        ctypes.c_int),
        ('timestamp',      ctypes.c_long),
        ('player',         ctypes.c_char * 64),
        ('current_puzzle', ctypes.c_int),
        ('total_score',    ctypes.c_int),
        ('total_elapsed',  ctypes.c_int),
        ('puzzle_count',   ctypes.c_int),
        ('puzzles',        _PuzzleSaveStruct * MAX_PUZZLES),
    ]

# Timer 對應 timer.h 的 Timer struct
class _TimerStruct(ctypes.Structure):
    _fields_ = [
        ('start_epoch', ctypes.c_double),
        ('accum_sec',   ctypes.c_double),
        ('limit_sec',   ctypes.c_int),
        ('state',       ctypes.c_int),   # TimerState enum
    ]

# ── C 函式簽名：puzzle ────────────────────────────────────────────
_lib.load_puzzles.argtypes    = [ctypes.c_char_p, ctypes.POINTER(_PuzzleStruct), ctypes.c_int]
_lib.load_puzzles.restype     = ctypes.c_int

_lib.validate_answer.argtypes = [ctypes.POINTER(_PuzzleStruct), ctypes.c_char_p]
_lib.validate_answer.restype  = ctypes.c_int

_lib.unlock_hints.argtypes    = [ctypes.POINTER(_PuzzleStruct), ctypes.c_int]
_lib.unlock_hints.restype     = ctypes.c_uint

_lib.get_hint.argtypes        = [ctypes.POINTER(_PuzzleStruct), ctypes.c_int]
_lib.get_hint.restype         = ctypes.c_char_p

_lib.calc_score.argtypes      = [ctypes.c_int]
_lib.calc_score.restype       = ctypes.c_int

# ── C 函式簽名：timer ─────────────────────────────────────────────
_lib.timer_init.argtypes      = [ctypes.POINTER(_TimerStruct), ctypes.c_int]
_lib.timer_init.restype       = None

_lib.timer_start.argtypes     = [ctypes.POINTER(_TimerStruct)]
_lib.timer_start.restype      = None

_lib.timer_stop.argtypes      = [ctypes.POINTER(_TimerStruct)]
_lib.timer_stop.restype       = None

_lib.timer_elapsed_int.argtypes = [ctypes.POINTER(_TimerStruct)]
_lib.timer_elapsed_int.restype  = ctypes.c_int

_lib.timer_hints_due.argtypes = [ctypes.POINTER(_TimerStruct), ctypes.c_int]
_lib.timer_hints_due.restype  = ctypes.c_int

# ── C 函式簽名：save ──────────────────────────────────────────────
_lib.save_init.argtypes       = [ctypes.POINTER(_SaveFileStruct), ctypes.c_char_p, ctypes.c_int]
_lib.save_init.restype        = None

_lib.save_write.argtypes      = [ctypes.c_char_p, ctypes.POINTER(_SaveFileStruct)]
_lib.save_write.restype       = ctypes.c_int

_lib.save_read.argtypes       = [ctypes.c_char_p, ctypes.POINTER(_SaveFileStruct)]
_lib.save_read.restype        = ctypes.c_int

_lib.save_exists.argtypes     = [ctypes.c_char_p]
_lib.save_exists.restype      = ctypes.c_int

_lib.save_set_puzzle.argtypes = [ctypes.POINTER(_SaveFileStruct),
                                  ctypes.c_int, ctypes.c_int,
                                  ctypes.c_int, ctypes.c_int, ctypes.c_int]
_lib.save_set_puzzle.restype  = None

# ── 內部狀態 ──────────────────────────────────────────────────────
_puzzles      = (_PuzzleStruct * MAX_PUZZLES)()
_puzzle_count = 0
_save         = _SaveFileStruct()
_timers       = [_TimerStruct() for _ in range(MAX_PUZZLES)]  # 每關一個timer

# ── 初始化 ────────────────────────────────────────────────────────
def init():
    global _puzzle_count, _save
    _puzzle_count = _lib.load_puzzles(_DATA_PATH.encode(), _puzzles, MAX_PUZZLES)
    if _puzzle_count < 0:
        raise RuntimeError(f"無法載入謎題資料：{_DATA_PATH}")
    if _lib.save_exists(_SAVE_PATH.encode()):
        _lib.save_read(_SAVE_PATH.encode(), ctypes.byref(_save))
    else:
        _lib.save_init(ctypes.byref(_save), "玩家".encode('utf-8'), _puzzle_count)

# ── 人A 可以直接呼叫的函式 ────────────────────────────────────────

def start_timer(puzzle_index: int):
    """開始計時（謎題出現時呼叫）"""
    _lib.timer_init(ctypes.byref(_timers[puzzle_index]), 900)
    _lib.timer_start(ctypes.byref(_timers[puzzle_index]))

def get_elapsed(puzzle_index: int) -> int:
    """取得該關已過秒數（由C的timer計算）"""
    return _lib.timer_elapsed_int(ctypes.byref(_timers[puzzle_index]))

def check_answer(puzzle_index: int, user_input: str) -> bool:
    """驗證答案，回傳True=答對"""
    if puzzle_index < 0 or puzzle_index >= _puzzle_count:
        return False
    result = _lib.validate_answer(
        ctypes.byref(_puzzles[puzzle_index]),
        user_input.encode('utf-8'))
    return result == 0

def get_hint(puzzle_index: int, elapsed_sec: int, hint_index: int):
    """取得提示，hint_index=0/1/2"""
    if puzzle_index < 0 or puzzle_index >= _puzzle_count:
        return None
    # 強制解鎖所有提示到 hint_index
    force_elapsed = (hint_index + 1) * 241
    _lib.unlock_hints(ctypes.byref(_puzzles[puzzle_index]), force_elapsed)
    _lib.get_hint.restype = ctypes.c_char_p
    result = _lib.get_hint(ctypes.byref(_puzzles[puzzle_index]), hint_index)
    if not result:
        return None
    try:
        return result.decode('utf-8')
    except Exception:
        try:
            return result.decode('latin-1')
        except Exception:
            return None

def save_result(puzzle_index: int, hints_shown: int):
    """
    儲存該關結果，elapsed由C的timer取得，score由C的calc_score計算
    """
    _lib.timer_stop(ctypes.byref(_timers[puzzle_index]))
    elapsed = _lib.timer_elapsed_int(ctypes.byref(_timers[puzzle_index]))
    score   = _lib.calc_score(elapsed)
    puzzle_id = puzzle_index + 1
    solved    = 1 if _puzzles[puzzle_index].solved else 0
    _lib.save_set_puzzle(
        ctypes.byref(_save),
        puzzle_id, solved, score, elapsed, hints_shown)
    
    _save.total_score = sum(
        _save.puzzles[i].score 
        for i in range(_save.puzzle_count)
    )
    _save.total_elapsed += elapsed
    _save.current_puzzle = puzzle_id + 1
    _lib.save_write(_SAVE_PATH.encode(), ctypes.byref(_save))

def get_total_score() -> int:
    """回傳累積總分"""
    return _save.total_score

def load_current_puzzle() -> int:
    """回傳玩家目前應從第幾關開始（0-based）"""
    idx = _save.current_puzzle - 1
    return max(0, min(idx, _puzzle_count - 1))

def puzzle_count() -> int:
    return _puzzle_count