#!/usr/bin/env python
# Copyright 2013 David Irvine
#
# This file is part of openlava-python
#
# openlava-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# openlava-python is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openlava-python.  If not, see <http://www.gnu.org/licenses/>.
import unittest
from openlava.lslib import ls_getclustername, ls_getmastername, ls_gethostinfo, HostInfo, ls_info, LsInfo, ResItem,ls_gethosttype,ls_gethostmodel, get_lserrno, LSBE_NO_ERROR
from openlava.lsblib import lsb_init,lsb_queueinfo,lsb_hostinfo,HostInfoEnt, lsb_openjobinfo, lsb_readjobinfo, lsb_closejobinfo, JobInfoEnt, Submit, lsb_userinfo, UserInfoEnt,lsb_submit, Submit, SubmitReply

class LsBlib(unittest.TestCase):
	def test_users(self):
		self.assertGreaterEqual(lsb_init("Test Case"), 0)
		users=lsb_userinfo()
		self.assertIsNotNone(users)
		for user in users:
			self.check_user(user)

	def test_submit(self):
		s=Submit()
		s.command="hostname"
		s.maxNumProcessors=1
		s.numProcessors=1
		r=SubmitReply()
		job_id=lsb_submit(s,r)
		self.assertGreaterEqual(job_id,0)

	def check_user(self, u):
		self.assertIsInstance(u, UserInfoEnt)
		self.assertIsInstance(u.user,unicode)
		methods=[
				'procJobLimit',
				'maxJobs',
				'numStartJobs',
				'numJobs',
				'numPEND',
				'numRUN',
				'numSSUSP',
				'numUSUSP',
				'numRESERVE',
				]
		for i in methods:
			self.assertGreaterEqual(getattr(u,i),0)

		
	def test_job(self):
		self.assertGreaterEqual(lsb_init("Test Case"), 0)
		num_jobs=lsb_openjobinfo(job_id=1)
		self.assertEqual( num_jobs, -1)
		lsb_closejobinfo()

	def test_jobs(self):
		num_jobs=lsb_openjobinfo()
		self.assertEqual( get_lserrno(), LSBE_NO_ERROR)
		for i in range(num_jobs):
			job=lsb_readjobinfo()
			self.check_job(job)
			lsb_closejobinfo()
			self.assertEqual( get_lserrno(), LSBE_NO_ERROR )

	def check_job(self,job):
		self.assertIsInstance(job, JobInfoEnt)
		ints=[
			'jobId',
			'status',
			'numReasons',
			'reasons',
			'subreasons',
			'jobPid',
			'submitTime',
			'reserveTime',
			'startTime',
			'predictedStartTime',
			'endTime',
			'umask',
			'numExHosts','nIdx',
			'exitStatus',
			'execUid',
			'jType',
			'port',
			'jobPriority',
			'jRusageUpdateTime'
			]
		for attr in ints:
			self.assertIsInstance(getattr(job,attr),int)
		for a in range(7):
			self.assertIsInstance(job.counter[a],int)

		for attr in ['cwd','subHomeDir','fromHost','execHome','execCwd','execUsername','parentGroup','jName',]:
			self.assertIsInstance(getattr(job,attr),unicode)
		
		self.assertIsInstance(job.exHosts,list)
		for host in job.exHosts:
			self.assertIsInstance(host, unicode)

		self.assertIsInstance(job.loadSched,list)
		self.assertIsInstance(job.loadStop,list)
		self.assertEqual(len(job.loadSched), job.nIdx)
		self.assertEqual(len(job.loadStop), job.nIdx)
		for l in job.loadSched:
			self.assertIsInstance(l,float)
		for l in job.loadStop:
			self.assertIsInstance(l,float)
		for a in [job.cpuFactor, job.cpuTime]:
			self.assertIsInstance(a,float)

		s=job.submit
		self.assertIsInstance(s,Submit)
		for attr in [
				'options',
				'options2',
				'numAskedHosts',
				'numProcessors',
				'sigValue',
				'nxf',
				'delOptions',
				'delOptions2',
				'maxNumProcessors',
				'userPriority',
				'beginTime',
				'termTime',
				'chkpntPeriod',
				]:
			self.assertIsInstance(getattr(s,attr),int)
		for attr in [
				'jobName',
				'queue',
				'resReq',
				'hostSpec',
				'dependCond',
				'inFile',
				'outFile',
				'errFile',
				'command',
				'chkpntDir',
				'preExecCmd',
				'mailUser',
				'projectName',
				'loginShell',]:
			self.assertIsInstance(getattr(s,attr),unicode)
		self.assertEqual(len(s.askedHosts),s.numAskedHosts)
		for h in s.askedHosts:
			self.assertIsInstance(h,unicode)
		for r in range(10):
			self.assertIsInstance(s.rLimits[r],int)
			self.assertGreaterEqual(s.rLimits[r],-1)
		xf=s.xf
		self.assertEqual(len(xf), s.nxf)
		self.assertIsInstance(xf,list)
		for a in xf:
			self.assertIsInstance(a.subFn,unicode)
			self.assertIsInstance(a.execFn,unicode)
			self.assertIsInstance(a.options,int)
		ru=job.runRusage
		for a in ['mem','swap','utime','stime','npids','npgids']:
			self.assertIsInstance(getattr(ru,a),int)
			self.assertGreaterEqual(getattr(ru,a),-1)
			inf=ru.pidInfo
			self.assertEqual(len(inf),ru.npids)
			for pi in inf:
				for a in ['pid','ppid','pgid','jobid']:
					self.assertGreaterEqual(getattr(pi,a),-1)
			for g in range(ru.npgids):
				self.assertGreaterEqual(ru.pgid[g],-1)


	def test_init(self):
		self.assertGreaterEqual(lsb_init("Test Case"), 0)
	def test_queueinfo(self):
		lsb_init("test queues")
		queues=lsb_queueinfo()
		self.assertIsInstance(queues,list)
		for queue in queues:
			self.check_queue(queue)

	def test_hostinfo(self):
		lsb_init("test hosts")
		hosts=lsb_hostinfo()
		self.assertIsInstance(hosts,list)
		for host in hosts:
			self.check_host(host)

	def check_queue(self, queue):
		self.assertIsInstance(queue.queue,unicode)
		self.assertNotEqual(queue.queue,"")
		self.assertIsInstance(queue.description,unicode)
		self.assertIsInstance(queue.priority,int)
		self.assertIsInstance(queue.nice,int)
		self.assertIsInstance(queue.userList, list)
		for user in queue.userList:
			self.assertIsInstance(user, unicode)
			self.assertNotEqual(user,"")
		self.assertIsInstance(queue.hostList, list)
		for host in queue.hostList:
			self.assertIsInstance(host, unicode)
			self.assertNotEqual(host,"")

		self.assertIsInstance(queue.nIdx, int)
		self.assertGreaterEqual(queue.nIdx,0)
		self.assertEqual(queue.nIdx, len(queue.loadSched))
		self.assertEqual(queue.nIdx, len(queue.loadStop))
		self.assertIsInstance(queue.userJobLimit,int)
		self.assertIsInstance(queue.procJobLimit,float)
		self.assertIsInstance(queue.windows,unicode)
		self.assertIsInstance(queue.rLimits,list)
		self.assertEqual(len(queue.rLimits), 11)
		for i in queue.rLimits:
			self.assertIsInstance(i,int)
			self.assertGreaterEqual(i,-1)
		self.assertIsInstance(queue.hostSpec, unicode)
		self.assertIsInstance(queue.qAttrib, int)
		self.assertIsInstance(queue.qStatus, int)
		self.assertIsInstance(queue.maxJobs, int)
		self.assertIsInstance(queue.numJobs, int)
		self.assertIsInstance(queue.numPEND, int)
		self.assertIsInstance(queue.numRUN, int)
		self.assertIsInstance(queue.numSSUSP, int)
		self.assertIsInstance(queue.numUSUSP, int)
		self.assertIsInstance(queue.mig, int)
		self.assertIsInstance(queue.schedDelay, int)
		self.assertIsInstance(queue.acceptIntvl, int)

	def check_host(self,host):
		self.assertIsInstance(host, HostInfoEnt)



