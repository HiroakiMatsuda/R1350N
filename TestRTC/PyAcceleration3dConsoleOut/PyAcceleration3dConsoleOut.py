#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file PyAcceleration3dConsoleOut.py
 @brief ModuleDescription
 @date $Date$


"""
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
pyacceleration3dconsoleout_spec = ["implementation_id", "PyAcceleration3dConsoleOut", 
		 "type_name",         "PyAcceleration3dConsoleOut", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "VenderName", 
		 "category",          "CONSOLE", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class PyAcceleration3dConsoleOut
# @brief ModuleDescription
# 
# 
class PyAcceleration3dConsoleOut(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_data = RTC.Acceleration3D(0.0, 0.0, 0.0)
		"""
		"""
		self._dataIn = OpenRTM_aist.InPort("data", self._d_data)


		


		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>


		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		self.addInPort("data",self._dataIn)
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		# Set CORBA Service Ports
		
		return RTC.RTC_OK
	


	def onActivated(self, ec_id):
	
		return RTC.RTC_OK
	

	def onDeactivated(self, ec_id):
	
		return RTC.RTC_OK
	

	def onExecute(self, ec_id):
	
		if self._dataIn.isNew():
			self._d_data = self._dataIn.read()
			print("Ax:%f Ay:%f Az:%f") %(self._d_data.ax, self._d_data.ay, self._d_data.az) 
	
		return RTC.RTC_OK
	


def PyAcceleration3dConsoleOutInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=pyacceleration3dconsoleout_spec)
    manager.registerFactory(profile,
                            PyAcceleration3dConsoleOut,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    PyAcceleration3dConsoleOutInit(manager)

    # Create a component
    comp = manager.createComponent("PyAcceleration3dConsoleOut")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

