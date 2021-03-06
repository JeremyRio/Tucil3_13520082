from heapq import heappop, heappush
import time


class PuzzleNode:
    """
    Kelas PuzzleNode untuk menyimpan matriks puzzle,
    depth, g_cost, dan parent dari PuzzleNode
    """

    # instansiasi variabel g_cost
    g_cost = 999

    def __init__(self, puzzle_board, depth, parent):
        self.puzzle_board = puzzle_board.copy()
        self.depth = depth
        self.parent = parent


def ReadFileGUI(file_name):
    """
    Membaca file matriks puzle dan memasukkannya ke dalam list puzzle_board (untuk GUI)
    """
    puzzle_board = []
    for raw_lines in open(file_name, 'r'):
        lines = raw_lines.replace("\n", "").split()
        for line in lines:
            puzzle_board.append(int(line))
    return puzzle_board


def ReadFile():
    """
    Membaca file matriks puzzle dan memasukkannya ke dalam list puzzle_board
    """
    while True:
        try:
            puzzle_board = []
            filename = input("Masukkan nama file (tanpa .txt): ")
            for raw_lines in open("../test/" + filename + ".txt", 'r'):
                lines = raw_lines.replace("\n", "").split()
                for line in lines:
                    puzzle_board.append(int(line))
            return puzzle_board
        except:
            print("Nama file tidak ditemukan, ulangi")


def PrintPuzzle(puzzle_board):
    """
    Mencetak list puzzle_board ke layar dalam bentuk puzzle matriks
    """
    for i in range(16):
        print("|" + str(puzzle_board[i]).ljust(2), end="")
        if i % 4 == 3:
            print("|")


def GetX(idx):
    """
    Mendapatkan nilai X untuk penjumlahan Kurang(i) + X
    """
    list_x = [1, 3, 4, 6, 9, 11, 12, 14]
    if idx in list_x:
        return 1
    else:
        return 0


def GetListKurangAndSum(puzzle_board):
    """
    Mendapatkan semua nilai Kurang(i) dan total nilai Kurang(i) + X
    """
    list_kurang = []
    kurang_sum = 0
    for i in range(1, 17):
        count = 0
        i_idx = puzzle_board.index(i)
        for j in range(i_idx+1, 16):
            if(i > puzzle_board[j]):
                count += 1
        list_kurang.append(count)
        kurang_sum += count
    kurang_sum += GetX(i_idx)
    return kurang_sum, list_kurang


def Get_g_cost(puzzle_board):
    """
    Menghitung jumlah ubin tidak kosong dalam list puzzle_board yang tidak berada pada tempat sesuai susunan akhir (goal state)
    """
    cost = 0
    for i in range(15):
        if(i+1 != puzzle_board[i]):
            cost += 1
    return cost


def Swap(puzzle_board, idx1, idx2):
    """
    Menukar nilai idx1 dan idx2 pada list puzzle_board
    """
    puzzle_board[idx1], puzzle_board[idx2] = puzzle_board[idx2], puzzle_board[idx1]


def GetPossibleNodes(node_count, prioq_bnb, puzzle_node):
    """
    Mengembalikan semua simpul yang dapat dibangkitkan dari puzzle_node
    serta mengembalikan jumlah simpul yang dibangkitkan
    """
    empty_idx = puzzle_node.puzzle_board.index(16)
    puzzle_board = puzzle_node.puzzle_board
    new_depth = puzzle_node.depth + 1

    # Menambahkan simpul state ketika ubin kosong digeser ke arah kanan
    if ((empty_idx + 1) % 4 != 0):
        node_count += 1
        new_node = PuzzleNode(puzzle_board, new_depth, puzzle_board)
        Swap(new_node.puzzle_board, empty_idx, empty_idx + 1)
        new_node.g_cost = Get_g_cost(new_node.puzzle_board)
        heappush(prioq_bnb, (new_depth + new_node.g_cost, node_count, new_node))

    # Menambahkan simpul state ketika ubin kosong digeser ke arah kiri
    if(empty_idx % 4 != 0):
        node_count += 1
        new_node = PuzzleNode(puzzle_board, new_depth, puzzle_board)
        Swap(new_node.puzzle_board, empty_idx, empty_idx - 1)
        new_node.g_cost = Get_g_cost(new_node.puzzle_board)
        heappush(prioq_bnb, (new_depth + new_node.g_cost, node_count, new_node))

    # Menambahkan simpul state ketika ubin kosong digeser ke arah atas
    if(empty_idx - 3 > 0):
        node_count += 1
        new_node = PuzzleNode(puzzle_board, new_depth, puzzle_board)
        Swap(new_node.puzzle_board, empty_idx, empty_idx - 4)
        new_node.g_cost = Get_g_cost(new_node.puzzle_board)
        heappush(prioq_bnb, (new_depth + new_node.g_cost, node_count, new_node))

    # Menambahkan simpul state ketika ubin kosong digeser ke arah bawah
    if(empty_idx + 3 < 15):
        node_count += 1
        new_node = PuzzleNode(puzzle_board, new_depth, puzzle_board)
        Swap(new_node.puzzle_board, empty_idx, empty_idx + 4)
        new_node.g_cost = Get_g_cost(new_node.puzzle_board)
        heappush(prioq_bnb, (new_depth + new_node.g_cost, node_count, new_node))

    return node_count


def BranchAndBoundSolve(puzzle_board):
    """
    Algoritma Branch And Bound untuk mencari solusi dari 15 Puzzle
    """
    prioq_bnb = []
    node_path = {}
    node_count = 0
    current_node = PuzzleNode(puzzle_board, 0, "ROOT")
    g_cost = Get_g_cost(puzzle_board)
    if g_cost != 0:
        node_count = GetPossibleNodes(node_count, prioq_bnb, current_node)
        current_node = heappop(prioq_bnb)[2]

    # Dilakukan iterasi sampai semua ubin yang tidak kosong dalam list puzzle_board
    # sesuai pada tempatnya (goal node)
    while g_cost != 0:
        if(str(current_node.puzzle_board) not in node_path):
            node_path[str(current_node.puzzle_board)
                      ] = current_node.parent
            node_count = GetPossibleNodes(node_count, prioq_bnb, current_node)
        current_node = heappop(prioq_bnb)[2]
        g_cost = current_node.g_cost

    if (str(current_node.puzzle_board) != str(puzzle_board)):
        node_path[str(current_node.puzzle_board)] = current_node.parent
    return current_node.puzzle_board, node_path, node_count
