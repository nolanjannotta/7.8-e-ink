from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont






class LIVEthereum:
    def __init__(self, network_id, client_version):
        self.display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)
        # self.get_font("PlayfairDisplay-BlackItalic.ttf", 180) = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/PlayfairDisplay-BlackItalic.ttf", 180)

        

        # self.get_font("Zag_Bold.ttf", 130) = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/Zag_Bold.ttf", 130)
        self.refresh_counter = 0
        self.title = "LIVEthereum"
        self.client_version = client_version
        self.network_id = network_id

        
        self.last_text_width = 0

        print('Clearing display...')
        self.display.clear()
        print("cleared")
        self.layout_init()



    def get_font(self, font_name, size):
        return ImageFont.truetype(f"/home/pi/code/7.8-e-ink/fonts/{font_name}", size)


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
        text_width, _ = self.get_font("Unique.ttf", 215).getsize(self.title)
        text_height = 180

        draw_x = (img_width - text_width)//2

        draw_y = (300 - text_height)//2

        # title
        
        draw.text((draw_x, -20), self.title, font=self.get_font("Unique.ttf", 215))
        draw.text((70, 200), f'chain id: {self.network_id} || client version: {self.client_version}', font=self.get_font("Zag_Bold.ttf", 45))
        # draw.text((500, 200), self.client_version, font=self.get_font("Zag_Bold.ttf", 45))
        # draw.text((0,500), "$", font=self.get_font("Zag_Bold.ttf", 130))
        self.display.draw_full(constants.DisplayModes.GC16)

    def clear_screen(self):
        
        print('Clearing display...')
        self.display.clear()
        print("cleared")
        self.layout_init()
        self.refresh_counter = 0

    # def connection_health(self, ):

       
    def update_block(self, block_data):
        

        self.refresh_counter += 1
        
        if self.refresh_counter == 10:
            self.clear_screen()


        draw = ImageDraw.Draw(self.display.frame_buf)
        

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,254,self.display.width,596))
        # draw.rectangle((0,350,self.display.width,550),  outline = 0, width=5)
        

        
        # block = f"{block_number}"
        price = "$3000.13"
        _hash = f"hash: {block_data['block_hash']}"
        gas = f"gas price: {block_data['current_gas_price']} gwei"
        average_gas = f"last {block_data['num_last_blocks']} block average: {block_data['average']} gwei"
        txs = f"{block_data['num_tx']} transactions"

        time = block_data['date_time'].strftime("%I:%M:%S %p")
        burned = f"{block_data['eth_burned']} eth burned"
        block_number_width, _ = self.get_font("Zag_Bold.ttf", 180).getsize(block_data['block_number'])
        price_width, _ = self.get_font("Zag_Bold.ttf", 130).getsize(price)
        
        self.handle_transactions(draw,block_data['transactions'], block_data['num_tx'])
        self.handle_pending(draw, block_data['num_pending'])
        self.handle_activity_monitor(draw) 

        x_value = 125 + block_number_width + 20
        draw.text((x_value,315), gas,font=self.get_font("Zag_Bold.ttf", 60))

        draw.text((x_value + 43,375), average_gas,font=self.get_font("Zag_Bold.ttf", 35))

        draw.text((x_value,408), txs, font=self.get_font("Zag_Bold.ttf", 60))
        
        x_value = 20 + price_width + 20
        draw.text((x_value,470),time,font=self.get_font("Zag_Bold.ttf", 60))
        draw.text((x_value,527),burned,font=self.get_font("Zag_Bold.ttf", 60))


        draw.text((20,473),price,font=self.get_font("Zag_Bold.ttf", 130))
        draw.text((20 ,270),_hash, font=self.get_font("Zag_Bold.ttf", 43))


        draw.text((20,326), "block", font=self.get_font("Zag_Bold.ttf", 48))
        draw.text((27,368), "#", font=self.get_font("Zag_Bold.ttf", 110))

        draw.text((125,320), str(block_data['block_number']), font=self.get_font("Zag_Bold.ttf", 180))

        self.display.draw_partial(constants.DisplayModes.DU)

        



    def handle_pending(self, draw, pending_transactions):
        self.display.frame_buf.paste(0xFF, box=(912,1465,self.display.width,1800))
        # draw.rectangle((912,1465,self.display.width,1800),  outline = 0, width=5)
        pending_width, _ = self.get_font("Zag_Bold.ttf", 60).getsize("connection health:")
        x_value = ((self.display.width + 910) // 2) - (pending_width // 2)
        draw.text((x_value, 1500),"connection health:", font=self.get_font("Zag_Bold.ttf", 60))

        pending_width, _ = self.get_font("Zag_Bold.ttf", 130).getsize(str(pending_transactions))
        x_value = ((self.display.width + 910) // 2) - (pending_width // 2)
        draw.text((x_value, 1600),str(pending_transactions), font=self.get_font("Zag_Bold.ttf", 130))

        

    def handle_activity_monitor(self, draw):
        pending_width, _ = self.get_font("Zag_Bold.ttf", 60).getsize("activity monitor")
        x_value = (910 - pending_width) // 2
        draw.text((x_value, 1500),"activity monitor", font=self.get_font("Zag_Bold.ttf", 60))

 
    def handle_transactions(self,draw, transactions, num_tx):
        img_width = self.display.frame_buf.width

        

        starting_x = 20
        starting_y = 660

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,605,self.display.width,1458))

        text_width, _ = self.get_font("Zag_Bold.ttf", 60).getsize("transactions hashes:")

        draw_x = (img_width - text_width)//2

        draw.text((draw_x, 605),"transaction hashes:", font=self.get_font("Zag_Bold.ttf", 60))
        
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

            draw.text((starting_x, starting_y),tx_draw, font=self.get_font("Zag_Bold.ttf", 35))
            starting_y +=30
        
        text_width, _ = self.get_font("Zag_Bold.ttf", 43).getsize(f"showing {tx_counter} of {num_tx}")

        draw_x = (img_width - text_width)//2

        draw.text((draw_x, 1415), f"showing {tx_counter} of {num_tx}", font=self.get_font("Zag_Bold.ttf", 48))
        # self.display.draw_partial(constants.DisplayModes.DU)
        



# def main():
#     live_ethereum = LIVEthereum()

#     live_ethereum.update_block("1232133")



    



# if __name__ == "__main__":
#     main()