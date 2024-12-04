import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import moderngl
import typing

class Texture:
    """
    Responsible for handling an OpenGL texture object.
    """
    def __init__(self, image: pygame.Surface, ctx: moderngl.Context, build_mipmaps: bool = False) -> None:
        image = pygame.transform.flip(image, False, True)
        self.image_width, self.image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, "RGBA")
        self.texture = ctx.texture(size=image.get_size(), components=4, data=img_data)
        self.texture.repeat_x = False
        self.texture.repeat_y = False

        self.build_mipmaps = build_mipmaps
        if self.build_mipmaps:
            self.texture.build_mipmaps()
            self.texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR_MIPMAP_LINEAR)

    def update(self, image: pygame.Surface) -> None:
        """
        Writes the contents of the pygame Surface to OpenGL texture. 
        """

        image = pygame.transform.flip(image, False, True)
        image_width, image_height = image.get_rect().size
        img_data = pygame.image.tostring(image, "RGBA")

        self.texture.write(img_data)

        if self.build_mipmaps:
            # regenerate mipmaps from new data
            self.texture.build_mipmaps()
            self.texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR_MIPMAP_LINEAR)

    def as_surface(self) -> pygame.Surface:
        """
        Returns the OpenGL texture as a pygame Surface.
        """

        buffer = self.texture.read()
        surf = pygame.image.frombuffer(buffer, (self.image_width, self.image_height), "RGBA")
        return surf

    def bind(self, unit: int, read: bool=True, write: bool=True) -> None:
        """
        Bind the texture to a certain texture slot with given permissions
        """

        self.texture.bind_to_image(unit, read=read, write=write)

    def use(self, _id: typing.Union[None, int] = None) -> None:
        """
        Use the texture object for rendering
        """
        if not _id:
            self.texture.use()  
        else:
            self.texture.use(_id)