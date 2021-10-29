"""Run shell command, taken from Vitals
"""

from subprocess import Popen, PIPE, TimeoutExpired


def run_command(cmd, timeout=None, raise_on_timeout=True):
    """Run command as child subprocess with optional timeout.

    :param list cmd: list of tokens to be executed, e.g.:
        ['find', '-name', 'file_to_be_found']

    :param float or int timeout: Optional timeout for execution.
        If timeout expires, process is killed and subprocess.TimeoutExpired
        is raised or return code is set to 124, depending on raise_on_timeout
        parameter.

    :param bool raise_on_timeout: whether raise subprocess.TimeoutExpired
        on timeout or return killed process output.

    :returns: tuple (return_status, stdout, stderr)
    """
    assert type(cmd) is list

    if timeout:
        cmd = ['timeout', '--kill', '0.1', str(timeout)] + cmd

    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, universal_newlines=True)

    return_code = None
    stdout, stderr, data_stdout, data_stderr = '', '', '', ''
    while return_code is None or data_stdout or data_stderr:
        data_stdout = proc.stdout.readline().strip()
        if data_stdout:
            stdout += data_stdout + '\n'

        data_stderr = proc.stderr.readline().strip()
        if data_stderr:
            stderr += data_stderr + '\n'

        return_code = proc.poll()

    proc.stdout.close()
    proc.stderr.close()

    if timeout is not None and return_code == 124:
        if raise_on_timeout:
            raise TimeoutExpired(cmd, timeout)
        else:
            print(
                '"{}" timed out after {} seconds.'.format(cmd, timeout)
            )

    return return_code, stdout, stderr
