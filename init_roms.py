from pyboy import PyBoy
from pyboy import WindowEvent


def init_rom(rom):
    pyboy = PyBoy('roms/' + str(rom) + '/' + str(rom) + '.gb', window_type="headless")
    for i in range(1200):
        pyboy.tick()
    pyboy.send_input(WindowEvent.PRESS_BUTTON_A)
    pyboy.tick()
    pyboy.tick()
    pyboy.send_input(WindowEvent.RELEASE_BUTTON_A)
    pyboy.tick()
    pyboy.tick()

    pyboy.save_state(open('roms/' + str(rom) + '/' + str(rom) + '.gb.state', 'wb'))
    pyboy.stop()

# init_rom('green')
# init_rom('blue')
# init_rom('red')
# init_rom('yellow')
# init_rom('gold')
# init_rom('silver')
# init_rom('crystal')
init_rom('coral')

