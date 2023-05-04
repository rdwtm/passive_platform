import copy
import time
import threading
import logging
import queue as queue
from threading import Lock
import numpy
import rtde_control
import rtde_receive


class URRTDEInterface:
  
  def __init__(self, robot_ip):
    self._robot_ip = robot_ip
    self.connected = False
    
    self.timestamp = 0
    self._joint_positions = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._joint_velocities = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._joint_torques = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._joint_currents = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._tool_position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._tool_velocity = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._tool_force = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    self._is_moving = False
    
    self.digital_inputs = 0
    self.digital_outputs = 0
    
    self._state_lock = Lock()
    
  def __del__(self):
    self.connected = False
    #self.data_thread.join()
    self.disconnect()
    
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
    print(self._robot_ip)
    self.rtde_c = rtde_control.RTDEControlInterface(self._robot_ip)
    self.rtde_r = rtde_receive.RTDEReceiveInterface(self._robot_ip)
    self.connected = True
    
    self.data_thread = threading.Thread(target=self.data_thread)
    self.data_thread.daemon = True
    self.data_thread.start()
    
  def disconnect(self):
    self._connected = False
    #self._socket.close()
    # TODO
  
  def data_thread(self):
    print("Starting data thread...")
    t0 = time.time()
    while self.connected:
      t = time.time() - t0
      
      self._state_lock.acquire()
      self._joint_positions = self.rtde_r.getActualQ()
      self._joint_velocities = self.rtde_r.getActualQd()
      self._joint_currents = self.rtde_r.getActualCurrent()
      self._tool_position = self.rtde_r.getActualTCPPose()
      self._tool_velocity = self.rtde_r.getActualTCPSpeed()
      self._tool_force = self.rtde_r.getActualTCPForce()
      self._state_lock.release()
  
  def is_moving(self):
    return self._is_moving

  def stop_robot(self):
    self.rtde_c.stopJ()
  
  def move_to_configuration(self, q, a=1.4, v=0.75, t=0, r=0):
    self.rtde_c.moveJ(q, True)
    
  def move_to_configuration_linear(self, q, a=1.4, v=0.75, t=0, r=0):
    self.rtde_c.moveL_FK(q, True)
  
  def move_to_pose(self, p, a=1.4, v=0.75, t=0, r=0):
    self.rtde_c.moveJ_IK(p, True)
    
  def move_to_pose_linear(self, p, a=1.4, v=0.75, t=0, r=0):
    self.rtde_c.moveL(p, True)
    
  def servo_to_configuration(self, q, a=1.4, v=0.75, t=0.008):
    dself.rtde_c.servoJ(q)
    
  def speed_in_joint_space(self, qd, a=1.4):
    self.rtde_c.speedJ(qd)
  
  def speed_in_tool_space(self, xd, a=1.4):
    self.rtde_c.speedL(xd)

if __name__ == "__main__":
  pass
