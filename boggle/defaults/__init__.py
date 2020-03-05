from .game import read_from_file

# Read dictionary.txt and test_board.txt into other modules
DEFAULT_BOARD = read_from_file("boggle/defaults/test_board.txt", type="str")
DICTIONARY = read_from_file("boggle/defaults/dictionary.txt", type="set")
