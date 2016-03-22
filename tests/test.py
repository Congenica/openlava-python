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
import os
import time
try:
    from openlava import lsblib
    from openlava import lslib
    from openlava import constants
except ImportError as e:
    print "Error importing openlava modules: {}".format(e) #to get around setuptools hiding this
    raise
from openlava.utils import find_openlava

class LsblibTest(unittest.TestCase):
    def setUp(self):
        lsblib.lsb_init("test case")

    def test_users(self):
        self.assertGreaterEqual(lsblib.lsb_init("Test Case"), 0)
        users = lsblib.lsb_userinfo()
        self.assertIsNotNone(users)
        for user in users:
            self.check_user(user)

    def test_submit(self):
        s = lsblib.Submit()
        s.command = "hostname"
        s.maxNumProcessors = 1
        s.numProcessors = 1
        sr = lsblib.lsb_submit(s)
        self.assertGreaterEqual(sr.jobId, 0)

#this will alter our live queues!
#    def test_queuecontrol(self):
#        queues = lsblib.lsb_queueinfo()
#        for q in queues:
#            queueName = q.queue
#            code = lsblib.lsb_queuecontrol(queueName, constants.QUEUE_INACTIVATE)
#            code = lsblib.lsb_queuecontrol(queueName, constants.QUEUE_ACTIVATE)
#            code = lsblib.lsb_queuecontrol(queueName, constants.QUEUE_CLOSED)
#            code = lsblib.lsb_queuecontrol(queueName, constants.QUEUE_OPEN)


