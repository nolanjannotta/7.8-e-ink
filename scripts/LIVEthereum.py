from IT8951.display import AutoEPDDisplay
from time import sleep
from IT8951 import constants
from PIL import Image, ImageDraw, ImageFont
from collections import deque
import qrcode
import asyncio







class LIVEthereum:
    def __init__(self, network_id, client_version, initial_health):
        self.display = AutoEPDDisplay(vcom=-2.06, rotate="CCW", spi_hz=24000000)
        # self.get_font("PlayfairDisplay-BlackItalic.ttf", 180) = ImageFont.truetype("/home/pi/7.8-e-ink/fonts/PlayfairDisplay-BlackItalic.ttf", 180)
        
        self.connection_health = {}
        self.activity_list = deque([])
        self.current_tracked_tx = deque([])
        


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

        self.handle_health(initial_health)



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


        activity_width, _ = self.get_font("Zag_Bold.ttf", 60).getsize("activity monitor")
        x_value = (910 - activity_width) // 2
        draw.text((x_value, 1470),"activity monitor", font=self.get_font("Zag_Bold.ttf", 60))


        health_width, _ = self.get_font("Zag_Bold.ttf", 60).getsize("connection health:")
        x_value = ((self.display.width + 930) // 2) - (health_width // 2)
        draw.text((x_value, 1470),"connection health:", font=self.get_font("Zag_Bold.ttf", 60))

        hashes_width, _ = self.get_font("Zag_Bold.ttf", 60).getsize("transactions hashes:")
        draw_x = (self.display.width - hashes_width)//2
        draw.text((draw_x, 605),"transaction hashes:", font=self.get_font("Zag_Bold.ttf", 60))



        draw.line((930,1460, 930, self.display.height), width=4)

        img_width = self.display.frame_buf.width
        text_width, _ = self.get_font("Unique.ttf", 215).getsize(self.title)
        text_height = 180

        draw_x = (img_width - text_width)//2

        draw_y = (300 - text_height)//2

        # title
        
        draw.text((draw_x, -20), self.title, font=self.get_font("Unique.ttf", 215))
        draw.text((50, 200), f'chain id: {self.network_id}   ||   client version: {self.client_version}', font=self.get_font("Zag_Bold.ttf", 45))
        # draw.text((500, 200), self.client_version, font=self.get_font("Zag_Bold.ttf", 45))
        # draw.text((0,500), "$", font=self.get_font("Zag_Bold.ttf", 130))
        self.display.draw_full(constants.DisplayModes.GC16)

    def clear_screen(self):
        
        print('Clearing display...')
        self.display.clear()
        print("cleared")
        self.layout_init()
        self.print_activity()
        self.connection_health = {} # clear out the connection health object so that the function detects a difference and draw on the screen
        self.refresh_counter = 0

    # def connection_health(self, ):

    def print_qr(self, block_number):
       

        # clearing image to white
        qr = qrcode.QRCode(
            box_size=7,
            border=0
        )
        qr.add_data(f'https://etherscan.io/block/{block_number}')
        qr.make()
        img = qr.make_image()
        self.display.frame_buf.paste(img, (self.display.width - img.size[0] - 10, 600 - img.size[1] - 10))


    def handle_exception(self, message):
        draw = ImageDraw.Draw(self.display.frame_buf)
        self.print_message(message, draw)

    def print_message(self, message, draw):
        self.display.frame_buf.paste(0xFF, box=(0,655,self.display.width,1458))
        draw.text((20, 700),str(message), font=self.get_font("Zag_Bold.ttf", 60))
        self.display.draw_partial(constants.DisplayModes.DU)

    def loading_message(self, block_number):
        draw = ImageDraw.Draw(self.display.frame_buf)
        message = f"loading transactions for #{block_number}..."
        loading_width, _ = self.get_font("Zag_Bold.ttf", 70).getsize(message)
        x_value = (910 - loading_width) // 2
        self.display.frame_buf.paste(0xFF, box=(0,655,self.display.width,1458))
        draw.text((x_value, 800), message, font=self.get_font("Zag_Bold.ttf", 70))
        
        self.display.draw_partial(constants.DisplayModes.DU)


    def update_block(self, block_data):
        

        self.refresh_counter += 1
        
        if self.refresh_counter == 10:
            self.clear_screen()
           
        

        # self.display.frame_buf.paste(0xFF, box=(0,605,self.display.width,1458))
        draw = ImageDraw.Draw(self.display.frame_buf)

        

        # clears a portion of the screen where the number is with padding each side
        self.display.frame_buf.paste(0xFF, box=(0,254,self.display.width,596))
        
        # draw.rectangle((0,350,self.display.width,550),  outline = 0, width=5)
        

        
        # block = f"{block_number}"
        price = "$3000.13"
        _hash = f"hash: {block_data['block_hash']}"
        gas = f"gas: {block_data['current_gas_price']} gwei"
        average_gas = f"{block_data['num_last_blocks']} block average: {block_data['average']} gwei"
        miner = f"miner: {block_data['miner']}"

        time = block_data['date_time'].strftime("%I:%M:%S %p" )
        burned = f"{block_data['eth_burned']} eth burned"
        block_number_width, _ = self.get_font("Zag_Bold.ttf", 180).getsize(block_data['block_number'])
        price_width, _ = self.get_font("Zag_Bold.ttf", 130).getsize(price)
        time_width, _ = self.get_font("Zag_Bold.ttf", 60).getsize(time)

      

        burned_time = f'{burned} || {time}'
        
        # self.handle_pending(draw, block_data['num_pending'])

        x_value = 20 + price_width + 20 + time_width + 20
        # draw.text((x_value,470), gas,font=self.get_font("Zag_Bold.ttf", 60))
        # draw.text((x_value,375), average_gas,font=self.get_font("Zag_Bold.ttf", 35))

        x_value = 125 + block_number_width + 20
        draw.text((x_value,330), miner, font=self.get_font("Zag_Bold.ttf", 60))
        draw.text((x_value,390),gas,font=self.get_font("Zag_Bold.ttf", 60))

        x_value = 20 + price_width + 20
        draw.text((x_value,470),average_gas,font=self.get_font("Zag_Bold.ttf", 60))
        draw.text((x_value,527),burned_time,font=self.get_font("Zag_Bold.ttf", 60))


        draw.text((20,473),price,font=self.get_font("Zag_Bold.ttf", 130))
        draw.text((20 ,270),_hash, font=self.get_font("Zag_Bold.ttf", 43))


        draw.text((20,326), "block", font=self.get_font("Zag_Bold.ttf", 48))
        draw.text((30,368), "#", font=self.get_font("Zag_Bold.ttf", 110))

        draw.text((125,320), str(block_data['block_number']), font=self.get_font("Zag_Bold.ttf", 180))

        self.print_qr(block_data['block_number'])
        
        self.loading_message(block_data['block_number']) 
        self.display.draw_partial(constants.DisplayModes.DU)

        self.handle_transactions(block_data['transactions'])
        


        


        



    def handle_health(self, current_connection_status):

        if current_connection_status != self.connection_health:
            self.connection_health = current_connection_status
        
            draw = ImageDraw.Draw(self.display.frame_buf)
            self.display.frame_buf.paste(0xFF, box=(935,1535,self.display.width,self.display.height))

            # draw.rectangle((915,1535,self.display.width,self.display.height),  outline = 0, width=5)

            web3_connection = "-connected to node" if current_connection_status['is_connected'] else "-not connected to node"

            client_listening = "-client is actively" if current_connection_status['client_is_listening'] else "-client is not actively listening for network connections."


            wifi_is_connected = "-connected to internet" if current_connection_status['wifi_is_connected'] else "-not connected to internet"

            
            draw.text((970, 1600),web3_connection, font=self.get_font("Zag_Bold.ttf", 50))

           
            # draw.text((950, 1680),client_listening, font=self.get_font("Zag_Bold.ttf", 50))
            # draw.text((950, 1630),'listening for network connections.', font=self.get_font("Zag_Bold.ttf", 50))
            
            draw.text((970, 1700),wifi_is_connected, font=self.get_font("Zag_Bold.ttf", 50))
            self.display.draw_partial(constants.DisplayModes.DU)
        pass

    

    def print_activity(self):
        draw = ImageDraw.Draw(self.display.frame_buf)
        y_value = 1550
        for activity in self.activity_list:
            draw.text((20, y_value),activity, font=self.get_font("Zag_Bold.ttf", 41))
            y_value += 45

        self.display.draw_partial(constants.DisplayModes.DU)


    def handle_activity_monitor(self, address, hash, block_number):
        short_hash = f"{hash[:5]}...{hash[len(hash)-3:]}"
        message = f"-activity from {address} in {short_hash} in block #{block_number}"
        self.display.frame_buf.paste(0xFF, box=(10, 1535, 925 , self.display.height))

        self.current_tracked_tx.append(hash)

        if len(self.activity_list) < 7:
            if message not in self.activity_list:
                self.activity_list.appendleft(message)
                self.current_tracked_tx.appendleft(hash)
                
        else:
            # draw.rectangle((10, 1535, 905 , self.display.height),  outline = 0, width=5)
            self.activity_list.pop()
            self.current_tracked_tx.appendleft(hash)
            if message not in self.activity_list:
                self.activity_list.appendleft(message)

        self.print_activity()




 
    def handle_transactions(self, transactions):
        draw = ImageDraw.Draw(self.display.frame_buf)


        img_width = self.display.frame_buf.width
        starting_x = 20
        starting_y = 660

        y_counter = 0
        x_counter = 0
        tx_counter = 0
        self.display.frame_buf.paste(0xFF, box=(0,655,self.display.width,1458))
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
            # check for tracking addrress
            for tx in self.current_tracked_tx:
                if tx == tx_hex:
                    text_width, _ = self.get_font("Zag_Bold.ttf", 35).getsize(f"{tx_draw}")
                    
                    draw.rounded_rectangle((starting_x - 5, starting_y - 3, starting_x + text_width + 2, starting_y + 31), radius=6,  outline = 0, width=3)

                    

            draw.text((starting_x, starting_y),tx_draw, font=self.get_font("Zag_Bold.ttf", 35))
            starting_y +=30
        
        text_width, _ = self.get_font("Zag_Bold.ttf", 43).getsize(f"showing {tx_counter} of {len(transactions)}")

        draw_x = (img_width - text_width)//2

        draw.text((draw_x, 1410), f"showing {tx_counter} of {len(transactions)}", font=self.get_font("Zag_Bold.ttf", 52))
        
        self.display.draw_partial(constants.DisplayModes.DU)
        



# def main():
#     live_ethereum = LIVEthereum()

#     live_ethereum.update_block("1232133")



    



# if __name__ == "__main__":
#     main()