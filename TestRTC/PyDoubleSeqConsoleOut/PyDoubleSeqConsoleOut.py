#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file PyDoubleSeqConsoleOut.py
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
pydoubleseqconsoleout_spec = ["implementation_id", "PyDoubleSeqConsoleOut", 
		 "type_name",         "PyDoubleSeqConsoleOut", 
		 "description",       "ModuleDescription", 
		 "version",           "1.0.0", 
		 "vendor",            "Hiroaki Matsuda", 
		 "category",          "CONSOLE", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class PyDoubleSeqConsoleOut
# @brief ModuleDescription
# 
# 
class PyDoubleSeqConsoleOut(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

		self._d_data = RTC.TimedDoubleSeq(RTC.Time(0,0),[])
		"""
		"""
		self._dataIn = OpenRTM_aist.InPort("data", self._d_data)


		

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
			print self._d_data.data
			
		return RTC.RTC_OK
	



def PyDoubleSeqConsoleOutInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=pydoubleseqconsoleout_spec)
    manager.registerFactory(profile,
                            PyDoubleSeqConsoleOut,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    PyDoubleSeqConsoleOutInit(manager)

    # Create a component
    comp = manager.createComponent("PyDoubleSeqConsoleOut")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

