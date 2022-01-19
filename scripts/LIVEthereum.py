from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont



display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)

#helper function
def _place_text(img, text, x_offset=0, y_offset=0):
    '''
    Put some centered text at a location on the image.
    '''
    fontsize = 80

    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeSans.ttf', fontsize)
    except OSError:
        font = ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf', fontsize)

    img_width, img_height = img.size
    text_width, _ = font.getsize(text)
    text_height = fontsize

    draw_x = (img_width - text_width)//2 + x_offset
    draw_y = (img_height - text_height)//2 + y_offset

    draw.text((0, 0), text, font=font)

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
    print("writing title...")
    _place_text(display.frame_buf, 'LIVEthereum')
    display.draw_partial(constants.DisplayModes.DU)

    


def main():


    print('Clearing display...')
    display.clear()
    print("cleared")
    # display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    # print('  writing full...')
    # _place_text(display.frame_buf, 'HELLO', x_offset=-display.width//4)
    # display.draw_full(constants.DisplayModes.GC16)
    partial_update(display)


    



if __name__ == "__main__":
    main()