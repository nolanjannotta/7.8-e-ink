from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont





#helper function
def _place_text(display, text, x=0, y=0):
    '''
    Put some centered text at a location on the image.
    '''


    

def partial_update(display):
    print('Starting partial update...')

    # clear image to white
    display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    # print('  writing full...')
    # _place_text(display.frame_buf, 'partial', x_offset=-display.width//4)
    # display.draw_full(constants.DisplayModes.GC16)

    # # TODO: should use 1bpp for partial text update
    # print('  writing partial...')
    # _place_text(display.frame_buf, 'update', x_offset=+display.width//4)
    # display.draw_partial(constants.DisplayModes.DU)
    
def layout_init(display):

    fontsize = 180

    message = "LIVEthereum"

    draw = ImageDraw.Draw(display.frame_buf)
    # title box
    draw.rectangle((0, 0, display.width, 300),  outline = 0, width=5)
    
    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)
    except OSError:
        font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)

    img_width, img_height = display.frame_buf.size
    text_width, _ = font.getsize(message)
    text_height = fontsize

    draw_x = (img_width - text_width)//2

    draw_y = (300 - text_height)//2

    draw.text((draw_x, draw_y), message, font=font)
    display.draw_partial(constants.DisplayModes.GLD16)






    
def title(display):
    print("writing title...")
    _place_text(display.frame_buf, 'hello this is mode DU')
    display.draw_partial(constants.DisplayModes.DU)
    sleep(2)

    _place_text(display.frame_buf, 'hello this is mode gc16', 0,200)
    display.draw_partial(constants.DisplayModes.GC16)
    sleep(2)
    _place_text(display.frame_buf, 'hello this is mode gl16',0,400)
    display.draw_partial(constants.DisplayModes.GL16)
    sleep(2)
    _place_text(display.frame_buf, 'hello this is mode glr16',0,600)
    display.draw_partial(constants.DisplayModes.GLR16)
    sleep(2)
    _place_text(display.frame_buf, 'hello this is mode gld16,',0,800)
    display.draw_partial(constants.DisplayModes.GLD16)
    sleep(2)
    _place_text(display.frame_buf, 'hello this is mode a2',0,1000)
    display.draw_partial(constants.DisplayModes.A2)
    sleep(2)
    _place_text(display.frame_buf, 'hello this is mode du4',0,1200)
    display.draw_partial(constants.DisplayModes.DU4)

def main():
    display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)

    print('Clearing display...')
    display.clear()
    print("cleared")
    # display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    # print('  writing full...')
    # _place_text(display.frame_buf, 'HELLO', x_offset=-display.width//4)
    # display.draw_full(constants.DisplayModes.GC16)
    layout_init(display)
    # title(display)


    



if __name__ == "__main__":
    main()