
def send_play():
    play_cmd = "play\n"
    sock.send(play_cmd.encode())

def set_freedrive():
    freedrive_on = "def myProg():\n  set_standard_analog_input_domain(0, 0)\n  set_tool_digital_out(0, False)\n  set_analog_outputdomain(0, 0)\n  set_freedrive(1)\n  loop = 1\n  while loop == 1:\n    sync()\n  end\nend\n"
    sock.send(freedrive_on.encode())
