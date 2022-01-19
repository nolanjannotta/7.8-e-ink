from IT8951.display import AutoEPDDisplay
from time import sleep


display = AutoEPDDisplay(vcom=-2.06, rotate=True, spi_hz=24000000)

def main():


    print('Clearing display...')
    display.clear()

    print("cleared")



if __name__ == "__main__":
    main()