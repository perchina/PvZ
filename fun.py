def handle_index_error(image_list, index):
    """处理正常和错误情况的图片列表"""
    try:
        image_list[index]
    except IndexError:
        index = 0
    return image_list[index]


def plot_image(surface, image, x, y, align_location=4):
    """在指定的surface上绘制图片"""
    rect = image.get_rect()
    if align_location == 0:
        rect.topleft = (x, y)
    elif align_location == 1:
        rect.midtop = (x, y)
    elif align_location == 2:
        rect.topright = (x, y)
    elif align_location == 3:
        rect.center = (x, y)
    elif align_location == 4:
        rect.bottomleft = (x, y)
    elif align_location == 5:
        rect.midbottom = (x, y)
    elif align_location == 6:
        rect.bottomright = (x, y)
    surface.blit(image, rect)