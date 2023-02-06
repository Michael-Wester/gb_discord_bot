from pyboy import PyBoy

"""
This takes 10mb of memory each time it is called.
This is reused to reduce memory usage.
Before I was creating a new pyboy instance each time a command was called.
This was causing the bot to crash after a lot of commands.
This can be any rom as it will be overwritten by loading the save state.
Now there is two instances of pyboy, one for GB and one for GBC.
"""
pyboy_gb = PyBoy("roms/red/red.gb", window_type="headless")
pyboy_gbc = PyBoy("roms/gold/gold.gb", window_type="headless")