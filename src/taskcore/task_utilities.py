import json
from subprocess import *
from paramiko import SSHClient
import pprint
import operator
import collections


class JobExecuter(object):
    def __init__(self, cmd_arg):
        b_str = " "
        if isinstance(cmd_arg, str):
            self.cmd = cmd_arg
        if isinstance(cmd_arg, list):
            if len(cmd_arg) == 1:
                self.cmd = cmd_arg
            if len(cmd_arg) == 2:
                self.cmd = b_str.join(cmd_arg)
            if len(cmd_arg) == 3:
                self.cmd = b_str.join(cmd_arg[0:1])
                self.usernamev = cmd_arg[2]
                self.passwordv = None
            if len(cmd_arg) >= 4:
                self.cmd = b_str.join(cmd_arg[0:1])
                self.usernamev = cmd_arg[2]
                self.passwordv = cmd_arg[3]

    def run(self):
        # if it is a script, CMD should be Path + CMD
        try:
            p = Popen(self.cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = p.communicate(timeout=90)
            return stdout.decode(), stderr.decode()
        except TimeoutExpired:
            p.kill()
            # stdout, stderr = p.communicate()
            return stderr('Got subprocess.TimeoutExpired for command:', self.cmd)
            # return stdout.decode(), stderr.decode()

    def remote_run(self):
        try:
            client = SSHClient()
            client.load_system_host_keys()
            if self.passwordv != None:
                client.connect(self.hostname, username=self.usernamev, password=self.passwordv)
            else:
                client.connect(self.hostname, username=self.usernamev)
            stdin, stdout, stderr = client.exec_command(self.cmd, timeout=90)
            return stdout.readlines(), stderr.readlines()
        except TimeoutExpired:
            client.close()
            # print('Got TimeoutExpired for:', self.cmd)
            return stderr('Got TimeoutExpired for:', self.cmd)


class TaskBuilder(object):

    def __init__(self, t_json):
        if not isinstance(t_json, dict):
            f = open(t_json)
            d = json.load(f)
            self.tasks_d = d['tasks']
        else:
            # if it is dict object provided by web UI, just use the dict directly
            self.tasks_d = t_json

    def __job_execute(self, job):
        # execute the job on the server by using the current user:
        result = JobExecuter(job).run()
        # print(result)
        if (len(result) == 1):
            return 1, result
        elif len(result[1]) != 0:
            return 1, result
        else:
            return 0, result

    def __stage_execute(self, stage):
        # On the failure of any job within a stage, an error should be logged and any
        # further jobs in the stage should be skipped.
        s_jobd = collections.OrderedDict(sorted(stage.items()))
        result_l = []
        for k, v in s_jobd.items():
            print(v)
            res = self.__job_execute(v)
            job_status_code = res[0]
            if (job_status_code == 1):
                cmd_string = ("failed to execute" + str(v))
                strn = '\n'
                error_string = ("failed result:" + str(res[1]))
                error_log = cmd_string + strn + error_string
                # print(error_log)
                result_l.append(error_log)
                break
            else:
                cmd_string = ('successfull executed:' + str(v))
                strn = '\n'
                r_string = ('successfull result:' + str(res[1]))
                result_log = cmd_string + strn + r_string
                # print(result_log)
                result_l.append(result_log)
                continue
        return result_l

    def execute(self):
        task_r = []
        taskd = self.tasks_d
        s_taskd = collections.OrderedDict(sorted(taskd.items()))
        for k, v in s_taskd.items():
            # print(v)
            r = self.__stage_execute(v)
            task_r.append(r)
        return task_r
