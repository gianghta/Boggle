from cytoolz.itertoolz import partition


def parse_matrix(board, *, board_width=4):
    """Split a string of characters (separated by commas) into a 4x4 matrix."""
    arr = [item.strip() for item in board.split(",")]
    return [list(item) for item in partition(board_width, arr)]


def calculate_word_points(word):
    return len(word)


def exist(board, word):
    def dfs(board, x, y, word):
        if len(word) == 0:
            return True
        if x < 0 or y < 0 or x >= len(board) or y >= len(board[0]):
            return False

        # Check for wildcard symbol - right now only works with 'dug','hug', 'tide'
        # Does not work with unorganized word
        if word[0] != board[x][y]:
            if board[x][y] != "*":
                return False

        tmp = board[x][y]
        board[x][y] = ""
        ans = (
            dfs(board, x + 1, y, word[1:])
            or dfs(board, x - 1, y, word[1:])
            or dfs(board, x, y + 1, word[1:])
            or dfs(board, x, y - 1, word[1:])
            or dfs(board, x + 1, y + 1, word[1:])
            or dfs(board, x - 1, y - 1, word[1:])
            or dfs(board, x - 1, y + 1, word[1:])
            or dfs(board, x + 1, y - 1, word[1:])
        )
        board[x][y] = tmp
        return ans

    if not board:
        return False

    word = word.upper()

    for x in range(len(board)):
        for y in range(len(board[0])):
            if dfs(board, x, y, word):
                return True
    return False
