import hashlib

class Block:
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256((self.data + self.previous_hash).encode()).hexdigest()

# Пример
genesis_block = Block("Genesis Block", "0")
second_block = Block("Second Block", genesis_block.hash)

print("Hash of Genesis Block:", genesis_block.hash)
print("Hash of Second Block:", second_block.hash)
