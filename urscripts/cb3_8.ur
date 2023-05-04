def kair_urscript():
	textmsg("Starting program kair_urscript")
  
  #---------------------------------------------------------------------
  # constants and variables
  #---------------------------------------------------------------------
  host = "192.168.0.154"
  port = 33333
  global qtarget = [0, 0, 0, 0, 0, 0]
  global posetarget = p[0, 0, 0, 0, 0, 0]
  global dqtarget = [0, 0, 0, 0, 0, 0]
  global acceleration = 1.4
  global tool_acceleration = 1.2
  global speed = 0.75
  global time = 0.0
  global blend = 0.0
  global motionFinished = 0
  global isServoing = 0
  global isStopped = 1
  global receive_buffer = [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  global receive_buffer18 = [18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  global FLOAT_SCALE = 0.0001
  global mass = 0.0
  global center_of_gravity = [0, 0, 0]

  #---------------------------------------------------------------------
  # Stop robot
  #---------------------------------------------------------------------
  def stop_robot():
    textmsg("Stopping robot")
    stopj(10)
    isServoing = 0
    isStopped = 1
  end

  #---------------------------------------------------------------------
  # Move to configuration
  #---------------------------------------------------------------------
  def move_q():
    textmsg("move_q()")
    cnt = 0           
    enter_critical  
      motionFinished = 0      
      while cnt < 6:
        qtarget[cnt] = receive_buffer[cnt+2]*FLOAT_SCALE
        cnt = cnt + 1
      end
    exit_critical

    acceleration = receive_buffer[8] * FLOAT_SCALE
    speed = receive_buffer[9] * FLOAT_SCALE
    time = receive_buffer[10] * FLOAT_SCALE
    blend = receive_buffer[11] * FLOAT_SCALE

    movej(qtarget, acceleration, speed, time, blend)
    
    enter_critical
      motionFinished = 1
    exit_critical
  end
  
  #---------------------------------------------------------------------
  # Move to configuration linear
  #---------------------------------------------------------------------
  def move_q_linear():
    textmsg("move_q_linear()")
    cnt = 0           
    enter_critical  
      motionFinished = 0      
      while cnt < 6:
        qtarget[cnt] = receive_buffer[cnt+2]*FLOAT_SCALE
        cnt = cnt + 1
      end
    exit_critical

    acceleration = receive_buffer[8] * FLOAT_SCALE
    speed = receive_buffer[9] * FLOAT_SCALE
    time = receive_buffer[10] * FLOAT_SCALE
    blend = receive_buffer[11] * FLOAT_SCALE

    movel(qtarget)
    
    enter_critical
      motionFinished = 1
    exit_critical
  end
  
  #---------------------------------------------------------------------
  # Move to pose
  #---------------------------------------------------------------------
  def move_p():
    textmsg("move_p()")
    cnt = 0           
    enter_critical  
      motionFinished = 0      
      while cnt < 6:
        posetarget[cnt] = receive_buffer[cnt+2]*FLOAT_SCALE
        cnt = cnt + 1
      end
    exit_critical

    acceleration = receive_buffer[8] * FLOAT_SCALE
    speed = receive_buffer[9] * FLOAT_SCALE
    time = receive_buffer[10] * FLOAT_SCALE
    blend = receive_buffer[11] * FLOAT_SCALE

    movej(posetarget, acceleration, speed, time, blend)
    
    enter_critical
      motionFinished = 1
    exit_critical
  end
  
  #---------------------------------------------------------------------
  # Move to pose linear
  #---------------------------------------------------------------------
  def move_p_linear():
    textmsg("move_p_linear()")
    cnt = 0           
    enter_critical  
      motionFinished = 0      
      while cnt < 6:
        posetarget[cnt] = receive_buffer[cnt+2]*FLOAT_SCALE
        cnt = cnt + 1
      end
    exit_critical

    acceleration = receive_buffer[8] * FLOAT_SCALE
    speed = receive_buffer[9] * FLOAT_SCALE
    time = receive_buffer[10] * FLOAT_SCALE
    blend = receive_buffer[11] * FLOAT_SCALE

    movel(posetarget, acceleration, speed, time, blend)
    
    enter_critical
      motionFinished = 1
    exit_critical
  end

  #---------------------------------------------------------------------
  # Servo to configuration
  #---------------------------------------------------------------------
  def servo_q():
    cnt = 0           
    enter_critical        
      while cnt < 6:
        qtarget[cnt] = receive_buffer[cnt+2]*FLOAT_SCALE
        cnt = cnt + 1
      end
      acceleration = receive_buffer[8] * FLOAT_SCALE
      speed = receive_buffer[9] * FLOAT_SCALE
    exit_critical
        
    enter_critical
      motionFinished = 1
    exit_critical
  end
  
  thread servo_thread():
    while isServoing == 1:
      enter_critical
        q = qtarget
      exit_critical
      servoj(q, acceleration, speed, 0.008)
      #sync()
    end
  end
  
  #---------------------------------------------------------------------
  # Speed in configuration space
  #---------------------------------------------------------------------
  def speed_q():
    cnt = 0           
    enter_critical        
      while cnt < 6:
        dqtarget[cnt] = receive_buffer[cnt+2]*FLOAT_SCALE
        cnt = cnt + 1
      end
      acceleration = receive_buffer[8] * FLOAT_SCALE
    exit_critical
  end
  
  thread speed_thread():
    while isServoing == 2:
      enter_critical
        dq = dqtarget
      exit_critical
      speedj(dq, acceleration, 0.008)
      #sync()
    end
  end
  
  #---------------------------------------------------------------------
  # Speed in Cartesian space
  #---------------------------------------------------------------------
  def speed_p():
    cnt = 0           
    enter_critical        
      while cnt < 6:
        dqtarget[cnt] = receive_buffer[cnt+2]*FLOAT_SCALE
        cnt = cnt + 1
      end
      acceleration = receive_buffer[8] * FLOAT_SCALE
    exit_critical
  
    enter_critical
      motionFinished = 1
    exit_critical
  end
  
  thread cartesian_thread():
    while isServoing == 3:
      enter_critical
        dp = dqtarget
        #dp = [-0.01, 0, 0, 0, 0, 0]
      exit_critical
      speedl(dp, acceleration, 0.008)
    end
  end

  #---------------------------------------------------------------------
  # Set IO
  #---------------------------------------------------------------------
  def set_io():
    textmsg("setIO()")
    id = receive_buffer[2]
    onoff = receive_buffer[3]
    if onoff == 1:
      set_digital_out(id, True)
    else:
      set_digital_out(id, False)
    end	
  end

  #---------------------------------------------------------------------
  # Set TCP payload
  #---------------------------------------------------------------------
  def set_tcp_payload():
    textmsg("setTcpPayload()")
    cnt = 0
    mass = receive_buffer[cnt+2]*FLOAT_SCALE
    cnt = cnt + 1
    while cnt < 4:
      center_of_gravity[cnt - 1] = receive_buffer[cnt+2]*FLOAT_SCALE
      cnt = cnt + 1
    end

    textmsg("New payload: ")
    textmsg(mass)
    textmsg("Center of gravity: ")
    textmsg(center_of_gravity)
    
    set_payload(mass, center_of_gravity) 
  end

  #---------------------------------------------------------------------
  # The main loop
  #---------------------------------------------------------------------
  textmsg("Connecting with host")
  opened = socket_open(host, port)
  while opened == False:
    opened = socket_open(host, port)
  end 
  textmsg("Connected")
  
  global servo_thrd = run speed_thread()
  
  errcnt = 0
  while errcnt < 1:       
    receive_buffer = socket_read_binary_integer(11)
    
    if receive_buffer[0] != 11:
      #textmsg("Did not receive 11 integers as expected")

      
    elif receive_buffer[1] == 0: #0: Stop Robot
      isServoing = 0
      kill servo_thrd
      if isStopped == 0:
        stop_robot()
      end
      
                 
    elif receive_buffer[1] == 1: #1: move_q()
      isStopped = 0
      if isServoing != 0:
        isServoing = 0
        kill servo_thrd
      end
      move_q()
      
    elif receive_buffer[1] == 2: #2: move_q_linear()
      isStopped = 0
      if isServoing != 0:
        isServoing = 0
        kill servo_thrd
      end
      move_q_linear()
      
    elif receive_buffer[1] == 3: #3: move_p()
      isStopped = 0
      if isServoing != 0:
        isServoing = 0
        kill servo_thrd
      end
      move_p()
    
    elif receive_buffer[1] == 4: #4: move_p_linear()
      isStopped = 0
      if isServoing != 0:
        isServoing = 0
        kill servo_thrd
      end
      move_p_linear()
      
    elif receive_buffer[1] == 5: #5: servo_q()
      isStopped = 0
      servo_q()
      if isServoing != 1:
        isServoing = 1
        kill servo_thrd
        servo_thrd = run servo_thread()
      end
      
    elif receive_buffer[1] == 6: #6: speed_q()
      isStopped = 0
      speed_q()
      if isServoing != 2:
        isServoing = 2
        kill servo_thrd
        servo_thrd = run speed_thread()
      end
    
    elif receive_buffer[1] == 7: #7: speed_p()
      isStopped = 0
      speed_p()
      if isServoing != 3:
        isServoing = 3
        kill servo_thrd
        servo_thrd = run cartesian_thread()
      end
      
    elif receive_buffer[1] == 9: #9: Set IO
      set_io()
      
    elif receive_buffer[1] == 10: #10: Set Payload
      set_tcp_payload()	
      
    elif receive_buffer[1] == 9999: #1: Do nothing
      #isStopped = 0
      #isServoing = 0
    end
    
    sync()

  end
  
  textmsg("Program finished")
end

run program
