import random

class Move:
    def __init__(self, face, direction=None):
        self.face = face
        self.direction = direction
    
    def __str__(self):
        return f"{self.face}{self.direction or ''}"

class MoveList:
    def __init__(self):
        self.moves = []
    
    def add_move(self, move):
        self.moves.append(move)
    
    def get_moves(self):
        return [(move.face, move.direction) for move in self.moves]

    def __str__(self):
        return ' '.join(str(move) for move in self.moves)

class RubiksCubeCodec:
    FACES = ['R', 'L', 'U', 'D', 'F', 'B']
    DIRECTIONS = [None, "'", '2']

    @staticmethod
    def encode(data):
        move_list = MoveList()
        if not isinstance(data, bytes):
            data = str(data).encode('utf-8')
        for byte in data:
            # Introduce randomness in face selection
            face = random.choice(range(6))
            # Use the byte value to determine direction and an additional move
            direction = byte % 3
            additional_move = byte // 3
            move_list.add_move(Move(RubiksCubeCodec.FACES[face], RubiksCubeCodec.DIRECTIONS[direction]))
            move_list.add_move(Move(str(additional_move)))
        return move_list.get_moves()

    @staticmethod
    def decode(moves):
        data = bytearray()
        for i in range(0, len(moves), 2):
            face_move, additional_move = moves[i], moves[i+1]
            face = RubiksCubeCodec.FACES.index(face_move[0])
            direction = RubiksCubeCodec.DIRECTIONS.index(face_move[1])
            additional = int(additional_move[0])
            # Reconstruct the original byte
            byte_value = (additional * 3) + direction
            data.append(byte_value)
        return bytes(data)

# Example usage
original_data = "Hello, Rubik's Cube!"
print(f"Original data: {original_data}")

# Encode
encoded_moves = RubiksCubeCodec.encode(original_data)
print(f"Encoded moves: {encoded_moves}")

# Decode
decoded_data = RubiksCubeCodec.decode(encoded_moves)
print(f"Decoded data: {decoded_data.decode('utf-8')}")

# Verify
print(f"Original and decoded data match: {original_data == decoded_data.decode('utf-8')}")
