#Not sure if this is right or not, but a starting step.
#(C)Tsubasa Kato - Inspire Search - 9/16/2024 8:36AM JST
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Cube4x4x4:
    def __init__(self):
        self.colors = {
            'U': 'white',
            'D': 'yellow',
            'F': 'blue',
            'B': 'green',
            'L': 'orange',
            'R': 'red'
        }
        self.size = 4
        self.cube = self._create_solved_cube()

    def _create_solved_cube(self):
        cube = {}
        for x in range(self.size):
            for y in range(self.size):
                for z in range(self.size):
                    cubie = {}
                    if x == 0:
                        cubie['L'] = self.colors['L']
                    if x == self.size - 1:
                        cubie['R'] = self.colors['R']
                    if y == 0:
                        cubie['D'] = self.colors['D']
                    if y == self.size - 1:
                        cubie['U'] = self.colors['U']
                    if z == 0:
                        cubie['B'] = self.colors['B']
                    if z == self.size - 1:
                        cubie['F'] = self.colors['F']
                    cube[(x, y, z)] = cubie
        return cube

    def apply_move(self, face, layer=0, direction=''):
        num_rotations = {'': 1, "'": -1, '2': 2}[direction]
        for _ in range(num_rotations % 4):
            self._rotate_layer(face, layer)

    def _rotate_layer(self, face, layer):
        if face == 'U':
            indices = [(x, self.size - 1 - layer, z) for x in range(self.size) for z in range(self.size)]
            axis = 'y'
            k = 1
        elif face == 'D':
            indices = [(x, layer, z) for x in range(self.size) for z in range(self.size)]
            axis = 'y'
            k = -1
        elif face == 'F':
            indices = [(x, y, self.size - 1 - layer) for x in range(self.size) for y in range(self.size)]
            axis = 'z'
            k = 1
        elif face == 'B':
            indices = [(x, y, layer) for x in range(self.size) for y in range(self.size)]
            axis = 'z'
            k = -1
        elif face == 'R':
            indices = [(self.size - 1 - layer, y, z) for y in range(self.size) for z in range(self.size)]
            axis = 'x'
            k = 1
        elif face == 'L':
            indices = [(layer, y, z) for y in range(self.size) for z in range(self.size)]
            axis = 'x'
            k = -1
        else:
            raise ValueError("Invalid face")

        # Extract the layer to be rotated
        layer_cubies = {idx: self.cube[idx] for idx in indices}

        # Rotate the layer indices
        rotated_indices = self._rotate_indices(indices, axis, k)

        # Create a copy of the cube to prevent overwriting
        cube_copy = self.cube.copy()

        # Map the rotated cubies back to the cube
        for orig_idx, new_idx in zip(indices, rotated_indices):
            cube_copy[new_idx] = self._rotate_cubie(layer_cubies[orig_idx], axis, k)

        # Update the cube after all rotations
        for idx in indices:
            self.cube[idx] = cube_copy[idx]

    def _rotate_indices(self, indices, axis, k):
        rotated = []
        for idx in indices:
            x, y, z = idx
            if axis == 'x':
                y, z = self._rotate_coords(y, z, k)
            elif axis == 'y':
                x, z = self._rotate_coords(x, z, k)
            elif axis == 'z':
                x, y = self._rotate_coords(x, y, k)
            rotated.append((x, y, z))
        return rotated

    def _rotate_coords(self, a, b, k):
        if k == 1:
            return b, self.size - 1 - a
        elif k == -1:
            return self.size - 1 - b, a
        elif k == 2:
            return self.size - 1 - a, self.size - 1 - b

    def _rotate_cubie(self, cubie, axis, k):
        new_cubie = {}
        for face in cubie:
            new_face = self._map_face(face, axis, k)
            new_cubie[new_face] = cubie[face]
        return new_cubie

    def _map_face(self, face, axis, k):
        face_order = {
            'x': ['U', 'B', 'D', 'F'],
            'y': ['F', 'R', 'B', 'L'],
            'z': ['U', 'L', 'D', 'R'],
        }
        if face in face_order[axis]:
            idx = face_order[axis].index(face)
            new_face = face_order[axis][(idx + k) % 4]
            return new_face
        else:
            return face

    def visualize(self, title=""):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Sort the cubies to draw back ones first
        sorted_cubies = sorted(self.cube.items(), key=lambda item: (item[0][1], item[0][2], item[0][0]))

        for idx, cubie in sorted_cubies:
            x, y, z = idx
            for face in cubie:
                color = cubie[face]
                self._draw_face(ax, x, y, z, face, color)

        ax.set_xlim([0, self.size])
        ax.set_ylim([0, self.size])
        ax.set_zlim([0, self.size])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.title(title)
        plt.show()

    def _draw_face(self, ax, x, y, z, face, color):
        if face == 'U':
            verts = [
                [x, y + 1, z],
                [x + 1, y + 1, z],
                [x + 1, y + 1, z + 1],
                [x, y + 1, z + 1]
            ]
        elif face == 'D':
            verts = [
                [x, y, z],
                [x, y, z + 1],
                [x + 1, y, z + 1],
                [x + 1, y, z]
            ]
        elif face == 'F':
            verts = [
                [x, y, z + 1],
                [x + 1, y, z + 1],
                [x + 1, y + 1, z + 1],
                [x, y + 1, z + 1]
            ]
        elif face == 'B':
            verts = [
                [x, y, z],
                [x, y + 1, z],
                [x + 1, y + 1, z],
                [x + 1, y, z]
            ]
        elif face == 'L':
            verts = [
                [x, y, z],
                [x, y, z + 1],
                [x, y + 1, z + 1],
                [x, y + 1, z]
            ]
        elif face == 'R':
            verts = [
                [x + 1, y, z],
                [x + 1, y + 1, z],
                [x + 1, y + 1, z + 1],
                [x + 1, y, z + 1]
            ]
        else:
            return

        square = Poly3DCollection([verts], alpha=1.0)
        square.set_facecolor(color)
        square.set_edgecolor('black')
        ax.add_collection3d(square)

# Example usage:
cube = Cube4x4x4()

# Visualize initial state
cube.visualize("Initial State")

# Define moves: (face, layer, direction)
moves = [
    ('U', 0, ''),
    ('U', 1, ''),
    ('R', 0, "'"),
    ('R', 1, "'"),
    ('F', 0, '2'),
    ('F', 1, '2'),
]

# Apply moves and visualize
for i, move in enumerate(moves, start=1):
    face, layer, direction = move
    cube.apply_move(face, layer, direction)
    layer_str = str(layer + 1) if layer > 0 else ''
    cube.visualize(f"Step {i}: Move {face}{layer_str}{direction}")
