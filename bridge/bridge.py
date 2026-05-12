import ctypes
import os

lib = ctypes.CDLL(os.path.join(os.path.dirname(__file__), '../core/puzzle.so'))

# 對應人B的C函式
lib.check_answer.argtypes = [ctypes.c_int, ctypes.c_char_p]
lib.check_answer.restype = ctypes.c_int

lib.get_hint.argtypes = [ctypes.c_int, ctypes.c_int]
lib.get_hint.restype = ctypes.c_char_p

lib.save_progress.argtypes = [ctypes.c_int, ctypes.c_int]
lib.save_progress.restype = None

lib.load_progress.argtypes = []
lib.load_progress.restype = ctypes.c_int

lib.get_score.argtypes = [ctypes.c_int]
lib.get_score.restype = ctypes.c_int

# 包裝成人A可以直接呼叫的函式
def check_answer(puzzle_id, user_input):
    return lib.check_answer(puzzle_id, user_input.encode())

def get_hint(puzzle_id, hint_level):
    result = lib.get_hint(puzzle_id, hint_level)
    return result.decode() if result else ""

def save_progress(puzzle_id, score):
    lib.save_progress(puzzle_id, score)

def load_progress():
    return lib.load_progress()

def get_score(puzzle_id):
    return lib.get_score(puzzle_id)
