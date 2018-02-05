#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil

class ResourceInfo:
	def __init__(self, logger):
		self._logger = logger

	def doProcess(self):
		self._logger.debug(psutil.cpu_times())
		self.getCpuInfo()
		self.getMemoryInfo()
		self.getDiskInfo()
		self.getNetworkInfo()
		self.getSensorInfo()
		self.getSystemInfo()
		self.getProcessManagementInfo()
		self.getFurtherProcessApiInfo()
		self.getPopenWrapperInfo()


	def getCpuInfo(self):
		self._logger.info("<CPU Info>")
		self._logger.debug(psutil.cpu_percent(interval=1, percpu=True))
		self._logger.debug(psutil.cpu_times_percent(interval=1, percpu=False))

		self._logger.debug(psutil.cpu_count())
		self._logger.debug(psutil.cpu_count(logical=False))

		# self._logger.debug(psutil.cpu_stats())
		# self._logger.debug(psutil.cpu_freq())
		print '\n'


	def getMemoryInfo(self):
		self._logger.info("<Memory Info>")
		self._logger.debug(psutil.virtual_memory())
		self._logger.debug(psutil.swap_memory())
		print '\n'


	def getDiskInfo(self):
		self._logger.info("<Disk Info>")
		self._logger.debug(psutil.disk_partitions())
		self._logger.debug(psutil.disk_usage('/'))
		self._logger.debug(psutil.disk_io_counters(perdisk=False))


	def getNetworkInfo(self):
		self._logger.info("<Network Info>")
		self._logger.debug(psutil.net_io_counters(pernic=True))
		# self._logger.debug(psutil.net_connections())
		self._logger.debug(psutil.net_if_addrs())
		self._logger.debug(psutil.net_if_stats())
		print '\n'


	def getSensorInfo(self):
		self._logger.info("<Sensor Info>")
		# self._logger.debug(psutil.sensors_temperatures())
		# self._logger.debug(psutil.sensors_fans())
		# self._logger.debug(psutil.sensors_battery())
		print '\n'


	def getSystemInfo(self):
		self._logger.info("<System Info>")
		self._logger.debug(psutil.users())
		self._logger.debug(psutil.boot_time())
		print '\n'


	def getProcessManagementInfo(self):
		self._logger.info("<Process Management Info>")
		self._logger.debug(psutil.pids())
		p = psutil.Process(27310)
		self._logger.debug(p.name())
		self._logger.debug(p.exe())
		self._logger.debug(p.cwd())
		self._logger.debug(p.cmdline())
		self._logger.debug(p.pid)
		self._logger.debug(p.ppid())
		self._logger.debug(p.parent())
		self._logger.debug(p.children())
		self._logger.debug(p.status())
		self._logger.debug(p.username())
		self._logger.debug(p.create_time())
		self._logger.debug(p.terminal())
		self._logger.debug(p.uids())
		self._logger.debug(p.gids())
		self._logger.debug(p.cpu_times())
		self._logger.debug(p.cpu_percent(interval=1.0))
		# self._logger.debug(p.cpu_affinity())
		# self._logger.debug(p.cpu_affinity([0, 1]))  # setp.cpu_num())
		self._logger.debug(p.memory_info())
		# self._logger.debug(p.memory_full_info())  # "real" USS memory usage (Linux, OSX, Win only))
		self._logger.debug(p.memory_percent())
		# self._logger.debug(p.memory_maps())
		# self._logger.debug(p.io_counters())
		self._logger.debug(p.open_files())
		self._logger.debug(p.connections())
		self._logger.debug(p.num_threads())
		self._logger.debug(p.num_fds())
		# self._logger.debug(p.threads())
		self._logger.debug(p.num_ctx_switches())
		self._logger.debug(p.nice())
		self._logger.debug(p.nice(10))  # setp.ionice(psutil.IOPRIO_CLASS_IDLE)  # IO priority (Win and Linux only)p.ionice())
		# self._logger.debug(p.rlimit(psutil.RLIMIT_NOFILE, (5, 5)))  # set resource limits (Linux only)p.rlimit(psutil.RLIMIT_NOFILE))
		# self._logger.debug(p.environ())
		self._logger.debug(p.as_dict())
		self._logger.debug(p.is_running())
		self._logger.debug(p.suspend())
		self._logger.debug(p.resume())
		# self._logger.debug(p.terminate())
		# self._logger.debug(p.wait(timeout=3))
		# self._logger.debug(psutil.test())
		print '\n'


	def getFurtherProcessApiInfo(self):
		self._logger.info("<Further Process API Info>")
		# for proc in psutil.process_iter(attrs=['pid', 'name']):
			# self._logger.debug(proc.info)
		# self._logger.debug(psutil.pid_exists(3))
		print '\n'


	def getPopenWrapperInfo(self):
		self._logger.info("<SPopen Wrapper Info>")
		from subprocess import PIPE
		p = psutil.Popen(["/usr/bin/python", "-c", "print('hello')"], stdout=PIPE)

		self._logger.debug(p.name())
		self._logger.debug(p.username())
		self._logger.debug(p.communicate())
		self._logger.debug(p.wait(timeout=2))
		print '\n'
