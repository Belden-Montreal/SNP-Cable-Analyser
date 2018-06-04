import threading

class TabThread(threading.Thread):
    def __init__(self, tid, sample, param):
        threading.Thread.__init__(self)
        self.sample = sample
        self.param = param
        self.tid = tid
        self.worstValue = None
        self.worstMargin = None

    def run(self):
        if self.sample.standard and self.param in self.sample.standard.limits:
            #try:
            self.worstMargin = self.sample.getWorstMargin(self.param)
            self.worstValue = self.sample.getWorstValue(self.param)
            # except:
            #     self.worstMargin = None
            #     self.worstValue = None
    
    def join(self):
        threading.Thread.join(self)
        return (self.worstValue, self.worstMargin)