import socket
import copy
import struct
import time
import threading
import logging
import queue as queue
from threading import Lock
import numpy


def get_local_ip():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  ip = s.getsockname()[0]
  s.close()
  return ip


class URInterface:
  
  UR_SUBTYPE_ROBOT_MODE_DATA = 0
  UR_SUBTYPE_JOINT_DATA = 1
  UR_SUBTYPE_MASTERBOARD_DATA = 3
  UR_SUBTYPE_CARTESIAN_INFO = 4
  UR_SUBTYPE_FORCE_MODE_DATA = 7
  UR_SUBTYPE_ADDITIONAL_INFO = 8
  
  CMD_STOP = 0
  CMD_MOVE_Q = 1
  CMD_MOVE_Q_LINEAR = 2
  CMD_MOVE_P = 3
  CMD_MOVE_P_LINEAR = 4
  CMD_SERVO_Q = 5
  CMD_SPEED_Q = 6
  CMD_SPEED_P = 7
  
  def __init__(self, robot_ip, host_port, command_port, data_port, ur_script):
    self._robot_ip = robot_ip
    self._host_port = host_port
    self._command_port = command_port
    self._data_port = data_port
    self._ur_script = ur_script
    self._cmd_queue = queue.Queue()
    self._is_moving = False
    
    self.connected = False
    
    self.timestamp = 0
    self.robot_connected = 0
    self.robot_enabled = 0
    self.robot_power = 0
    self.emergency_stop = 0
    self.freedrive_button_pressed = 0
    
    self._joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._joint_velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._joint_torques = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._joint_currents = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._tool_position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._tool_velocity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._tool_force = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    self.digital_inputs = 0
    self.digital_outputs = 0
    
    self._state_lock = Lock()
    self._cmd_lock = Lock()
  def __del__(self):
    self.connected = False
    # self.data_thread.join()
    # self.disconnect()
    
  @property
  def joint_positions(self):
    self._state_lock.acquire()
    positions = self._joint_positions[:]
    self._state_lock.release()
    return positions
  
  @property
  def joint_velocities(self):
    self._state_lock.acquire()
    velocities = self._joint_velocities[:]
    self._state_lock.release()
    return velocities
  
  @property
  def joint_torques(self):
    self._state_lock.acquire()
    torques = self._joint_torques[:]
    self._state_lock.release()
    return torques
    
  @property
  def joint_currents(self):
    self._state_lock.acquire()
    currents = self._joint_currents[:]
    self._state_lock.release()
    return currents
    
  @property
  def tool_position(self):
    self._state_lock.acquire()
    position = self._tool_position[:]
    self._state_lock.release()
    return position
    
  @property
  def tool_velocity(self):
    self._state_lock.acquire()
    velocity = self._tool_velocity[:]
    self._state_lock.release()
    return velocity
    
  @property
  def tool_force(self):
    self._state_lock.acquire()
    force = self._tool_force[:]
    self._state_lock.release()
    return force
    
  def connect(self):
    print("Connecting to command port...")
    self._cmd_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._cmd_socket.connect((self._robot_ip, self._command_port))
    
    print("Connecting to data port...")
    self._data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #self._data_socket.setblocking(0)
    #self._data_socket.settimeout(0.01)
    self._data_socket.connect((self._robot_ip, self._data_port))
    
    print("Creating callback server..." + get_local_ip())
    self._cb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._cb_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self._cb_socket.bind((get_local_ip(), self._host_port))
    self._cb_socket.listen(1)
    
    print("Sending urscript...")
    self.send_ur_script(self._ur_script)
    self._cb_conn, self._cp_addr = self._cb_socket.accept()
    self.connected = True
    
    print("Launching threads...")
    self.cmd_thread = threading.Thread(target=self.cmd_thread)
    self.cmd_thread.daemon = True
    self.cmd_thread.start()
    
    self.data_thread = threading.Thread(target=self.data_thread)
    self.data_thread.daemon = True
    self.data_thread.start()
    
  def disconnect(self):
    self._connected = False
    self._data_socket.close()
    
  def cmd_thread(self):
    print("Starting command thread...")
    while self.connected:
      # get the next command from queue
      self._cmd_lock.acquire()
      if not self._cmd_queue.empty():
        cmd = self._cmd_queue.get()
        self._cb_conn.send(cmd) # TODO: should it be outside the lock?
        # print(cmd)
      self._cmd_lock.release()
      time.sleep(0)
  
  def data_thread(self):
    print("Starting data thread...")
    t0 = time.time()
    #n = 0
    while self.connected:
      try:
        N = 2048
        msg = self._data_socket.recv(N)
        
        frame_length = struct.unpack('>I', msg[0:4])[0]
        frame_type = struct.unpack('B', msg[4:5])[0]
        #print(len(msg), frame_length, frame_type)
        self.handle_message(msg)

      except Exception as e:
        print(e)

      #n = n + 1
      t = time.time() - t0
      t0 = time.time()
      #print(t)
      time.sleep(0)
  
  def handle_message(self, msg):
    msg_length = len(msg)
    if msg_length < 588:
      #print('Robot message too short')
      return

    frame_length = struct.unpack('>I', msg[0:4])[0]
    frame_type = struct.unpack('B', msg[4:5])[0]
    
    robot_time = struct.unpack('>d', msg[4:12])[0]
    
    #self._state_lock.acquire()
    self._joint_positions = struct.unpack('>dddddd', msg[252:300])[:]
    self._joint_velocities = struct.unpack('>dddddd', msg[300:348])[:]
    # self._joint_torques = struct.unpack('>dddddd', msg[300:348])[:] # TODO: torques not implemented
    self._joint_currents = struct.unpack('>dddddd', msg[348:396])[:]
    self._tool_position = struct.unpack('>dddddd', msg[444:492])[:]
    self._tool_velocity = struct.unpack('>dddddd', msg[492:540])[:]
    self._tool_force = struct.unpack('>dddddd', msg[540:588])[:]
    self.digital_inputs = struct.unpack('>8s', msg[684:692])[0]
    # print (msg[684:692])
    #self._state_lock.release()
  
  def is_moving(self):
    return self._is_moving

  def send_ur_script(self, script):
    self._cmd_socket.sendall(bytes(script, 'utf-8'))
    return True
    
  def stop_robot(self):
    cmd = struct.pack(">iiiiiiiiiii", self.CMD_STOP, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    self._cmd_lock.acquire()
    while not self._cmd_queue.empty():
      self._cmd_queue.get()
    self._cmd_queue.put(cmd)
    self._cmd_lock.release()
    return True # TODO: implement checking result
  
  def move_to_configuration(self, q, a=1.4, v=0.75, t=0, r=0):
    data = [int(x * 10000) for x in q]
    a = int(a * 10000)
    v = int(v * 10000)
    r = int(r * 10000) 
    t = int(t * 10000) 
    cmd = struct.pack(">iiiiiiiiiii", self.CMD_MOVE_Q, data[0], data[1], data[2], data[3], data[4], data[5], a, v, t, r)
    self._cmd_lock.acquire()
    self._cmd_queue.put(cmd)
    self._cmd_lock.release()
    return True # TODO: implement checking result
    
  def move_to_configuration_linear(self, q, a=1.4, v=0.75, t=0, r=0):
    data = [int(x * 10000) for x in q]
    a = int(a * 10000)
    v = int(v * 10000)
    r = int(r * 10000) 
    t = int(t * 10000) 
    cmd = struct.pack(">iiiiiiiiiii", self.CMD_MOVE_Q_LINEAR, data[0], data[1], data[2], data[3], data[4], data[5], a, v, t, r)
    self._cmd_lock.acquire()
    self._cmd_queue.put(cmd)
    self._cmd_lock.release()
    return True # TODO: implement checking result
  
  def move_to_pose(self, p, a=1.4, v=0.75, t=0, r=0):
    data = [int(x * 10000) for x in p]
    a = int(a * 10000)
    v = int(v * 10000)
    r = int(r * 10000) 
    t = int(t * 10000) 
    cmd = struct.pack(">iiiiiiiiiii", self.CMD_MOVE_P, data[0], data[1], data[2], data[3], data[4], data[5], a, v, t, r)
    self._cmd_lock.acquire()
    self._cmd_queue.put(cmd)
    self._cmd_lock.release()
    return True # TODO: implement checking result
    
  def move_to_pose_linear(self, p, a=1.4, v=0.75, t=0, r=0):
    data = [int(x * 10000) for x in p]
    a = int(a * 10000)
    v = int(v * 10000)
    r = int(r * 10000) 
    t = int(t * 10000) 
    cmd = struct.pack(">iiiiiiiiiii", self.CMD_MOVE_P_LINEAR, data[0], data[1], data[2], data[3], data[4], data[5], a, v, t, r)
    self._cmd_lock.acquire()
    self._cmd_queue.put(cmd)
    self._cmd_lock.release()
    return True # TODO: implement checking result
    
  def servo_to_configuration(self, q, a=1.4, v=0.75, t=0.008):
    data = [int(x * 10000) for x in q]
    a = int(a * 10000)
    v = int(v * 10000) 
    t = int(t * 10000) 
    cmd = struct.pack(">iiiiiiiiiii", self.CMD_SERVO_Q, data[0], data[1], data[2], data[3], data[4], data[5], a, v, t, 0)
    self._cmd_lock.acquire()
    #while not self._cmd_queue.empty():
    #  self._cmd_queue.get()
    self._cmd_queue.put(cmd)
    self._cmd_lock.release()
    return True # TODO: implement checking result
    
  def speed_in_joint_space(self, qd, a=1.4):
    data = [int(x * 10000) for x in qd]
    a = int(a * 10000)
    cmd = struct.pack(">iiiiiiiiiii", self.CMD_SPEED_Q, data[0], data[1], data[2], data[3], data[4], data[5], a, 0, 0, 0)
    self._cmd_lock.acquire()
    #while not self._cmd_queue.empty():
    #  self._cmd_queue.get()
    self._cmd_queue.put(cmd)
    self._cmd_lock.release()
    return True # TODO: implement checking result
  
  def speed_in_tool_space(self, xd, a=1.4):
    data = [int(x * 10000) for x in xd]
    a = int(a * 10000)
    cmd = struct.pack(">iiiiiiiiiii", self.CMD_SPEED_P, data[0], data[1], data[2], data[3], data[4], data[5], a, 0, 0, 0)
    self._cmd_lock.acquire()
    #while not self._cmd_queue.empty():
    #  self._cmd_queue.get()
    self._cmd_queue.put(cmd)
    self._cmd_lock.release()
    return True # TODO: implement checking result

if __name__ == "__main__":
  pass
