import time


class DelayStage:
    
    def __init__(self, t0):
        self.ready = False
        self.t0 = t0
        self.min_mm = 0.0
        self.max_mm = 300.0
        # old TCPIP settings (host='192.168.0.1', port=50000)
        # note that the axis should be 'A'
        
    def initialise(self):
        self.REF()
        self.ready = True
        return

    def home(self):
        self.GOH()
        return
        
    def move_to(self, time_point_ps):
        new_pos_mm = self.convert_ps_to_mm(float(time_point_ps+self.t0))
        self.MOV(new_pos_mm)
        return
        
    def convert_ps_to_mm(self, time_ps):
        pos_mm = 0.299792458*time_ps/2
        return pos_mm

    def close(self):
        self.EXIT()
        return
        
    def check_times(self, times):
        all_on_stage = True
        for t in times:
            pos = self.convert_ps_to_mm(float(t+self.t0))
            if (pos > self.max_mm) or (pos < self.min_mm):
                all_on_stage = False
        return all_on_stage
        
    def check_time(self, time):
        on_stage = True
        pos = self.convert_ps_to_mm(float(time+self.t0))
        if (pos > self.max_mm) or (pos < self.min_mm):
            on_stage = False
        return on_stage
    
    ###########################################################################
    ###########################################################################
    ###########################################################################
    
    # basic commands to mimic the DLL (or we may do serial read/write)
    
    def MOV(self, pos_mm):
        time.sleep(0.1)
        return
    
    def GOH(self):
        time.sleep(0.1)
        return
    
    def REF(self):
        time.sleep(0.1)
        return
    
    def EXIT(self):
        return