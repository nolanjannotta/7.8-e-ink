from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont






class LIVEthereum:
    def __init__(self):
        self.display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)
        # self.get_font("PlayfairDisplay-BlackItalic.ttf", 180) = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/PlayfairDisplay-BlackItalic.ttf", 180)
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
        self.get_font("PlayfairDisplay-BlackItalic.ttf", 180)

    def get_font(font_name, size):
        return ImageFont.truetype(f"/home/pi/7.8-e-ink/fonts/{font_name}", size)

    

    def layout_init(self):


        draw = ImageDraw.Draw(self.display.frame_buf)
        # title box
        # draw.rectangle((0,320,self.display.width,580),  outline = 0, width=5)
        # draw.rectangle((0, 0, display.width, 300),  outline = 0, width=5)
        draw.line((0,250,self.display.width,250), width=4)
        # draw.rectangle((0,303),display.width //2, 400, outline = 0, width=5)
        draw.line((0,600,self.display.width,600), width=4)

        draw.line((1,1460,self.display.width,1460 ), width=4)

        

        draw.line((910,1460, 910, self.display.height), width=4)

        img_width = self.display.frame_buf.width
        text_width, _ = (self.get_font("PlayfairDisplay-BlackItalic.ttf", 180)).getsize(self.title)
        text_height = 180

        draw_x = (img_width - text_width)//2

        draw_y = (300 - text_height)//2

        # title
        
        draw.text((draw_x, 0), self.title, font=self.get_font("PlayfairDisplay-BlackItalic.ttf", 180))
        # draw.text((0,500), "$", font=self.price_font)
        self.display.draw_full(constants.DisplayModes.GC16)

    def clear_screen(self):
        
        print('Clearing display...')
        self.display.clear()
        print("cleared")
        self.layout_init()
        self.refresh_counter = 0

       
    def update_block(self, block_number, block_hash, gas_price, num_tx, time_stamp, transactions, eth_burned,pending_transactions):
        if self.refresh_counter == 15:
            self.clear_screen()


        draw = ImageDraw.Draw(self.display.frame_buf)
        

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,254,self.display.width,596))
        # draw.rectangle((0,350,self.display.width,550),  outline = 0, width=5)
        

        
        # block = f"{block_number}"
        price = "$3000.13"
        _hash = f"hash: {block_hash}"
        gas = f"gas price: {gas_price} gwei"
        txs = f"{num_tx} transactions"
        time = time_stamp.strftime("%I:%M:%S %p")
        burned = f"{eth_burned} eth burned"
        block_number_width, _ = self.block_font.getsize(str(block_number))
        
        self.handle_transactions(draw,transactions, num_tx)
        self.handle_pending(draw, pending_transactions)
        self.handle_activity_monitor(draw)
        gas_price_x = 120 + block_number_width + 20
        draw.text((gas_price_x,330), gas,font=self.gas_font)
        draw.text((gas_price_x,390), txs, font=self.gas_font)
        
        draw.text((gas_price_x,450),time,font=self.gas_font)
        draw.text((gas_price_x,510),burned,font=self.gas_font)
        draw.text((20,470),price,font=self.price_font)
        draw.text((30,270),_hash, font=self.hash_font)


        draw.text((20,320), "block", font=self.gas_font)
        draw.text((27,355), "#", font=self.price_font)

        draw.text((120,320), str(block_number), font=self.block_font)

        self.display.draw_partial(constants.DisplayModes.DU)

        self.refresh_counter += 1
    
    def handle_pending(self, draw, pending_transactions):
        self.display.frame_buf.paste(0xFF, box=(912,1465,self.display.width,1800))
        # draw.rectangle((912,1465,self.display.width,1800),  outline = 0, width=5)
        pending_width, _ = self.gas_font.getsize("pending transactions")
        x_value = ((self.display.width + 910) // 2) - (pending_width // 2)
        draw.text((x_value, 1500),"pending transactions", font=self.gas_font)

        pending_width, _ = self.price_font.getsize(str(pending_transactions))
        x_value = ((self.display.width + 910) // 2) - (pending_width // 2)
        draw.text((x_value, 1600),str(pending_transactions), font=self.price_font)

        

    def handle_activity_monitor(self, draw):
        pending_width, _ = self.gas_font.getsize("activity monitor")
        x_value = (910 - pending_width) // 2
        draw.text((x_value, 1500),"activity monitor", font=self.gas_font)

 
    def handle_transactions(self,draw, transactions, num_tx):
        img_width = self.display.frame_buf.width

        

        starting_x = 20
        starting_y = 660

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,605,self.display.width,1458))

        text_width, _ = self.gas_font.getsize("transactions hashes:")

        draw_x = (img_width - text_width)//2

        draw.text((draw_x, 605),"transaction hashes:", font=self.gas_font)
        
        y_counter = 0
        x_counter = 0
        tx_counter = 0

        for i in transactions:
            tx_hex = i.hex()
            tx_counter +=1
            if y_counter == 25:
                starting_x += 150
                starting_y = 660
                y_counter = 0
                x_counter += 1

            y_counter += 1


            if x_counter == 9:

                break


            

            tx_draw = f"{tx_hex[:5]}...{tx_hex[len(tx_hex)-3:]}"

            draw.text((starting_x, starting_y),tx_draw, font=self.tx_font)
            starting_y +=30
        
        text_width, _ = self.hash_font.getsize(f"showing {tx_counter} of {num_tx}")

        draw_x = (img_width - text_width)//2

        draw.text((draw_x, 1415), f"showing {tx_counter} of {num_tx}", font=self.hash_font)
        # self.display.draw_partial(constants.DisplayModes.DU)
        



# def main():
#     live_ethereum = LIVEthereum()

#     live_ethereum.update_block("1232133")



    



# if __name__ == "__main__":
#     main()