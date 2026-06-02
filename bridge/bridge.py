import ctypes
import os

# 載入人B編譯好的 .so
_lib_path = os.path.join(os.path.dirname(__file__), '..', 'core', 'libtcth_core.so')
_lib = ctypes.CDLL(_lib_path)

# ── puzzles.txt 路徑 ──────────────────────────────────────────────
_DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'puzzles.txt')
_SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'save.bin')

# ── C struct 對應 ─────────────────────────────────────────────────
MAX_PUZZLES  = 16
HINT_COUNT   = 3
PUZZLE_TIME  = 900   # 15分鐘

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

# ── C 函式簽名 ────────────────────────────────────────────────────
_lib.load_puzzles.argtypes    = [ctypes.c_char_p,
                                  ctypes.POINTER(_PuzzleStruct),
                                  ctypes.c_int]
_lib.load_puzzles.restype     = ctypes.c_int

_lib.validate_answer.argtypes = [ctypes.POINTER(_PuzzleStruct),
                                  ctypes.c_char_p]
_lib.validate_answer.restype  = ctypes.c_int   # 0=CORRECT, 1=WRONG

_lib.unlock_hints.argtypes    = [ctypes.POINTER(_PuzzleStruct),
                                  ctypes.c_int]
_lib.unlock_hints.restype     = ctypes.c_uint

_lib.get_hint.argtypes        = [ctypes.POINTER(_PuzzleStruct),
                                  ctypes.c_int]
_lib.get_hint.restype         = ctypes.c_char_p

_lib.calc_score.argtypes      = [ctypes.c_int]
_lib.calc_score.restype       = ctypes.c_int

_lib.save_init.argtypes       = [ctypes.POINTER(_SaveFileStruct),
                                  ctypes.c_char_p,
                                  ctypes.c_int]
_lib.save_init.restype        = None

_lib.save_write.argtypes      = [ctypes.c_char_p,
                                  ctypes.POINTER(_SaveFileStruct)]
_lib.save_write.restype       = ctypes.c_int

_lib.save_read.argtypes       = [ctypes.c_char_p,
                                  ctypes.POINTER(_SaveFileStruct)]
_lib.save_read.restype        = ctypes.c_int

_lib.save_exists.argtypes     = [ctypes.c_char_p]
_lib.save_exists.restype      = ctypes.c_int

_lib.save_set_puzzle.argtypes = [ctypes.POINTER(_SaveFileStruct),
                                  ctypes.c_int, ctypes.c_int,
                                  ctypes.c_int, ctypes.c_int,
                                  ctypes.c_int]
_lib.save_set_puzzle.restype  = None

# ── 內部狀態 ──────────────────────────────────────────────────────
_puzzles     = (_PuzzleStruct * MAX_PUZZLES)()
_puzzle_count = 0
_save        = _SaveFileStruct()

# ── 初始化：讀謎題 + 讀存檔 ──────────────────────────────────────
def init():
    """遊戲開始時呼叫一次。載入謎題資料與存檔。"""
    global _puzzle_count, _save
    _puzzle_count = _lib.load_puzzles(
        _DATA_PATH.encode(), _puzzles, MAX_PUZZLES)
    if _puzzle_count < 0:
        raise RuntimeError(f"無法載入謎題資料：{_DATA_PATH}")

    if _lib.save_exists(_SAVE_PATH.encode()):
        _lib.save_read(_SAVE_PATH.encode(), ctypes.byref(_save))
    else:
        _lib.save_init(ctypes.byref(_save),
                       "玩家".encode('utf-8'), _puzzle_count)

# ── 人A 可以直接呼叫的函式 ────────────────────────────────────────

def check_answer(puzzle_index: int, user_input: str) -> bool:
    """
    驗證玩家答案。
    puzzle_index: 0-based（第一關=0）
    回傳 True=答對, False=答錯
    """
    if puzzle_index < 0 or puzzle_index >= _puzzle_count:
        return False
    result = _lib.validate_answer(
        ctypes.byref(_puzzles[puzzle_index]),
        user_input.encode('utf-8'))
    return result == 0  # 0 = PUZZLE_CORRECT

def get_hint(puzzle_index: int, elapsed_sec: int, hint_index: int):
    """
    取得提示文字。
    elapsed_sec: 該關已經過幾秒
    hint_index: 0/1/2（第幾個提示）
    回傳提示字串，若尚未解鎖則回傳 None
    """
    if puzzle_index < 0 or puzzle_index >= _puzzle_count:
        return None
    _lib.unlock_hints(
        ctypes.byref(_puzzles[puzzle_index]), elapsed_sec)
    result = _lib.get_hint(
        ctypes.byref(_puzzles[puzzle_index]), hint_index)
    return result.decode('utf-8') if result else None

def get_score(elapsed_sec: int) -> int:
    """根據花費秒數回傳分數（4/3/2/1/0）"""
    return _lib.calc_score(elapsed_sec)

def get_location(puzzle_index: int) -> str:
    """回傳該關地點名稱"""
    if puzzle_index < 0 or puzzle_index >= _puzzle_count:
        return ""
    return _puzzles[puzzle_index].location.decode('utf-8')

def get_question(puzzle_index: int) -> str:
    """回傳該關題目說明"""
    if puzzle_index < 0 or puzzle_index >= _puzzle_count:
        return ""
    return _puzzles[puzzle_index].question.decode('utf-8')

def save_result(puzzle_index: int, elapsed_sec: int, hints_shown: int):
    """
    儲存該關結果到存檔。
    hints_shown: bitmask，哪些提示被看過（bit0=hint1, bit1=hint2, bit2=hint3）
    """
    puzzle_id = puzzle_index + 1
    solved    = 1 if _puzzles[puzzle_index].solved else 0
    score     = _lib.calc_score(elapsed_sec)
    _lib.save_set_puzzle(
        ctypes.byref(_save),
        puzzle_id, solved, score, elapsed_sec, hints_shown)
    _save.total_score    += score
    _save.total_elapsed  += elapsed_sec
    _save.current_puzzle  = puzzle_id + 1
    _lib.save_write(_SAVE_PATH.encode(), ctypes.byref(_save))

def load_current_puzzle() -> int:
    """回傳玩家目前應該從第幾關開始（0-based）"""
    idx = _save.current_puzzle - 1
    return max(0, min(idx, _puzzle_count - 1))

def get_total_score() -> int:
    """回傳目前累積總分"""
    return _save.total_score

def puzzle_count() -> int:
    """回傳總關數"""
    return _puzzle_count
