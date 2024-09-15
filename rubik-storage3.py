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
            face = byte // 48  # 0-5 for faces
            direction = (byte % 48) // 16  # 0-2 for directions
            layer = byte % 16  # 0-15 for layers
            move_list.add_move(Move(RubiksCubeCodec.FACES[face], RubiksCubeCodec.DIRECTIONS[direction]))
            move_list.add_move(Move(str(layer)))
        return move_list.get_moves()

    @staticmethod
    def decode(moves):
        data = bytearray()
        for i in range(0, len(moves), 2):
            face_move, layer_move = moves[i], moves[i+1]
            face = RubiksCubeCodec.FACES.index(face_move[0])
            direction = RubiksCubeCodec.DIRECTIONS.index(face_move[1])
            layer = int(layer_move[0])
            byte_value = (face * 48) + (direction * 16) + layer
            data.append(byte_value)
        return bytes(data)

# Example usage
original_data = "meow, meow, meo, ewo"
print(f"Original data: {original_data}")

# Encode
encoded_moves = RubiksCubeCodec.encode(original_data)
print(f"Encoded moves: {encoded_moves}")

# Decode
decoded_data = RubiksCubeCodec.decode(encoded_moves)
print(f"Decoded data: {decoded_data.decode('utf-8')}")

# Verify
print(f"Original and decoded data match: {original_data == decoded_data.decode('utf-8')}")