class LsLib(unittest.TestCase):
	def test_clustername(self):
		self.assertTrue(ls_getclustername())
	def test_mastername(self):
		self.assertTrue(ls_getmastername())
	
	def check_resource(self,res):
			self.assertIsInstance(res, ResItem)
			self.assertIsInstance(res.name, unicode)
			self.assertNotEqual(res.name,"")
			self.assertIsNotNone(res.name)

			self.assertIsInstance(res.des, unicode)

			self.assertIsInstance(res.flags, int)
			self.assertGreaterEqual(res.flags, 0)

			self.assertIsInstance(res.interval, int)
			self.assertGreaterEqual(res.interval,0)

			self.assertIsInstance(res.valueType, unicode)
			self.assertIn(res.valueType, [u"LS_BOOLEAN",u"LS_NUMERIC",u"LS_STRING",u"LS_EXTERNAL"])

			self.assertIsInstance(res.orderType, unicode)
			self.assertIn(res.orderType, [u"INCR", u"DECR", u"NA"])

	def test_lsinfo(self):
		ls=ls_info()
		self.assertIsInstance(ls,LsInfo)
		self.assertIsInstance(ls.nRes, int)
		self.assertGreaterEqual(ls.nRes,0)
		for res in ls.resTable:
			self.check_resource(res)

		self.assertIsInstance(ls.nTypes,int)
		self.assertGreaterEqual(ls.nTypes,0)
		for t in ls.hostTypes:
			self.assertIsInstance(t,unicode)
			self.assertIsNotNone(t)
			self.assertNotEqual(t,"")

		self.assertIsInstance(ls.nModels,int)
		self.assertGreaterEqual(ls.nModels,0)
		for m in ls.hostModels:
			self.assertIsInstance(m,unicode)
			self.assertIsNotNone(m)
			self.assertNotEqual(m,"")
		for a in ls.hostArchs:
			self.assertIsInstance(a,unicode)
			self.assertIsNotNone(a)
			self.assertNotEqual(a,"")
		for r in ls.modelRefs:
			self.assertIsInstance(r,int)
			self.assertIsNotNone(r)
			self.assertGreaterEqual(r,0)
		for c in ls.cpuFactor:
			self.assertIsInstance(c,float)
			self.assertGreaterEqual(c,0)
		self.assertIsInstance(ls.numIndx,int)
		self.assertIsInstance(ls.numUsrIndx,int)

	def test_gethostinfo(self):
		hosts=ls_gethostinfo()
		hinfo={}
		for host in hosts:
			hinfo[host.hostName]={}
			self.assertIsInstance(host,HostInfo)
			self.assertIsInstance(host.hostName, unicode)
			self.assertNotEqual(host.hostName,"")
			self.assertIsNotNone(host.hostName)

			self.assertIsInstance(host.hostType, unicode)
			self.assertNotEqual(host.hostType,"")
			self.assertIsNotNone(host.hostType)
			hinfo[host.hostName]['hostType']=host.hostType

			self.assertIsInstance(host.hostModel, unicode)
			self.assertIsNotNone(host.hostModel)
			self.assertNotEqual(host.hostModel,"")
			hinfo[host.hostName]['hostModel']=host.hostModel

			self.assertIsInstance(host.cpuFactor, float)
			self.assertGreaterEqual(host.cpuFactor,0)
			hinfo[host.hostName]['hostFactor']=host.cpuFactor

			self.assertIsInstance(host.maxCpus, int)
			self.assertGreaterEqual(host.maxCpus,0)

			self.assertIsInstance(host.maxMem, int)
			self.assertGreaterEqual(host.maxMem,0)

			self.assertIsInstance(host.maxSwap, int)
			self.assertGreaterEqual(host.maxSwap,0)

			self.assertIsInstance(host.maxTmp, int)
			self.assertGreaterEqual(host.maxTmp,0)

			self.assertIsInstance(host.nDisks, int)
			self.assertGreaterEqual(host.nDisks,0)

			self.assertIsInstance(host.nRes, int)
			self.assertGreaterEqual(host.nRes,0)

			for resource in host.resources:
				self.check_resource(resource)
			self.assertIsInstance(host.windows, unicode)
			self.assertNotEqual(host.windows,"")
			self.assertIsNotNone(host.windows)

			for load in host.busyThreshold:
				self.assertIsInstance(load, float)


			self.assertIsInstance(host.isServer,bool)
			self.assertIsInstance(host.rexPriority, int)
		for h,v in hinfo.items():
			#self.assertEqual(v['hostFactor'], ls_gethostfactor(h))
			self.assertEqual(v['hostType'], ls_gethosttype(h))
			self.assertEqual(v['hostModel'], ls_gethostmodel(h))



unittest.main()
