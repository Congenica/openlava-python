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

from libc.stdio cimport *
from lstypes cimport *
from lsstructs cimport *

cdef extern from "lsbatch.h":
    extern void           lsb_closejobinfo()
    extern int            lsb_deletejob (LS_LONG_INT jobId, int times, int options)
    extern eventRec *     lsb_geteventrec(FILE * log_fp, int * lineNum)
    extern int            lsb_hostcontrol(char *host, int opCode)
    extern hostInfoEnt *  lsb_hostinfo(char **hosts, int *numHosts)
    extern int            lsb_init (char *appName)
    extern LS_LONG_INT    lsb_modify (submit *, submitReply *, LS_LONG_INT)
    extern int            lsb_openjobinfo (long, char *, char *, char *, char *,int)
    extern jobInfoHead *  lsb_openjobinfo_a(long, char *, char *, char *, char *, int)
    extern char *         lsb_peekjob(unsigned long jobId)
    extern char *         lsb_pendreason (int numReasons, int *rsTb, jobInfoHead *jInfoH, loadIndexLog *ld)
    extern void           lsb_perror(char *)
    extern int            lsb_queuecontrol(char *queue, int opCode)
    extern queueInfoEnt * lsb_queueinfo (char **queues, int *numQueues, char *host, char *userName, int options)
    extern jobInfoEnt *   lsb_readjobinfo( int * )
    extern int            lsb_requeuejob(jobrequeue * reqPtr)
    extern int            lsb_reconfig(int)
    extern int            lsb_signaljob (LS_LONG_INT jobId, int sigValue)
    extern LS_LONG_INT    lsb_submit ( submit * subPtr, submitReply * repPtr)
    extern char *         lsb_sysmsg()
    extern userInfoEnt *  lsb_userinfo(char **users, int *numUsers)
    extern char *         lsb_suspreason (int, int, loadIndexLog *)

cdef extern from "lsf.h":
    extern clusterInfo *  ls_clusterinfo(char *resreq, int *numclusters, char **clusterlist, int listsize, int options)
    extern char *         ls_getclustername()
    extern float *        ls_gethostfactor(char *hostname)
    extern hostInfo *     ls_gethostinfo(char *resreq, int *numhosts, char **hostlist, int listsize, int options)
    extern char *         ls_gethostmodel(char *hostname)
    extern char *         ls_gethosttype(char *hostname)
    extern char *         ls_getmastername()
    extern lsInfo *       ls_info()
    extern hostLoad *     ls_load(char *resreq, int *numhosts, int options, char *fromhost)
    extern hostLoad *     ls_loadinfo(char *resreq, int *numhosts,int options, char *fromhost, char **hostlist,int listsize, char ***indxnamelist)
    extern void           ls_perror(char *usrMsg)
    extern char *         ls_sysmsg()

