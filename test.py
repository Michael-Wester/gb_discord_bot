

server_name = "tesESt 24234$@#$...///'''"
server_name = ''.join(ch for ch in server_name if ch.isalnum())
print(server_name)