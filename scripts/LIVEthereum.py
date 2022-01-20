from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont






class LIVEthereum:
    def __init__(self):
        self.display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)
        self.title_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/PlayfairDisplay-BlackItalic.ttf", 180)
        self.block_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 180)
        self.hash_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 43)
        self.gas_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 60)
        self.refresh_counter = 0
        self.title = "LIVEthereum"
        
        self.last_text_width = 0

        print('Clearing display...')
        self.display.clear()
        print("cleared")
        self.layout_init()

    

    def layout_init(self):


        draw = ImageDraw.Draw(self.display.frame_buf)
        # title box
        # draw.rectangle((0,320,self.display.width,580),  outline = 0, width=5)
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

    def clear_screen(self):
        
        print('Clearing display...')
        self.display.clear()
        print("cleared")
        self.layout_init()
        self.refresh_counter = 0

       
    def update_block(self, block_number, block_hash, gas_price, num_tx):
        if self.refresh_counter == 15:
            self.clear_screen()


        draw = ImageDraw.Draw(self.display.frame_buf)
        

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,304,self.display.width,596))
        # draw.rectangle((0,350,self.display.width,550),  outline = 0, width=5)
        
        
        block = f"#{block_number}"
        _hash = f"Hash: {block_hash}"
        gas = f"Gas Price: {gas_price} Gwei"
        txs = f"{num_tx} Transactions"
        block_number_width, _ = self.block_font.getsize(block)

        gas_price_x = 20 + block_number_width + 20
        draw.text((gas_price_x,440), txs, font=self.gas_font)
        draw.text((gas_price_x,380), gas,font=self.gas_font)
        draw.text((30,320),_hash, font=self.hash_font)
        draw.text((20,370), block, font=self.block_font)
        self.display.draw_partial(constants.DisplayModes.DU)

        self.refresh_counter += 1

 



# def main():
#     live_ethereum = LIVEthereum()

#     live_ethereum.update_block("1232133")



    



# if __name__ == "__main__":
#     main()