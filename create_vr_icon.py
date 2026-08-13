from pathlib import Path
import struct

W = H = 64
TRANSPARENT = (0, 0, 0, 0)
pixels = [[TRANSPARENT for _ in range(W)] for _ in range(H)]


def rect(x1, y1, x2, y2, color):
    for y in range(max(0, y1), min(H, y2)):
        for x in range(max(0, x1), min(W, x2)):
            pixels[y][x] = color


def border(x1, y1, x2, y2, color, thickness=2):
    rect(x1, y1, x2, y1 + thickness, color)
    rect(x1, y2 - thickness, x2, y2, color)
    rect(x1, y1, x1 + thickness, y2, color)
    rect(x2 - thickness, y1, x2, y2, color)

# Colors are RGBA
rect(10, 20, 54, 46, (6, 78, 95, 180))
rect(8, 18, 56, 44, (8, 145, 178, 220))
rect(12, 20, 52, 42, (15, 23, 42, 255))
border(10, 18, 54, 44, (34, 211, 238, 255), 3)
rect(18, 26, 29, 36, (103, 232, 249, 255))
rect(35, 26, 46, 36, (103, 232, 249, 255))
rect(20, 27, 25, 30, (207, 250, 254, 255))
rect(37, 27, 42, 30, (207, 250, 254, 255))
rect(28, 14, 36, 18, (34, 211, 238, 255))
rect(31, 49, 33, 57, (167, 139, 250, 255))
rect(27, 52, 37, 54, (167, 139, 250, 255))

# BITMAPINFOHEADER + pixels + AND mask
xor_bytes = bytearray()
for y in range(H - 1, -1, -1):
    for x in range(W):
        r, g, b, a = pixels[y][x]
        xor_bytes += bytes((b, g, r, a))

and_stride = ((W + 31) // 32) * 4
and_mask = bytes(and_stride * H)

bi_header = struct.pack(
    '<IIIHHIIIIII',
    40, W, H * 2, 1, 32, 0, len(xor_bytes), 0, 0, 0, 0
)
image_data = bi_header + xor_bytes + and_mask

ico_header = struct.pack('<HHH', 0, 1, 1)
dir_entry = struct.pack('<BBBBHHII', W, H, 0, 0, 1, 32, len(image_data), 6 + 16)
Path('Hysplex.ico').write_bytes(ico_header + dir_entry + image_data)
print('Created Hysplex.ico')
