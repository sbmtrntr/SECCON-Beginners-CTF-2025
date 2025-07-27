import matplotlib.pyplot as plt
import numpy as np
import binascii

def hex_to_bytes(hex_strs):
    return [binascii.unhexlify(h) for h in hex_strs]

def block_diff_matrix(hex_blocks, block_size=16):
    """
    暗号ブロック群（hex）をバイト列にして、各ブロックのbit差分を可視化。
    """
    byte_blocks = hex_to_bytes(hex_blocks)
    num_blocks = len(byte_blocks)
    matrix = np.zeros((num_blocks, block_size * 8), dtype=int)  # 各bit単位で行列化

    ref_block = byte_blocks[0]
    for i, blk in enumerate(byte_blocks):
        for j in range(block_size):
            ref_byte = ref_block[j]
            target_byte = blk[j]
            for bit in range(8):
                # XORでbit差分を見る
                ref_bit = (ref_byte >> (7 - bit)) & 1
                tgt_bit = (target_byte >> (7 - bit)) & 1
                matrix[i, j * 8 + bit] = ref_bit ^ tgt_bit
    return matrix

def visualize_diff(matrix, title='Bit Difference Heatmap'):
    plt.figure(figsize=(12, len(matrix) * 0.5))
    plt.imshow(matrix, cmap='Reds', interpolation='nearest')
    plt.title(title)
    plt.xlabel('Bit position (0~127)')
    plt.ylabel('Block index')
    plt.colorbar(label='Bit Difference')
    plt.show()

# 使用例: ブロック比較用の暗号化結果（例としてa/bの結果）
cipher_blocks = [
    '1d5bb1a5024dee0b591aadc4656796ce',
    '7fdb55d04d801fbda78bd372bcfae9ab',
    'd0da166a1e8615bebe974fd5f8f9987e',
    '32533bb5ff00d8b78e2e01e915fd3cd8',
    '160f96835c129478865dbdd8ae86b873',
    'b7041b3c597dd2eec84d3077a5bfd19d',
    'dc896b98e1194b84b2c5545f4f507dda',
    '498891ef121486bcff0539265b3092ac',
    'eeda51f01898c8fb9ad63d6f276d7fc0',
    '4570c643f075d2d379aaf0562e630e4f',
    '1856f7ce8412a397bd2130a687d61d23',
    '7c63a63d5caf76f4c5d1feb6dee253c2',
    '3a155f7e3e99a48ba12fa11fafaffbbd',
    '216f0d4e1b0153716fbdf0feee73a760',
]

matrix = block_diff_matrix(cipher_blocks)
visualize_diff(matrix)