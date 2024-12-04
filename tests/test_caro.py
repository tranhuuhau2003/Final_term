import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

# ===========================
# THUẬT TOÁN MINIMAX
# ===========================

def check_winner(board):
    """Kiểm tra trạng thái chiến thắng."""
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Hàng ngang
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Hàng dọc
        [0, 4, 8], [2, 4, 6]              # Đường chéo
    ]
    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != "":
            return board[pattern[0]]  # "X" hoặc "O"
    return None

def is_draw(board):
    """Kiểm tra trận hòa."""
    return all(cell != "" for cell in board) and check_winner(board) is None

def minimax(board, depth, is_maximizing):
    """Thuật toán Minimax."""
    winner = check_winner(board)
    if winner == "X":  # Người chơi thắng
        return 10 - depth
    if winner == "O":  # Máy thắng
        return depth - 10
    if is_draw(board):  # Trận hòa
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, depth + 1, False)
                board[i] = ""
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, depth + 1, True)
                board[i] = ""
                best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    """Tìm nước đi tốt nhất."""
    best_score = -float("inf")
    best_move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "X"  # Giả sử người chơi là "X"
            score = minimax(board, 0, False)
            board[i] = ""
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# ===========================
# SELENIUM FIXTURE
# ===========================

@pytest.fixture
def browser():
    """Khởi tạo trình duyệt."""
    driver = webdriver.Chrome()
    driver.get("https://playtictactoe.org/")
    yield driver
    driver.quit()

# ===========================
# CHỨC NĂNG LẤY VÀ CHƠI TRÊN GIAO DIỆN
# ===========================

def get_board(browser):
    """Chuyển trạng thái bàn cờ từ giao diện web."""
    squares = browser.find_elements(By.CLASS_NAME, "square")
    board = []
    for square in squares:
        inner = square.find_element(By.TAG_NAME, "div").get_attribute("class")
        if inner == "x":
            board.append("X")
        elif inner == "o":
            board.append("O")
        else:
            board.append("")
    return board

def make_move(browser, move_index):
    """Thực hiện nước đi trên giao diện."""
    squares = browser.find_elements(By.CLASS_NAME, "square")
    # time.sleep(2)
    squares[move_index].click()

def play_game_until_result(browser):
    """Chơi game tự động đến khi có kết quả."""
    while True:
        # Lấy trạng thái bàn cờ
        board = get_board(browser)

        # Kiểm tra kết quả
        winner = check_winner(board)
        if winner:
            return winner
        if is_draw(board):
            return "Tie"

        # Tìm nước đi tốt nhất và thực hiện
        best_move = find_best_move(board)
        if best_move is not None:
            make_move(browser, best_move)
        time.sleep(1)

def reset_game(browser):
    """Khởi động lại trò chơi bằng cách nhấn vào nút restart."""
    restart_button = browser.find_element(By.CLASS_NAME, "restart")
    time.sleep(3)
    restart_button.click()  # Nhấn vào nút restart
    time.sleep(3)  # Đảm bảo có thời gian để game được reset

# ===========================
# TEST CASES
# ===========================

def test_player_wins(browser):
    """Kiểm thử trường hợp người chơi thắng."""
    for _ in range(10):  # Thử tối đa 10 lần
        board = get_board(browser)
        while check_winner(board) is None and not is_draw(board):
            move = find_best_move(board)
            if move is not None:
                make_move(browser, move)
            board = get_board(browser)

        winner = check_winner(board)
        if winner == "X":  # Người chơi thắng
            print("Player won!")
            return
        reset_game(browser)

    assert False, "Could not achieve player win after multiple games."

def test_game_tie(browser):
    """Kiểm thử trường hợp hòa."""
    for _ in range(10):  # Thử tối đa 10 lần
        board = get_board(browser)
        moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]  # Một chuỗi nước đi để đạt hòa
        for move in moves:
            if board[move] == "":
                make_move(browser, move)
            board = get_board(browser)

        if is_draw(board):
            print("Game ended in a tie!")
            return
        reset_game(browser)

    assert False, "Could not achieve a tie after multiple games."

def test_player_loses(browser):
    """Kiểm thử trường hợp người chơi thua."""
    for _ in range(10):  # Thử tối đa 10 lần
        board = get_board(browser)
        # Lập trình người chơi cố tình chơi sai để thua
        bad_moves = [0, 4, 1]  # Lựa chọn một chuỗi các nước đi yếu
        for move in bad_moves:
            if board[move] == "":
                make_move(browser, move)
            board = get_board(browser)

        winner = check_winner(board)
        if winner == "O":  # Máy thắng
            print("Player lost!")
            return
        reset_game(browser)

    assert False, "Could not achieve player loss after multiple games."
selenium.webdriver.common.by