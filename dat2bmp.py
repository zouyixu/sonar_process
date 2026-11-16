import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2


## 读取数据
FOV = 80.0                                  # 扇形开角 (deg)
Range = 8.0                                 # 最大量程 (m)
row = 401                                   # 行：量程方向的采样点数
beam = 512                                  # 列：开角方向的采样点数
angle_res = FOV / beam                      # 每列对应的角度间隔 (deg)
range_res = Range / (row - 1)               # 每行对应的量程间隔 (m)，与 TF.m 的 dr = 0.02 一致

relative_path = "frame.dat"

frame = np.fromfile(relative_path, dtype=np.uint8)
frame = frame.reshape(row, beam)

r = np.arange(row)*range_res
theta = np.deg2rad(np.linspace(-FOV/2, FOV/2, beam))
Theta, R = np.meshgrid(theta, r)
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

## 滤波处理
frame_filtered = cv2.medianBlur(frame, 3)

## 绘制保存
fig, ax = plt.subplots(figsize=(6.4, 6.4))  # 正方形，适合 YOLO 的方形输入
ax.pcolormesh(Y, X, frame, shading='auto', cmap='gray')
ax.set_aspect('equal')
ax.axis('off')          # 关掉坐标轴
plt.subplots_adjust(0, 0, 1, 1)  # 去掉边距
fig.patch.set_facecolor('black')      # 画布背景黑
ax.set_facecolor('black')             # 坐标区背景黑
fig.savefig('out.jpg', dpi=200, bbox_inches='tight', pad_inches=0)
