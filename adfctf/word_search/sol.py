from pwn import *
import re
import numpy as np

ROWS=15
COLUMNS=15

def init_game(p):
    p.recvuntil("Remaining words:\n", drop=True)
    words = p.recvuntil("  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14\n", drop=True)
    words = words.decode().split("\n")[:-1]

    grid = p.recvuntil("Input start coordinate of word, e.g: 1, 2 for row 1 column 2\n", drop=True).decode()
    grid = "".join(re.findall("[a-z]+", grid))
    grid_array = []
    curr_row = []

    row_index = 0
    for i in range(len(grid)):
        curr_row_index = i // ROWS
        if row_index != curr_row_index:
            grid_array.append(curr_row)
            curr_row = []
            row_index = curr_row_index

        curr_row.append(grid[i])
    grid_array.append(curr_row)

    print("Words")
    for word in words:
        print(word)

    print("GRID")
    for x in grid_array:
        for y in x:
            print(y, end=" ")
        print()
    return words, np.array(grid_array)

# def get_dir_array(node_1, node_2):
#     node_1_r = node_1 // COLUMNS
#     node_1_c = node_1 % COLUMNS
#
#     node_2_r = node_2 // COLUMNS
#     node_2_c = node_2 % COLUMNS
#
#     dir_array = np.zeros((3,3), dtype=int)
#
#     dir_r_index = node_1_r - node_2_r
#     dir_c_index = node_1_c - node_2_c
#
#     dir_array[dir_r_index][dir_c_index] = 1
#     return dir_array

        # p.sendline(s_index)
        # p.recvline()
        # p.sendline(e_index)
        # if word != words[-1]:
        #     p.recvuntil("Input start coordinate of word, e.g: 1, 2 for row 1 column 2\n", drop=True).decode()

def find_indexes(i, j, word, letter_grid):
    len_word = len(word)
    start_i = i
    start_j = j
    d_search_i = [-1, 2]
    d_search_j = [-1, 2]

    # if j+1 < len(word):
    #     d_search_j[0] = 0
    # if COLUMNS - j < len(word):
    #     d_search_j[1] = 0
    # if i+1 < len(word):
    #     d_search_i[0] = 0
    # if ROWS - i < len(word):
    #     d_search_i[1] = 0

    dir_checks = []
    for row_offset in range(*d_search_i):
        for col_offset in range(*d_search_j):
            if row_offset == 0 and col_offset == 0: continue
            try:
                if letter_grid[i + row_offset][j + col_offset] == word[1]:
                    dir_checks.append([row_offset, col_offset])
            except:
                continue

    if len(dir_checks) == 0: return None, None

    for dir_check in dir_checks:
        found_letters = word[:2]
        i, j = start_i + dir_check[0], start_j+dir_check[1]
        word_index = 2
        while len(found_letters) < len_word:
            i, j = i + dir_check[0], j+dir_check[1]
            try:
                if letter_grid[i][j] != word[word_index]:
                    break
            except:
                break
            found_letters = found_letters + word[word_index]
            word_index += 1

        if len(found_letters) == len_word:
            return "{}, {}".format(start_i, start_j), "{}, {}".format(i, j)

    return None, None


def solve(p, words, letter_grid):
    first_letter_map = {}
    for word in words:
        first_letter_map[word[0]] = first_letter_map.get(word[0], []) + [word]

    for i in range(ROWS):
        for j in range(COLUMNS):
            # print(i,j)
            l = letter_grid[i][j]

            if l in first_letter_map:
                l_words = first_letter_map[l]

                new_l_words = []
                for word in l_words:
                    s_index, e_index = find_indexes(i,j, word, letter_grid)
                    if s_index == None:
                        new_l_words.append(word)
                        continue
                    print("Found Word:", word, s_index, e_index)
                    p.sendline(s_index)
                    p.recvline()
                    p.sendline(e_index)
                    words.remove(word)

                    if len(words) > 0:
                        p.recvuntil("Input start coordinate of word, e.g: 1, 2 for row 1 column 2\n", drop=True).decode()
                    else:
                        try:
                            for _i in range(100):
                                print(p.recvline().decode(), end="")
                        except:
                            pass
                        return
                first_letter_map[l] = new_l_words
    print("Missing words")
    for word in words:
        print(word)

def main():
    p = remote("word-search.ctf.fifthdoma.in", 4243)
    words, letter_grid = init_game(p)
    solve(p, words, letter_grid)

if __name__ == "__main__":
    main()
