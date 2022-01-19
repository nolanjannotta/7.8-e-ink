from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont







    

def layout_init(display):

    fontsize = 180

    message = "LIVEthereum"

    draw = ImageDraw.Draw(display.frame_buf)
    # title box

    # draw.rectangle((0, 0, display.width, 300),  outline = 0, width=5)
    draw.line((0,300,display.width,300), width=4)
    # draw.rectangle((0,303),display.width //2, 400, outline = 0, width=5)
    draw.line((0,600,display.width,600), width=4)
    draw.line((1,1100,display.width,1100 ), width=4)
    
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
    draw.text((0,450), "#", font=font)
    draw.text((draw_x, draw_y), message, font=font)

    display.draw_full(constants.DisplayModes.GLD16)

# def center_text(xmax, ymax, message):
#     img_width = display.frame_buf.width
#     text_width, _ = font.getsize(message)
#     text_height = fontsize

#     draw_x = (img_width - text_width)//2

#     draw_y = (300 - text_height)//2




def main():
    display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)

    print('Clearing display...')
    display.clear()
    print("cleared")
   
    layout_init(display)



    



if __name__ == "__main__":
    main()