#this test will close hosts in our production system, so don't do that
#    def test_hostcontrol(self):
#        hosts = lsblib.lsb_hostinfo()
#        for h in hosts:
#            if h.hStatus & (constants.HOST_STAT_OK | constants.HOST_STAT_BUSY) != 0:
#                hostName = h.host
#                code = lsblib.lsb_hostcontrol(hostName, constants.HOST_CLOSE)
#                code = lsblib.lsb_hostcontrol(hostName, constants.HOST_OPEN)


    def test_xFile(self):
        x = lsblib.XFile()
        x.subFn = "foo"
        x.execFn = "bar"
        x.options = 0
        self.assertEqual(u"foo", x.subFn)
        self.assertEqual(u"bar", x.execFn)
        self.assertEqual(0, x.options)

    def check_user(self, u):
        self.assertIsInstance(u, lsblib.UserInfoEnt)
        self.assertIsInstance(u.user, basestring)
        methods = [
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
            self.assertGreaterEqual(getattr(u, i), 0)


    def test_job(self):
        try:
            num_jobs = lsblib.lsb_openjobinfo(job_id=1)
            self.assertEqual(num_jobs, 0)
        finally:
            lsblib.lsb_closejobinfo()

    def test_jobs(self):
        try:
            num_jobs = lsblib.lsb_openjobinfo()
            self.assertEqual(lsblib.get_lsberrno(), constants.LSBE_NO_ERROR)
            for i in range(num_jobs):
                job = lsblib.lsb_readjobinfo()
                self.check_job(job)
                ld = lsblib.LoadIndexLog()
                reasons = lsblib.lsb_pendreason(job.numReasons, job.reasonTb, None, ld)
                reasons = lsblib.lsb_suspreason(job.reasons, job.subreasons, ld)
                filename = lsblib.lsb_peekjob(job.jobId)
        finally:
           lsblib.lsb_closejobinfo()

    def check_job(self, job):
        self.assertIsInstance(job, lsblib.JobInfoEnt)
        ints = [
            'jobId',
            'numReasons',
            'reasons',
            'subreasons',
            'jobPid',
            'umask',
            'numExHosts', 'nIdx',
            'exitStatus',
            'execUid',
            'jType',
            'port',
            'jobPriority',
            'jRusageUpdateTime'
        ]
        for attr in ints:
            self.assertIsInstance(getattr(job, attr), int)
        for a in range(7):
            self.assertIsInstance(job.counter[a], int)

        times = [
            'predictedStartTime',
            'submitTime',
            'reserveTime',
            'startTime',
            'endTime',
        ]

        for attr in times:
            self.assertIsInstance(getattr(job, attr), time.struct_time)

        for attr in ['cwd', 'subHomeDir', 'fromHost', 'execHome', 'execCwd', 'execUsername', 'parentGroup', 'jName', 'status']:
            self.assertIsInstance(getattr(job, attr), basestring)

        self.assertIsInstance(job.exHosts, list)
        for host in job.exHosts:
            self.assertIsInstance(host, basestring)

        self.assertIsInstance(job.loadSched, list)
        self.assertIsInstance(job.loadStop, list)
        self.assertEqual(len(job.loadSched), job.nIdx)
        self.assertEqual(len(job.loadStop), job.nIdx)
        for l in job.loadSched + job.loadStop + [job.cpuFactor]:
            self.assertIsInstance(l, float)

        self.assertIsInstance(job.cpuTime, time.struct_time)

        s = job.submit
        self.assertIsInstance(s, lsblib.Submit)
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
            self.assertIsInstance(getattr(s, attr), int)
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
            'loginShell', ]:
            self.assertIsInstance(getattr(s, attr), basestring)
        self.assertEqual(len(s.askedHosts), s.numAskedHosts)
        for h in s.askedHosts:
            self.assertIsInstance(h, basestring)
        for r in range(10):
            self.assertIsInstance(s.rLimits[r], int)
            self.assertGreaterEqual(s.rLimits[r], -1)
        xf = s.xf
        self.assertEqual(len(xf), s.nxf)
        self.assertIsInstance(xf, list)
        for a in xf:
            self.assertIsInstance(a.subFn, basestring)
            self.assertIsInstance(a.execFn, basestring)
            self.assertIsInstance(a.options, int)
        ru = job.runRusage
        for a in ['mem', 'swap', 'utime', 'stime', 'npids', 'npgids']:
            self.assertIsInstance(getattr(ru, a), int)
            self.assertGreaterEqual(getattr(ru, a), -1)
            inf = ru.pidInfo
            self.assertEqual(len(inf), ru.npids)
            for pi in inf:
                for a in ['pid', 'ppid', 'pgid', 'jobid']:
                    self.assertGreaterEqual(getattr(pi, a), -1)
            for g in range(ru.npgids):
                self.assertGreaterEqual(ru.pgid[g], -1)


    def test_init(self):
        self.assertGreaterEqual(lsblib.lsb_init("Test Case"), 0)

    def test_queueinfo(self):
        lsblib.lsb_init("test queues")
        queues = lsblib.lsb_queueinfo()
        self.assertIsInstance(queues, list)
        for queue in queues:
            self.check_queue(queue)

    def test_hostinfo(self):
        hosts = lsblib.lsb_hostinfo()
        self.assertIsInstance(hosts, list)
        for host in hosts:
            self.check_host(host)

    def check_queue(self, queue):
        self.assertIsInstance(queue.queue, basestring)
        self.assertNotEqual(queue.queue, "")
        self.assertIsInstance(queue.description, basestring)
        self.assertIsInstance(queue.priority, int)
        self.assertIsInstance(queue.nice, int)
        self.assertIsInstance(queue.userList, list)
        for user in queue.userList:
            self.assertIsInstance(user, basestring)
            self.assertNotEqual(user, "")
        self.assertIsInstance(queue.hostList, list)
        for host in queue.hostList:
            self.assertIsInstance(host, basestring)
            self.assertNotEqual(host, "")

        self.assertIsInstance(queue.nIdx, int)
        self.assertGreaterEqual(queue.nIdx, 0)
        self.assertEqual(queue.nIdx, len(queue.loadSched))
        self.assertEqual(queue.nIdx, len(queue.loadStop))
        self.assertIsInstance(queue.userJobLimit, int)
        self.assertIsInstance(queue.procJobLimit, float)
        self.assertIsInstance(queue.windows, basestring)
        self.assertIsInstance(queue.rLimits, list)
        self.assertEqual(len(queue.rLimits), 11)
        for i in queue.rLimits:
            self.assertIsInstance(i, int)
            self.assertGreaterEqual(i, -1)
        self.assertIsInstance(queue.hostSpec, basestring)
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

    def check_host(self, host):
        self.assertIsInstance(host, lsblib.HostInfoEnt)

    def test_lsbaccts(self):
        lsfdir = find_openlava()

        for fname in ['lsb.acct', 'lsb.events']:
            acct_file = os.path.join(lsfdir, "work", "logdir", fname)
            f = open(acct_file)
            row_num = 0
            while (True):
                rec = lsblib.lsb_geteventrec(f, row_num)
                if rec == None:
                    if lsblib.get_lsberrno() == constants.LSBE_EOF:
                        break
                if lsblib.get_lsberrno() == constants.LSBE_EVENT_FORMAT:
                    print "Bad Row: %s in %s" % (row_num, fname)
                    continue
                self.assertEqual(lsblib.get_lsberrno(), constants.LSBE_NO_ERROR)


