from pymouse import PyMouse
import time

m = PyMouse()
# a = m.position()  # 获取当前坐标的位置
# print(a)

# m.move(347, 219)  # 鼠标移动到(x,y)位置
# a = m.position()
# print(a)

counter = 0
while counter < 1200:
    m.click(1133, 147)  # 移动并且在(x,y)位置左击
    time.sleep(3)
