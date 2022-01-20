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
        self.tx_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 35)
        self.gas_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 60)
        self.price_font = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 130)
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
        draw.line((0,250,self.display.width,250), width=4)
        # draw.rectangle((0,303),display.width //2, 400, outline = 0, width=5)
        draw.line((0,600,self.display.width,600), width=4)

        draw.line((1,1160,self.display.width,1160 ), width=4)

        img_width = self.display.frame_buf.width
        text_width, _ = self.title_font.getsize(self.title)
        text_height = 180

        draw_x = (img_width - text_width)//2

        draw_y = (300 - text_height)//2

        # title
        
        draw.text((draw_x, 0), self.title, font=self.title_font)
        # draw.text((0,500), "$", font=self.price_font)
        self.display.draw_full(constants.DisplayModes.GC16)

    def clear_screen(self):
        
        print('Clearing display...')
        self.display.clear()
        print("cleared")
        self.layout_init()
        self.refresh_counter = 0

       
    def update_block(self, block_number, block_hash, gas_price, num_tx, time_stamp, transactions):
        if self.refresh_counter == 15:
            self.clear_screen()


        draw = ImageDraw.Draw(self.display.frame_buf)
        

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,254,self.display.width,596))
        # draw.rectangle((0,350,self.display.width,550),  outline = 0, width=5)
        
        
        block = f"#{block_number}"
        price = "$3000.13"
        _hash = f"block hash: {block_hash}"
        gas = f"gas price: {gas_price} gwei"
        txs = f"{num_tx} transactions"
        block_number_width, _ = self.block_font.getsize(block)
        time = time_stamp.strftime("%I:%M:%S %p")
        self.handle_transactions(draw,transactions, num_tx)
        gas_price_x = 20 + block_number_width + 20
        draw.text((gas_price_x,390), txs, font=self.gas_font)
        draw.text((gas_price_x,330), gas,font=self.gas_font)
        draw.text((gas_price_x,450),time,font=self.gas_font)
        draw.text((20,470),price,font=self.price_font)
        draw.text((30,270),_hash, font=self.hash_font)
        draw.text((20,320), block, font=self.block_font)
        self.display.draw_partial(constants.DisplayModes.DU)

        self.refresh_counter += 1
        

 
    def handle_transactions(self,draw, transactions, num_tx):
        img_width = self.display.frame_buf.width

        

        starting_x = 20
        starting_y = 635

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,605,self.display.width,1155))

        text_width, _ = self.tx_font.getsize("transactions hashes:")

        draw_x = (img_width - text_width)//2

        draw.text((draw_x, 605),"transaction hashes:", font=self.tx_font)
        
        y_counter = 0
        x_counter = 0
        tx_counter = 0

        for i in transactions:
            tx_hex = i.hex()
            tx_counter +=1
            if y_counter == 16:
                starting_x += 150
                starting_y = 635
                y_counter = 0
                x_counter += 1

            y_counter += 1


            if x_counter == 9:

                break


            

            tx_draw = f"{tx_hex[:5]}...{tx_hex[len(tx_hex)-3:]}"

            draw.text((starting_x, starting_y),tx_draw, font=self.tx_font)
            starting_y +=30
        
        text_width, _ = self.tx_font.getsize(f"showing {tx_counter} of {num_tx}")

        draw_x = (img_width - text_width)//2

        draw.text((draw_x, 1120), f"showing {tx_counter} of {num_tx}", font=self.tx_font)
        # self.display.draw_partial(constants.DisplayModes.DU)
        



# def main():
#     live_ethereum = LIVEthereum()

#     live_ethereum.update_block("1232133")



    



# if __name__ == "__main__":
#     main()