class LslibTest(unittest.TestCase):
    def test_clustername(self):
        self.assertTrue(lslib.ls_getclustername())

    def test_mastername(self):
        self.assertTrue(lslib.ls_getmastername())

    def check_resource(self, res):
        self.assertIsInstance(res, lslib.ResItem)
        self.assertIsInstance(res.name, basestring)
        self.assertNotEqual(res.name, "")
        self.assertIsNotNone(res.name)

        self.assertIsInstance(res.des, basestring)

        self.assertIsInstance(res.flags, int)
        self.assertGreaterEqual(res.flags, 0)

        self.assertIsInstance(res.interval, int)
        self.assertGreaterEqual(res.interval, 0)

        self.assertIsInstance(res.valueType, basestring)
        self.assertIn(res.valueType, [u"LS_BOOLEAN", u"LS_NUMERIC", u"LS_STRING", u"LS_EXTERNAL"])

        self.assertIsInstance(res.orderType, basestring)
        self.assertIn(res.orderType, [u"INCR", u"DECR", u"NA"])

    def test_lsinfo(self):
        ls = lslib.ls_info()
        self.assertIsInstance(ls, lslib.LsInfo)
        self.assertIsInstance(ls.nRes, int)
        self.assertGreaterEqual(ls.nRes, 0)
        for res in ls.resTable:
            self.check_resource(res)

        self.assertIsInstance(ls.nTypes, int)
        self.assertGreaterEqual(ls.nTypes, 0)
        for t in ls.hostTypes:
            self.assertIsInstance(t, basestring)
            self.assertIsNotNone(t)
            self.assertNotEqual(t, "")

        self.assertIsInstance(ls.nModels, int)
        self.assertGreaterEqual(ls.nModels, 0)
        for m in ls.hostModels:
            self.assertIsInstance(m, basestring)
            self.assertIsNotNone(m)
            self.assertNotEqual(m, "")
        for a in ls.hostArchs:
            self.assertIsInstance(a, basestring)
            self.assertIsNotNone(a)
            self.assertNotEqual(a, "")
        for r in ls.modelRefs:
            self.assertIsInstance(r, int)
            self.assertIsNotNone(r)
            self.assertGreaterEqual(r, 0)
        for c in ls.cpuFactor:
            self.assertIsInstance(c, float)
            self.assertGreaterEqual(c, 0)
        self.assertIsInstance(ls.numIndx, int)
        self.assertIsInstance(ls.numUsrIndx, int)

    def test_gethostinfo(self):
        hosts = lslib.ls_gethostinfo()
        hinfo = {}
        for host in hosts:
            hinfo[host.hostName] = {}
            self.assertIsInstance(host, lslib.HostInfo)
            self.assertIsInstance(host.hostName, basestring)
            self.assertNotEqual(host.hostName, "")
            self.assertIsNotNone(host.hostName)

            self.assertIsInstance(host.hostType, basestring)
            self.assertNotEqual(host.hostType, "")
            self.assertIsNotNone(host.hostType)
            hinfo[host.hostName]['hostType'] = host.hostType

            self.assertIsInstance(host.hostModel, basestring)
            self.assertIsNotNone(host.hostModel)
            self.assertNotEqual(host.hostModel, "")
            hinfo[host.hostName]['hostModel'] = host.hostModel

            self.assertIsInstance(host.cpuFactor, float)
            self.assertGreaterEqual(host.cpuFactor, 0)
            hinfo[host.hostName]['hostFactor'] = host.cpuFactor

            self.assertIsInstance(host.maxCpus, int)
            self.assertGreaterEqual(host.maxCpus, 0)

            self.assertIsInstance(host.maxMem, int)
            self.assertGreaterEqual(host.maxMem, 0)

            self.assertIsInstance(host.maxSwap, int)
            self.assertGreaterEqual(host.maxSwap, 0)

            self.assertIsInstance(host.maxTmp, int)
            self.assertGreaterEqual(host.maxTmp, 0)

            self.assertIsInstance(host.nDisks, int)
            self.assertGreaterEqual(host.nDisks, 0)

            self.assertIsInstance(host.nRes, int)
            self.assertGreaterEqual(host.nRes, 0)

            for resource in host.resources:
                self.assertIsInstance(resource, basestring)
            self.assertIsInstance(host.windows, basestring)
            self.assertNotEqual(host.windows, "")
            self.assertIsNotNone(host.windows)

            for load in host.busyThreshold:
                self.assertIsInstance(load, float)

            self.assertIsInstance(host.isServer, bool)
            self.assertIsInstance(host.rexPriority, int)
        for h, v in hinfo.items():
            #self.assertEqual(v['hostFactor'], ls_gethostfactor(h))
            self.assertEqual(v['hostType'], lslib.ls_gethosttype(h))
            self.assertEqual(v['hostModel'], lslib.ls_gethostmodel(h))


suite = unittest.TestSuite()
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LsblibTest))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(LslibTest))

if __name__ == '__main__':
    unittest.main()
