import os
import pygame

level_data = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                             T     H    K                                                                                                                                                               CXXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                     LGGGGGGGGGGGGGGGGGGGGGGGR                                                                                                                  T           T      G  G  G  G  LGGGGGGGGRXXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                     H     LGGGGGGGGR   LGGGGGGGR                        XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                         K           G                                                   XXXXXXXXXXXXXXXXXXXXXXXX', # 45 space in ''
'XXXXXXXXXXXXXXXXXXXXXXXX                                                         T  H       K                                                     H        LGGGGGGGGGGGGGGR                                                      XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX          T  H                      K    T         LGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGR           H       LGGGGGGGGGR                                                                        XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX     LGGGGGGGGGGGGGGGGGGGR    LGGGGGGGGGGGGGGGGR                                                         LGGGGGGGGGR                                                                                     XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                    K                                                                                                                                    XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX    HHH                           H               LGGGGR         LGGGGGGGGGGGGGGGGGG        T          K                                                                                                 XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXXLGGGGGGGGR                    LGGGGGGGGGGGGGGGGGGGG    GGGR   LGGR                 GGR     LGGGGGGGGGGGGGGGR  H                                                                                          XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX         LGGGGGGGR    LGGGGGGGR                                                                            GGGGGR                                                                                        XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                                                                                                                                                         XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX                                                                    T            K                                    H                 H        K   H             K    T        T        T H        T K XXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXX    P                              T                H       LGGGGGGGGGGGGGGGGGR  G  LGGGGGGGGR  LGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG   GGGG   GGGGGGGGGGGGGGGGGG  GGGGGGGGGGG  GGGGGGG   GGGGGGGR    LGGGRXXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXXLGGGGGGGR   LGGGGGGGGGGGGR   LGGGGGGR   T    LGGGGGGGGGGGGGGXXXXXXXXXXXXXXXXXXX  X  XXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXX   XXXXXXXXXXXXXXXXXX  XXXXXXXXXXX  XXXXXXX   XXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXX   XXXXXXXXGGGGGR  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  X  XXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXX   XXXXXXXXXXXXXXXXXX  XXXXXXXXXXX  XXXXXXX   XXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXXXXXXXXXXXX   XXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  X  XXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX   XXXX   XXXXXXXXXXXXXXXXXX  XXXXXXXXXXX  XXXXXXX   XXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
                                                                                                                                                                                                                                     #' end here ' is in place 

def import_folder(path):
    surf_list = []
    for _, __, image_files in os.walk(path):
        image_files.sort()
        for image in image_files:
            if not image.startswith('.'): # prevent .ds_store file
                #print(image)
                full_path = os.path.join(path, image)
                image_surf = pygame.image.load(full_path).convert_alpha()
                surf_list.append(image_surf)
    return surf_list

TILE_SIZE = 32
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = TILE_SIZE * len(level_data)
FPS = 60