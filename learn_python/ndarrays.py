import numpy as np

simple = [1, 2, 3]

# Remmeber that numpy nd arrays receive only one argument. That argument is a single sequence ()
matrix3x3 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print(f'1) This is what the matrix looks like: {matrix3x3}')
print(f'2) This is the first row  of the matrix: {matrix3x3[0]}')
print(f'3) This is the first two row of the matrix: {matrix3x3[:2]}')
print(f'4) This is first item in the 3rd row: {matrix3x3[2, 0]}')
print(f'5) This is the the last column of the first two rows: {matrix3x3[:2, -1]}')
print(f'6) This is th 2nd col item in the 2nd row: {matrix3x3[1][1]}')
print(f'7) This is the middle column: {matrix3x3[:, 1]}')
print(f'8) This is the fist column of the last two rows: {matrix3x3[-2:, 0]}')
print(f'9) The last two columns of the last two rows: {matrix3x3[-2:, -2:]}')
print(f'10) This is the first and 3rd columns: {matrix3x3[:, [0, 2]]}')
print(f'11) This is the diagonal of the matrix: {matrix3x3.diagonal()}')
print(f'12) This is the middle and last columns in the first and last rows: {matrix3x3[[0, 2], [1, 2]]}')
print(f'13: This is the last and penultimate columns of the first and last row {matrix3x3[[0, 2], [-1, -2]]}')
print(f'14: What np.arrange() does: {np.arange(20)}')  # 'arange' as in 'a range'
print(f'15: Reshape a range of values as a 2x2 matrix: {np.arange(36).reshape(3, 12)}')
print(f'16: What np.zeroes does: {np.zeros((2, 2))}')
print(f'17: What linspace does: {np.linspace(0, 2, 10)}')  # 10 Linearly spaces numbers from 0 to 2 (also preferred for floating point numbers over arange)
print(f'18: Transpose of a matrix: {matrix3x3.T}')
print(f'19: Invert a Matrix, {matrix3x3}: {np.linalg.inv(matrix3x3)}')
print(f'20: Identiy of 3x3 matrix: {np.eye(3)}')