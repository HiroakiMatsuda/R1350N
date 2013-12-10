#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file IMUR1350N.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import imu


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
imur1350n_spec = ["implementation_id", "IMUR1350N", 
		 "type_name",         "IMUR1350N", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Hiroaki Matsuda", 
		 "category",          "SENSOR", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 "conf.default.baudrate", "115200",
		 "conf.default.device", "COM1",
		 "conf.__widget__.baudrate", "text",
		 "conf.__widget__.device", "text",
		 ""]
# </rtc-template>

##
# @class IMUR1350N
# @brief ModuleDescription
# 
# 
class IMUR1350N(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_acceleration3d = RTC.Acceleration3D(0.0, 0.0, 0.0)
		"""
		"""
		self._accelerationOut = OpenRTM_aist.OutPort("acceleration", self._d_acceleration3d)
		self._d_angle = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._angleOut = OpenRTM_aist.OutPort("angle", self._d_angle)


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		"""
		
		 - Name:  config_baudrate
		 - DefaultValue: 115200
		"""
		self._config_baudrate = [115200]
		"""
		
		 - Name:  config_device
		 - DefaultValue: COM1
		"""
		self._config_device = ['COM1']
		
		# </rtc-template>


	def onInitialize(self):
		# Bind variables and configuration variable
		self.bindParameter("baudrate", self._config_baudrate, "115200")
		self.bindParameter("device", self._config_device, "COM1")
		
		# Set InPort buffers
		
		# Set OutPort buffers
		self.addOutPort("acceleration",self._accelerationOut)
		self.addOutPort("angle",self._angleOut)
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		self.myimu = imu.R1350N()
		
                #self._d_angle.data = [0.0, 0.0, 0.0, 0.0]
		
		return RTC.RTC_OK
	

	def onActivated(self, ec_id):
	
		self.myimu.open_port(self._config_device[0], self._config_baudrate[0])
                print('Open Port %s') % self._config_device[0]
                self.myimu.initialize(82)
		self.myimu.cue_data()
		
		return RTC.RTC_OK
	

	def onDeactivated(self, ec_id):
		self.myimu.close_port()
                print('Close Port %s') % self._config_device[0]
	
		return RTC.RTC_OK
	

	def onExecute(self, ec_id):
	
		try:
			angle = [0.0, 0.0, 0.0, 0.0]
			acceleration = [0.0, 0.0, 0.0]
			angle[0], angle[1], angle[2], angle[3], acceleration[0], acceleration[1], acceleration[2] = self.myimu.read_data()
			print('%03d Angle:%03d') % (angle[0], angle[1])
			
			self._d_angle.data = angle
			self._d_acceleration3d.ax = acceleration[0]
			self._d_acceleration3d.ay = acceleration[1]
			self._d_acceleration3d.az = acceleration[2]
			
			OpenRTM_aist.setTimestamp(self._d_angle)
			self._accelerationOut.write()
			self._angleOut.write()
			
		except:
			self.myimu.cue_data()
			

	
		return RTC.RTC_OK
	

def IMUR1350NInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=imur1350n_spec)
    manager.registerFactory(profile,
                            IMUR1350N,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    IMUR1350NInit(manager)

    # Create a component
    comp = manager.createComponent("IMUR1350N")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

