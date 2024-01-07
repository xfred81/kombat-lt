from handset import Handset
from virtualoperator.eyes import Eyes

import numpy as np
import time
import math


class Operator:
    def __init__(self, handset: Handset, pattern: np.array):
        self._handset = handset
        self._eyes = Eyes()
        self._pattern = pattern
        self._p0 = None
        self._drift = None
        
        print("Finding pattern's original position... ", end='')
        while self._p0 is None:
            self._p0 = self._find_pattern()
            time.sleep(1)
        
        print("ok.")
        self.learn()
        print("\rVirtual operator is ready.")
        
    def _find_pattern(self):
        return self._eyes.find(self._pattern)
    
    def _press_and_measure(self, b: int):
        p0 = self._find_pattern()
        
        self._handset.get_button(b).press()
        time.sleep(2)
        
        p1 = self._find_pattern()
        
        if p0 is not None and p1 is not None:
            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]
            return dx, dy
        else:
            return None        

    def _measure_drift(self):
        
        print("Measuring normal drift: ", end='', flush=True)
        tme = 3
        time.sleep(tme)
        p1 = None
        while p1 is None:
            p1 = self._find_pattern()
            time.sleep(1)
            tme += 1

        dx = p1[0] - self._p0[0]  
        dy = p1[1] - self._p0[1]

        self._drift = dx, dy, math.sqrt(dx**2+dy**2)
        print(f"({self._drift})")
        
        
    def learn(self):
        self._measure_drift()
        
        
        
        buttons = self._handset.get_buttons_number()
        its = 2
        
        tot = its * buttons
        it = 0
        print("Calibration...", end='')
        for i in range(0, its):
            for b in range(0, buttons):
                m = None
                while m is None:
                    m = self._press_and_measure(b)
                    if m is not None:
                        dt = math.sqrt(m[0]**2+m[1]**2)
                        if dt < self._drift[2]*4:
                            m = None
                            print(f"(dt={dt}, too low, retry)")
                            self._handset.get_button(b).cancel()
                        else:
                            self._handset.get_button(b).learn_press(m[0], m[1])
                    else:
                        print("(no pattern, retry)")
                    
                it += 1
                pc = (it*100)/tot
                print("\rCalibration: {:.1f}".format(pc), end='')
                
        print("Calibrated with following information:")
        for i in range(0, buttons):
            print(f" - b{i} {self._handset.get_button(i).expected_motion}")
                
    @staticmethod    
    def _delta(v0, v1):
        dx = v1[0] - v0[0]
        dy = v1[1] - v0[1]
        return dx, dy, math.sqrt(dx**2+dy**2)
                   
    def guide_once(self):
        p1 = None
        
        while p1 is None:
            p1 = self._find_pattern()
            if p1 is None:
                time.sleep(1)
                print("Can't find pattern")
            
        dx, dy, dt = self._delta(self._p0, p1)   
        
        buttons = self._handset.get_buttons_number()
        
        if dt > 10:   
            min_ndt = None
            min_ndt_b = None
            for b in range(0, buttons):
                btn = self._handset.get_button(b)
                xp = btn.expected_motion
            
                ndx = dx + xp[0]
                ndy = dy + xp[1]
            
                ndt = math.sqrt(ndx**2 + ndy**2)
                if min_ndt is None or ndt < min_ndt:
                    min_ndt = ndt
                    min_ndt_b = b
            
            if min_ndt < dt:
                self._press_and_measure(min_ndt_b)
            else:
                time.sleep(1)

        return dt