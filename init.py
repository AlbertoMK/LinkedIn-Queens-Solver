import datetime

import cv2


def get_color_at_coordinates(image, coordenadas):
    # Verificar si la imagen se ha cargado correctamente
    if image is None:
        raise ValueError("La imagen no se pudo cargar. Verifica la ruta del archivo.")
    id_color = 0
    colores = {}
    id_cell = 0
    mapeo = {}
    for coor in coordenadas:
        x, y = coor
        b, g, r = image[y, x]
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        if hex_color not in colores.values():
            colores[id_color] = hex_color
            id_color += 1
        id_this_color = 1
        for id in colores.keys():
            if colores[id] == hex_color:
                id_this_color = id
        mapeo[id_cell] = id_this_color
        id_cell += 1
    return mapeo


def mapeo(image_path, dimension):
    image = cv2.imread(image_path)
    height, width, channels = image.shape
    coordenadas = []
    for i in range(dimension):
        for j in range(dimension):
            x = int(width / dimension * (0.5 + j))
            y = int(height / dimension * (0.5 + i))
            coordenadas.append((x, y))
    map = get_color_at_coordinates(image, coordenadas)

    matrix = [[0 for _ in range(dimension)] for _ in range(dimension)]
    for i in range(dimension):
        for j in range(dimension):
            matrix[j][i] = map[j * dimension + i]
    return matrix


def backtracking(matrix):
    n = len(matrix)
    colores = [False for _ in range(n)]
    rows = [False for _ in range(n)]
    cols = [False for _ in range(n)]
    solution = []
    index = 0
    counter = 0
    while index < n * n and len(solution) < n:
        counter += backtrack(matrix, index, colores, rows, cols, solution)
        index += 1
    print(counter)
    return solution


def backtrack(matrix, cell, colores, rows, cols, solution):
    n = len(matrix)
    row, col = divmod(cell, n)
    counter = 0
    if colores[matrix[row][col]] is False and cols[col] is False and rows[row] is False and comprobarAdyacencias(cell, solution, n):
        counter += 1
        # anotar
        colores[matrix[row][col]] = True
        rows[row] = True
        cols[col] = True
        solution.append(row * n + col)
        # comprobar
        if len(solution) is not n:
            index = cell - cell % n + n
            while index < n * n and len(solution) < n:
                counter += backtrack(matrix, index, colores, rows, cols, solution)
                index += 1
            if len(solution) < n:
                # desanotar
                colores[matrix[row][col]] = False
                rows[row] = False
                cols[col] = False
                solution.pop()
    return counter


def comprobarAdyacencias(cell, solution, dimension):
    posibilidades = []
    if getRow(cell, dimension) - getRow(cell - dimension - 1, dimension) == 1:
        posibilidades.append(cell - dimension - 1)
    if getRow(cell, dimension) - getRow(cell - dimension + 1, dimension) == 1:
        posibilidades.append(cell - dimension + 1)
    if getRow(cell, dimension) - getRow(cell + dimension - 1, dimension) == -1:
        posibilidades.append(cell + dimension - 1)
    if getRow(cell, dimension) - getRow(cell + dimension + 1, dimension) == -1:
        posibilidades.append(cell + dimension + 1)
    for p in posibilidades:
        if p in solution:
            return False
    return True


def getRow(cell, dimension):
    return int(cell / dimension)


image_path = 'img.png'
matrix = mapeo("img.png", 11)
start = datetime.datetime.now()
solution = backtracking(matrix)
end = datetime.datetime.now()
for i in range(len(matrix)):
    for j in range(len(matrix)):
        if i * len(matrix) + j in solution:
            print(" x ", end="")
        else:
            print(" _ ", end="")
    print()
print(str((end - start).total_seconds()) + "s")
