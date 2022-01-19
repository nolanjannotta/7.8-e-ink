from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont






class LIVEthereum:
    def __init__(self):
        self.title_font = ImageFont.truetype("/home/pi//7.8-e-ink/fonts/PlayfairDisplay-BlackItalic.ttf", 180)
        self.title = "LIVEthereum"
        self.display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)

        print('Clearing display...')
        self.display.clear()
        print("cleared")

    

    def layout_init(self):


        draw = ImageDraw.Draw(self.display.frame_buf)
        # title box

        # draw.rectangle((0, 0, display.width, 300),  outline = 0, width=5)
        draw.line((0,300,self.display.width,300), width=4)
        # draw.rectangle((0,303),display.width //2, 400, outline = 0, width=5)
        draw.line((0,600,self.display.width,600), width=4)

        draw.line((1,1100,self.display.width,1100 ), width=4)

        img_width = self.display.frame_buf.width
        text_width, _ = self.title_font.getsize(self.title)
        text_height = 180

        draw_x = (img_width - text_width)//2

        draw_y = (300 - text_height)//2

        # title
        
        draw.text((draw_x, draw_y), self.title, font=self.title_font)
        draw.text((0,350), "#", font=self.title_font)
        self.display.draw_full(constants.DisplayModes.GLD16)




def main():
    live_ethereum = LIVEthereum()
    live_ethereum.layout_init()



    



if __name__ == "__main__":
    main()