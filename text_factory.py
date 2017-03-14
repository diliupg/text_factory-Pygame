import pygame, sys, os
from pygame.locals import KEYDOWN, K_ESCAPE, RLEACCEL



class Text_Factory(pygame.sprite.Sprite):

    """
    Defaults:
    =========
    Animation is 30 frames.
    Pause is 1500ms.
    Fade and rotation is off.
    Default text is "Level 1 complete".
    All above parameters can be changed any time when calling the two routines.

    import
    To use the text_factory module:
    import pygame
    from pygame.locals import KEYDOWN, K_ESCAPE, RLEACCEL
    eg: mytext =
    xpos and ypos are the coords where text will be drawn. This is center screen by default.
    if a font is not supplied (path), the default pygame font will be used.
    Font size need to be supplied along with the colour of text. Default is 100.
    text is the message to be drawn on screen. Depending on the number of letters and the font size, the text string may be wider than the width of the screen. Do the settings accordingly.
    frames are the number of frames generated for the animation. Play with this till you get what you want. Keep in mind that the larger the number, slower the animation and larger the file size.
    pause is how long the text will stay on the screen after the animation.
    slowdown is the animation speed control. larger the number, slower the animation.

    ----------------------------------------------------------------------------
    Zoomin = True by default.
    Zoomout = if False.
    Fading out is not set by default.
    If fade = "in", the animation will fade in while zooming in.
    If fade = "out", the animation will fade out while zooming out.
    Both the above fades can be achieved by passin the fade variable with the Zoomin and Zoomout routines.
    zoomin_rotR - zoom in rotating right
    zoomin_rotL - zoom in rotating left
    zoomout_rotR - zoom ut rotating right
    zoomout_rotL - zoom out rotating left
    """
    def __init__(self, posx = None, posy = None, font = None, fontsize = 100, colour = (255, 50, 64), text = "Level 1 Complete!",  frames = 30, pause = 1500, slowdown = 30, fade = False, rotate = None):

        pygame.sprite.Sprite.__init__(self)

        self.screen = pygame.display.get_surface()

        if self.screen == None:

            if sys.platform == 'win32' or sys.platform == 'win64':
                #os.environ['SDL_VIDEO_CENTERED'] = '0'# center of screen
                os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (10, 30)#top left corner

            self.screen =pygame.display.set_mode((800, 600), 1, 32)  # demo screen size

            back = pygame.image.load("D:\\IMAGES\\space_11.jpg").convert()
            self.screen.blit(back, (0, 0))

        # the subsurface is a rect
        self.subsurface = None  #self.screen.subsurface(0, 0, self.screen.get_width(), self.screen.get_height()).convert_alpha()
        self.background = (0, 0, 0)
        self.alpha = 255
        if posx == None:
            self.posx = self.screen.get_width() / 2
        else:
            self.posx = posx
        if posy == None:
            self.posy = self.screen.get_height() / 2
        else:
            self.posy = posy
        self.center = (self.posx, self.posy)
        self.fontsize = fontsize
        self.colour = colour
        self.font = font
        self.frames = frames
        self.pause = pause
        #self.zoom = zoom  # True - small to large    False - large to small
        self.slowdown = slowdown  # larger the number, slower the animation
        self.alpha = 255
        self.fade = fade
        self.q = 255 / self.frames  # the quantity by which fade_in or fade_out occurs
        self.rotate = rotate
        self.angle = 0
        self.increment = 0  # in degrees
        self.imagelist = []
        self.message = text

    #---------------------------------------------------------------------------
    def text_to_images(self, message = None, colour = None, font = None, fontsize = None, rotate = None):

        self.imagelist = []  # clear the imagelist

        if not colour: colour = self.colour
        if not font: font = self.font
        if not fontsize: fontsize = self.fontsize
        if not message: message = self.message
        if not rotate: rotate = self.rotate
        if rotate == "right": self.increment = -20
        elif rotate == "left": self.increment = 20

        self.renderedfont = pygame.font.Font(font, fontsize)

        # this is the largest text image
        matext = self.renderedfont.render(message, True, colour, self.background).convert()
        rect = matext.get_rect()
        matext_width = matext.get_width()  # get the width of the text image
        matext_height = matext.get_height()

        # depending on the size of the full text image, how much each step should increase / decrease image
        reduceX= matext_width / self.frames
        reduceY = matext_height / self.frames
        width = height = 0

        for x in xrange(self.frames + 2):  # increase / decrease image and add to imagelist

            newW = (matext_width - width)
            newH = (matext_height - height)
            if newW <= 0: newW = 1
            if newH <= 0: newH = 1
            # make a newsurface to the size that image will be shrunk
            newsurface = pygame.Surface((newW, newH))
            # reduce size of image and paste on newsurface which is faster than reducing the size of image itself.
            pygame.transform.scale(matext, (newW, newH), newsurface)
            # if rotate thenrotate in the correct direction
            if rotate == "right" or rotate == "left":

                rotsurface = pygame.transform.rotate(newsurface, self.angle)
                newsurface = rotsurface
                self.angle += self.increment

            # set the colour key
            newsurface.convert()
            newsurface.set_colorkey(0, RLEACCEL)
            #set alpha to max (fully opaque. if alpha - 0, fully transparent)
            newsurface.set_alpha(self.alpha)
            # add image to the list
            self.imagelist.append(newsurface)

            width += reduceX
            height += reduceY


    #---------------------------------------------------------------------------
    def get_rects(self, image):

        # grab a part of the image the size of the increased / reduced message

        clean_rect = dirty_rect = image.get_rect()

        dirty_rect.center = self.center
        posx = newposx = dirty_rect[0]
        posy = newposy = dirty_rect[1]
        width = dirty_rect[2]
        height = dirty_rect[3]
        if width > self.screen.get_width(): width = self.screen.get_width()
        if height > self.screen.get_height(): height = self.screen.get_height()
        if posx < 0: newposx = 0
        if posy < 0: newposy = 0
        #print dirty_rect, posx, posy, newposx, newposy
        clean_rect = pygame.Rect(newposx, newposy, width, height)
        # put the grabbed image into the subsurface variable
        self.subsurface = self.screen.subsurface(clean_rect).convert_alpha()

        return dirty_rect, clean_rect


    #---------------------------------------------------------------------------
    def blit(self, image, image_pos_rect, image_clear_rect):
        # blit the increasd / reduced image to the screen
        self.screen.blit(image, (image_pos_rect))
        pygame.display.flip()
        pygame.time.wait(self.slowdown)  # how long to pause while image displayed
        # now clear the image by pasting the subsurface which we  grabbed earlier
        self.screen.blit((self.subsurface), (image_clear_rect))


        for e in pygame.event.get():
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                raise SystemExit

    #---------------------------------------------------------------------------
    def default(self, text = None):

        self.Zoomin(text)
        self.Zoomout(text)

    #---------------------------------------------------------------------------
    def Zoomin(self, message = None, colour = None, font = None, fontsize = None, fade = None, rotate = None):

        if not colour: colour = self.colour
        if not font: font = self.font
        if not fontsize: fontsize = self.fontsize
        if not message: message = self.message
        if not fade: fade = self.fade
        if not rotate: rotate = self.rotate

        if fade == "in":
            self.alpha = 0
            fade = "working"

        elif fade == "out":
            self.alpha = 255
            self.q = -self.q
            fade = "working"

        self.text_to_images(message, colour, font, fontsize, rotate)

        for image in reversed(self.imagelist):

            dirty_rect, clean_rect = self.get_rects(image)

            if fade == "working":
                self.alpha += self.q
                image.set_alpha(self.alpha)

            self.blit(image, dirty_rect, clean_rect)
        self.alpha = 255  # reset alpha
        pygame.time.wait(self.pause)

    #---------------------------------------------------------------------------
    def Zoomout(self, message = None, colour = None, font = None, fontsize = None, fade = None, rotate = None):

        if not colour: colour = self.colour
        if not font: font = self.font
        if not fontsize: fontsize = self.fontsize
        if not message: message = self.message
        if not fade: fade = self.fade

        if fade == "out":
            self.alpha = 255
            fade = "working"

        elif fade == "in":
            self.alpha = 0
            fade = "working"
            self.q = -self.q

        self.text_to_images(message, colour, font, fontsize, rotate)

        # print the first (largest) image and pause for a while
        image = self.imagelist[0]
        dirty_rect, clean_rect = self.get_rects(image)
        self.blit(image, dirty_rect, clean_rect)
        pygame.time.wait(self.pause)

        # now blit the whole imagelist
        for image in (self.imagelist):

            dirty_rect, clean_rect = self.get_rects(image)

            if fade == "working":
                self.alpha -= self.q
                image.set_alpha(self.alpha)

            self.blit(image, dirty_rect, clean_rect)

    #---------------------------------------------------------------------------

if __name__ == '__main__':
    pygame.init()

    splash = Text_Factory()

    splash.default()

    #splash.Zoomin(message= "New Message", colour= (255, 0, 255))

    #splash.Zoomout(message= "Another message", colour= (100, 255, 75))

    #splash.Zoomin(message = "fading message", fade = "in")

    #splash.Zoomout(message = "fading message", fade = "out")
    #pygame.time.wait(splash.pause)
    #splash.Zoomin(message = "fading in message", rotate = "right", fade = "in")




