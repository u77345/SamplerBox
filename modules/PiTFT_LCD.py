###############################################################
#  LCD display via frame buffres vis pygame
#
#  Currently supports only Adafruit PiTFT 2.4
###############################################################

import pygame
import os
from typing import Optional
import time
import UI
import gv
import sys

# -----------------------------------------------------------------------------
# Constants and global variables
# -----------------------------------------------------------------------------

#lcd: Optional['pygame.Surface'] = None

class pitft_lcd:

    _cached_text = {}
    _cached_fonts = {}
    font = {}
    lcd = {}

# -----------------------------------------------------------------------------
# Methods
# -----------------------------------------------------------------------------

    def clear(self):
        empty = pygame.Color(0,0,0,0)
        self.lcd.fill(empty)


    def get_font(self, font_preferences, size):

        key = str(font_preferences) + '|' + str(size)
        font = self._cached_fonts.get(key, None)
        if font == None:
            font = self.make_font(font_preferences, size)
            self._cached_fonts[key] = font
        return font


    def create_text(self, text, fonts, size, color):
        global _cached_text
        key = '|'.join(map(str, (fonts, size, color, text)))
        image = self._cached_text.get(key, None)
        if image == None:
            font = self.get_font(fonts, size)
            image = font.render(text, True, color)
            self._cached_text[key] = image
        return image


    def draw_text(self, pos, s, font, fill):
        text = self.font.render(s, True, fill)
        self.lcd.blit(text, pos)
        pygame.display.flip()

    def __init__(self):
        try:
            self.busy = False
            self.s4 = ''
            self.s5 = ''
            self.s6 = ''
            self.x = 0
            
            os.putenv('SDL_FBDEV', '/dev/fb1')
            os.putenv('SDL_AUDIODRIVER', '/dev/null')
            pygame.mixer = None
            pygame.init()
            
            size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

            self.width = size[0]
            self.height = size[1]
            self.padding = gv.cp.getint(gv.cfg, "PITFT_LCD_PADDING".lower())
            self.top = self.padding
            self.bottom = self.height-self.padding

            self.logging = gv.cp.getboolean(gv.cfg, "LOG_PITFT_LCD".lower())

            self.lcd = pygame.display.set_mode((size[0], size[1]))
            self.lcd.fill((0,0,0))
            pygame.mouse.set_visible(False)
            pygame.display.update()
            self.font = pygame.font.Font("modules/res/DejaVuSans.ttf",28)

        except:
            print("**** Hiccup in PiTFT Init ****")
            print(sys.exc_info())


    def display(self, msg, menu1, menu2, menu3):
        if self.busy: 
            return False
        self.busy = True
        if self.logging:
            print('*' *42)
            print(" ** PiTFT: ", msg, menu1, menu2, menu3)
        
        # #########START DRAWING##########################
        self.clear()
        s1 = msg
        s2 = ''
        if s1 == '':
            if UI.Presetlist() != []:
                s1 = UI.Presetlist()[UI.getindex(UI.Preset(), UI.Presetlist())][1]
                preset_str = s1.split(" ",1)
                preset_num = preset_str[0]
                s1 = preset_str[1]
                s2 = preset_num # put preset number and voice number on line 2
            if UI.Voice() > 1:
                s2 += ' voice:'+ str(UI.Voice())

        s3a = "Scale:%s" % (UI.Scalename()[UI.Scale()])
        s3b = "Chord:%s" % (UI.Chordname()[UI.Chord()])
        # Change menu lines if necessary
        if menu1 != '':
            self.s4 = menu1
            self.s5 = menu2
            self.s6 = menu3
        #s6 = self.s6 if self.s6 != '' else UI.IP() #IP is cluttering
        if UI.USE_ALSA_MIXER:
            s7 = "%s | Vol: %d%%" % (UI.Mode(), UI.SoundVolume())
        else:
            s7 = "Mode: %s" % (gv.sample_mode)
        self.draw_text((self.x, self.top), s1, font=self.font, fill=(128,255,0))
        # self.draw.rectangle((self.x, self.top + 28, self.device.width, self.top + 30), fill=(255,255,255))
        self.draw_text((self.x+2, self.top+32), s2, font=self.font, fill=(64,128,0))
        self.draw_text((self.x, self.top+60), s3a, font=self.font, fill=(127,127,127))
        self.draw_text((self.x, self.top+84), s3b, font=self.font, fill=(127,127,127))
        self.draw_text((self.x, self.top+112), self.s4, font=self.font, fill=(255,128,0))
        if len(menu3) > 0:  # display menu item in yellow if you can scroll values
            self.draw_text((self.x, self.top+140), self.s5, font=self.font, fill=(255,255,0)) 
        else:
            self.draw_text((self.x, self.top+140), self.s5, font=self.font, fill=(255,128,0))
        #self.draw_text((self.x, self.top+168), s6, font=self.font, fill=(0,128,255))
        self.draw_text((self.x, self.top+198), s7, font=self.font, fill=(0,64,128))

        if self.logging:
            print(" ** PiTFT: ", s1)
            print(" ** PiTFT: ", s2)
            print(" ** PiTFT: ", s3a)
            print(" ** PiTFT: ", s3b)
            print(" ** PiTFT: ", self.s4)
            print(" ** PiTFT: ", self.s5)
            #print(" ** PiTFT: ", s6)
            print(" ** PiTFT: ", s7)

        # #########END DRAWING##########################
        self.busy = False
        return True


# -------------------------------------------------------------------------
# Static Entry
# -------------------------------------------------------------------------

if __name__ == "__main__":
    
    pitft = pim_lcd()

    pitft.display("MSG", "Menu1", "Menu2", "Menu3")

    while True:
        time.sleep(0.1)
