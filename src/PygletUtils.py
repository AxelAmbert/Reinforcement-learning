import PIL
import pyglet
from pyglet import gl

from src.GameInfo import GameInfo


class PygletUtils:
    @staticmethod
    def image_scale(image, width, height):
        texture = image.get_texture()
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        texture.width = width  # resize from 8x8 to 16x16
        texture.height = height

    @staticmethod
    def create_image_rgba(path):
        temp_image = PIL.Image.open(path)
        raw_image = temp_image.tobytes()

        return pyglet.image.ImageData(temp_image.width, temp_image.height, 'RGBA', raw_image,
                                      pitch=-temp_image.width * 4)

    @staticmethod
    # Object must have a size and pos attributes
    def get_aabb(object_pos, object_size):
        x1 = object_pos.x
        x2 = object_pos.x + object_size.x
        y1 = object_pos.y
        y2 = object_pos.y + object_size.y

        return x1, x2, y1, y2
