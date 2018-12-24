#########
# SETUP #
#########

from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from urequests import get
from json import loads
from time import sleep

# Ativa display OLED usando interface I2C
i2c = I2C(scl=Pin(4), sda=Pin(5))
oled = SSD1306_I2C(128, 64, i2c, 0x3c)

# Define se o texto deverá ser impresso no console serial
console = True

# Distântica entre as linhas de texto (base)
dist = 14

# Posição das linhas de texto
last_x, last_y = 0, 14
high_x, high_y = 0, last_y + dist
low_x,  low_y  = 0, high_y + dist
vol_x,  vol_y  = 0,  low_y + dist

# Monta o cabeçalho do display
oled.fill_rect(0, 0, 128, 9, 1)
oled.text('VALOR DO BITCOIN', 0, 1, 0)

# Imprime as linhas no display
oled.text('Atual:', last_x, last_y)
oled.text('Maior:', high_x, high_y)
oled.text('Menor:',  low_x,  low_y)
oled.text('Volume:', vol_x,  vol_y)

# Imprime no console serial, caso definido
if console:
    print('\x1b[2J\x1b[H')  # Limpa a tela
    print('-' * 16)
    print('VALOR DO BITCOIN')
    print('-' * 16)
    print('Atual:')
    print('Maior:')
    print('Menor:')
    print('Volume:')
    print('-' * 16)
    print()

oled.show()


########
# LOOP #
########

while True:
    # Coleta a cotação atual do Bitcoin em reais, via API do BitValor
    try:
        json = get('https://api.bitvalor.com/v1/ticker.json').text
    except Exception as identifier:
        last, high, low, vol = 0, 0, 0, 0
        print(identifier)
        raise
    else:
        data = loads(json)

        # Cotações totais do Bitcoin, poderado pelo volume
        last = data['ticker_24h']['total']['last']
        high = data['ticker_24h']['total']['high']
        low  = data['ticker_24h']['total']['low']
        vol  = data['ticker_24h']['total']['vol']
    
        # Limpa a região do display onde serão impressos os valores
        oled.fill_rect(last_x + 64, last_y, (vol_x + 64) - last_x, (vol_y + 8) - last_y, 0)

        # Imprime os valores no display
        oled.text('%5.2f' % float(last), last_x + 64, last_y)
        oled.text('%5.2f' % float(high), high_x + 64, high_y)
        oled.text('%5.2f' % float(low),   low_x + 64,  low_y)
        oled.text('%5.2f' % float(vol),   vol_x + 64,  vol_y)

        oled.show()

        # Imprime no console serial, caso definido
        if console:
            print('\x1b[H')  # Posiciona o cursor no canto superior esquerdo
            print('-' * 16)
            print('VALOR DO BITCOIN')
            print('-' * 16)
            print('Atual:  %5.2f' % float(last))
            print('Maior:  %5.2f' % float(high))
            print('Menor:  %5.2f' % float(low))
            print('Volume: %5.2f' % float(vol))
            print('-' * 16)
            print()

    # Atualiza a cada minuto
    sleep(60)
