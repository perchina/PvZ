import pygame

# 初始化Pygame
pygame.init()

# 加载图片
image = pygame.image.load("materials/game_elements/GardenHighLight.png")

# 水平翻转图片
flipped_image = pygame.transform.flip(image, True, False)

# 创建窗口
window = pygame.display.set_mode((800, 600))

# 渲染图片
window.blit(flipped_image, (0, 0))
pygame.display.flip()

# 游戏循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# 退出Pygame
pygame.quit()