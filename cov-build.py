import tkinter as tk
import tkinter.filedialog as filedialog
import subprocess
import os
import shutil
from enum import Enum
import webbrowser
import threading
from queue import Queue
import time

class Row(Enum):
    PROJECT = 0
    BUILDTOOL = 1
    COV = 2
    BUILD = 3
    COVBUILD = 4
    OUTPUT = 5
    XSCROLL = 6


class Column(Enum):
    BTN = 0
    LABEL = 1
    YSCROLL = 2


class AsynchronousFileReader(threading.Thread):
    def __init__(self, fd, queue):
        assert isinstance(queue, Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        time.sleep(.5)
        try:
            for line in iter(self._fd.readline, b''):
                if line != b'':
                    self._queue.put(line)
        except StopIteration:
            print('StopIteration')

    @property
    def eof(self):
        return (not self.is_alive()) and self._queue.empty()


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.__build_cmd = None #default
        self.__cov_cmd_dir = None #default
        self.__create_widgets()

    def __clear_output(self):
        self.__lbOutput.delete(0, self.__lbOutput.size() - 1)

    def __choose_build_tool_dialog(self):
        self.__build_cmd = filedialog.askopenfilename()
        if self.__build_cmd:
            self.__lbl_build_cmd['text']=self.__build_cmd
            pass

    def __choose_coverity_dialog(self):
        self.__cov_cmd_dir = filedialog.askdirectory()
        if self.__cov_cmd_dir:
            self.__lblCov['text']=self.__cov_cmd_dir
            pass


    def __run_cmd(self, cmd, wd=None):
        cwd = os.getcwd()
        if wd:
            os.chdir(wd)
        try:
            return subprocess.check_call(cmd)
        except (KeyboardInterrupt, subprocess.CalledProcessError) as e:
            self.__lbOutput.insert(tk.END, 'ERROR!')
            return -1
        if wd:
            os.chdir(cwd)


    def __run_cmd_redirected(self, cmd, wd=None):
        cwd = os.getcwd()
        if wd:
            os.chdir(wd)
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, shell=True)

            # Launch the asynchronous readers of the process' stdout and stderr.
            stdout_queue = Queue()
            stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
            stdout_reader.start()
            stderr_queue = Queue()
            stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
            stderr_reader.start()

            # Check the queues if we received some output (until there is nothing more to get).
            while not stdout_reader.eof or not stderr_reader.eof:
                # Show what we received from standard output.
                while not stdout_queue.empty():
                    #if self.__lbOutput.size() > 9999:
                    #    self.__clear_output()
                    self.__lbOutput.insert(tk.END, stdout_queue.get())

                # Show what we received from standard error.
                #for line in iter(stderr_queue.get, None):
                #    print(str(line))

                # Sleep a bit before asking the readers again.
                time.sleep(.5)

            # Let's be tidy and join the threads we've started.
            stdout_reader.join()
            stderr_reader.join()

            # Close subprocess' file descriptors.
            process.stdout.close()
            process.stderr.close()
        except (KeyboardInterrupt, subprocess.CalledProcessError) as e:
            self.__lbOutput.insert(tk.END, 'ERROR!')
            return -1
        if wd:
            os.chdir(cwd)

    def __build(self):
        if not self.__build_cmd:
            self.__clear_output()
            self.__lbOutput.insert(tk.END, 'Invailid build command')
        else:
            cmd = [os.path.basename(self.__build_cmd), self.__proj]
            self.__run_cmd(cmd, os.chdir(os.path.dirname(self.__build_cmd)))

    def __cov_build(self):
        if not self.__cov_cmd_dir:
            self.__clear_output()
            self.__lbOutput.insert(tk.END, 'Invailid cov command')
        else:
            cov_dir = os.path.dirname(self.__proj) + os.sep + 'Debug' + os.sep + 'cov'
            shutil.rmtree(cov_dir, ignore_errors=True)
            os.makedirs(cov_dir)
            cmd = [self.__cov_cmd_dir + os.sep + 'cov-build','--dir', cov_dir, os.path.basename(self.__build_cmd), self.__proj]
            self.__lbOutput.insert(tk.END, '------------------------------cov-build in progress------------------------------')
            self.__run_cmd(cmd, os.path.dirname(self.__build_cmd))
            self.__lbOutput.insert(tk.END, '------------------------------cov-build done------------------------------')
            self.__lbOutput.insert(tk.END, '------------------------------cov-analyze in progress------------------------------')

            cmd = [self.__cov_cmd_dir + os.sep + 'cov-analyze', '--dir', cov_dir,
                   '--enable-constraint-fpp', '--enable-callgraph-metrics', '-j','2']
            self.__run_cmd(cmd)
            self.__lbOutput.insert(tk.END, '------------------------------cov-analyze done------------------------------')
            self.__lbOutput.insert(tk.END, '------------------------------cov-format-errors in progress------------------------------')
            cmd = [self.__cov_cmd_dir + os.sep + 'cov-format-errors', '--dir', cov_dir]
            self.__run_cmd(cmd)
            self.__lbOutput.insert(tk.END, '------------------------------cov-format-errors done------------------------------')
            webbrowser.open(cov_dir + os.sep + 'output\\errors\\index.html')

    def __choose_project(self):
        self.__proj = filedialog.askopenfilename()
        if self.__proj:
            self.__lblProj['text'] = self.__proj

    def __create_widgets(self):
        self.pack(fill=tk.BOTH, expand=1)

        self.__btnProj = tk.Button(self, text='Project')
        self.__btnProj.grid(row=Row.PROJECT.value, column=Column.BTN.value, sticky=tk.W)
        self.__btnProj['command'] = self.__choose_project
        self.__lblProj = tk.Label(self)
        self.__lblProj.grid(row=Row.PROJECT.value, column=Column.LABEL.value, sticky=tk.W)
        
        self.__btn_build_cmd = tk.Button(self, text = 'BuildCmd')
        self.__btn_build_cmd.grid(row=Row.BUILDTOOL.value, column=Column.BTN.value, sticky=tk.W)
        self.__btn_build_cmd['command'] = self.__choose_build_tool_dialog
        self.__lbl_build_cmd = tk.Label(self)
        self.__lbl_build_cmd['text'] = 'Select Build command'
        self.__lbl_build_cmd.grid(row=Row.BUILDTOOL.value, column=Column.LABEL.value, sticky=tk.W)

        self.__btnCov = tk.Button(self, text='coverity')
        self.__btnCov.grid(row=Row.COV.value, column=Column.BTN.value, sticky=tk.W)
        self.__btnCov['command'] = self.__choose_coverity_dialog
        self.__lblCov = tk.Label(self)
        self.__lblCov['text'] = 'Select coverity BIN directory'
        self.__lblCov.grid(row=Row.COV.value, column=Column.LABEL.value, sticky=tk.W)

        self.__btnBuild = tk.Button(self, text='Build')
        self.__btnBuild['command'] = self.__build
        self.__btnBuild.grid(row=Row.BUILD.value, column=Column.BTN.value, sticky=tk.W)

        self.__btnCovBuild = tk.Button(self, text='CovBuild')
        self.__btnCovBuild['command'] = self.__cov_build
        self.__btnCovBuild.grid(row=Row.COVBUILD.value, column=Column.BTN.value, sticky=tk.W)

        self.__xscrollBar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.__xscrollBar.grid(row=Row.XSCROLL.value, column=Column.BTN.value, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)
        self.__yscrollBar = tk.Scrollbar(self)
        self.__yscrollBar.grid(row=Row.OUTPUT.value, column=Column.YSCROLL.value, sticky=tk.W+tk.E+tk.N+tk.S)
        
        self.__lbOutput = tk.Text(self, yscrollcommand = self.__yscrollBar.set, xscrollcommand = self.__xscrollBar.set)
        self.__lbOutput['width'] = 140
        self.__lbOutput['height'] = 20
        self.__lbOutput.config(state='disabled')
        self.__lbOutput.grid(row=Row.OUTPUT.value, column=Column.BTN.value, columnspan=2)
        self.__yscrollBar.config(command = self.__lbOutput.yview)
        self.__xscrollBar.config(command = self.__lbOutput.xview)


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
