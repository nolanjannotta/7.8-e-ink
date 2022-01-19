from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont






class LIVEthereum:
    def __init__(self):
        self.title_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 180)
        self.hash_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 40)
        self.title = "LIVEthereum"
        self.display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)
        self.last_text_width = 0

        print('Clearing display...')
        self.display.clear()
        print("cleared")
        self.layout_init()

    

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
        # draw.text((0,350), "#", font=self.title_font)
        self.display.draw_full(constants.DisplayModes.GC16)

    def update_block(self, block_number, block_hash):

        draw = ImageDraw.Draw(self.display.frame_buf)
        

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,304,self.display.width,596))

        text_width, _ = self.title_font.getsize(block_number)
        self.last_text_width = text_width

        # draw.rectangle((150,320 , 170 + text_width, 580),  outline = 0, width=5)
        # draw.line((0,310,self.display.width,300), width=4)
        message = f"#{block_number}"
        draw.text((30,320),block_hash, font=self.hash_font)
        draw.text((0,310), message, font=self.title_font)
        

        
        self.display.draw_partial(constants.DisplayModes.DU)

  



# def main():
#     live_ethereum = LIVEthereum()
#     live_ethereum.layout_init()
#     sleep(4)
#     live_ethereum.update_block("14034811")
#     sleep(4)
#     live_ethereum.update_block("14034714")


    



# if __name__ == "__main__":
#     main()