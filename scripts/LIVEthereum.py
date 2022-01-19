from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont







    

def layout_init(display):

    fontsize = 180

    message = "LIVEthereum"

    draw = ImageDraw.Draw(display.frame_buf)
    # title box
    draw.rectangle((0, 0, display.width, 300),  outline = 0, width=5)
    # draw.rectangle((0,303),display.width //2, 400, outline = 0, width=5)
    draw.line((0,403,display.width,403), width=5)
    
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)
    except OSError:
        font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)

    img_width = display.frame_buf.width
    text_width, _ = font.getsize(message)
    text_height = fontsize

    draw_x = (img_width - text_width)//2

    draw_y = (300 - text_height)//2
    # title

    draw.text((draw_x, draw_y), message, font=font)
    display.draw_full(constants.DisplayModes.GLD16)





def main():
    display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)

    print('Clearing display...')
    display.clear()
    print("cleared")
   
    layout_init(display)



    



if __name__ == "__main__":
    main()