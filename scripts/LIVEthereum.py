from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont





#helper function
def _place_text(img, text, x=0, y=0):
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


    draw.text((x, y), text, font=font)

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
    # _place_text(display.frame_buf, 'LIVEthereum')
    # display.draw_partial(constants.DisplayModes.DU)

    # _place_text(display.frame_buf, 'LIVEthereum', 0,20)
    # display.draw_partial(constants.DisplayModes.GC16)

    # _place_text(display.frame_buf, 'LIVEthereum',0,40)
    # display.draw_partial(constants.DisplayModes.GL16)

    # _place_text(display.frame_buf, 'LIVEthereum',0,60)
    # display.draw_partial(constants.DisplayModes.GLR16)

    # _place_text(display.frame_buf, 'LIVEthereum,',0,80)
    # display.draw_partial(constants.DisplayModes.GLD16)

    _place_text(display.frame_buf, 'LIVEthereum',0,100)
    display.draw_partial(constants.DisplayModes.A2)

    _place_text(display.frame_buf, 'LIVEthereum',0,120)
    display.draw_partial(constants.DisplayModes.DU4)

    
def title(display):
    print("writing title...")
    _place_text(display.frame_buf, 'LIVEthereum')
    display.draw_partial(constants.DisplayModes.DU)

def main():
    display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)

    print('Clearing display...')
    display.clear()
    print("cleared")
    # display.frame_buf.paste(0xFF, box=(0, 0, display.width, display.height))

    # print('  writing full...')
    # _place_text(display.frame_buf, 'HELLO', x_offset=-display.width//4)
    # display.draw_full(constants.DisplayModes.GC16)
    title(display)


    



if __name__ == "__main__":
    main()