from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.responses import FileResponse
import emulator
import constants as c

app = FastAPI()

@app.get("/cmd")
async def cmd(serverid: str, cmd: str): 
    if cmd == "a":
        emulator.a_button(serverid)
    elif cmd == "b":
        emulator.b_button(serverid)
    elif cmd == "up":
        emulator.up(serverid)
    elif cmd == "down":
        emulator.down(serverid)
    elif cmd == "left":
        emulator.left(serverid)
    elif cmd == "right":
        emulator.right(serverid)
    elif cmd == "start":
        emulator.start(serverid)
    elif cmd == "select":
        emulator.select(serverid)
    else:
        return "Invalid command"
    return FileResponse(serverid + "/" + c.screenshot_name)

#http://127.0.0.1:8888/get?serverid=957136739632295966&cmd=a