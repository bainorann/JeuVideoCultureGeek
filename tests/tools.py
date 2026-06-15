import sys


def txt_to_tiles(filepath):
    with open(filepath) as f:
        lines = [line.rstrip("\n") for line in f.readlines()]

    while len(lines) % 8 != 0:
        lines.append("")

    width = max(len(line) for line in lines)
    width = ((width + 15) // 16) * 16
    lines = [line.ljust(width) for line in lines]

    tiles_x = width // 16
    tiles_y = len(lines) // 8
    tiles = [[[] for _ in range(tiles_y)] for _ in range(tiles_x)]

    for tx in range(tiles_x):
        for ty in range(tiles_y):
            x0, y0 = tx * 16, ty * 8
            tile = [lines[y0 + dy][x0 : x0 + 16] for dy in range(8)]
            tiles[tx][ty] = tile

    return tiles


def tiles_to_py(tiles, name_prefix="room"):
    lines = []
    tiles_x = len(tiles)
    tiles_y = len(tiles[0])

    for tx in range(tiles_x):
        for ty in range(tiles_y):
            tile = tiles[tx][ty]
            name = f"{name_prefix}_{tx}_{ty}"

            lines.append(f'{name} = r"""')
            for row in tile:
                lines.append(row)
            lines.append('"""')
            lines.append("")

            mat_name = f"{name}_mat"
            lines.append(f"{mat_name} = [")
            for x in range(16):
                row_vals = []
                for y in range(8):
                    row_vals.append("1" if tile[y][x] != " " else "0")
                lines.append(f"    [{', '.join(row_vals)}],")
            lines.append("]")
            lines.append("")

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python tests/tools.py <input_file>")
        sys.exit(1)
    tiles = txt_to_tiles(sys.argv[1])
    print(tiles_to_py(tiles))
