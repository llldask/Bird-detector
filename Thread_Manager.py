class thread_manager:
    def __init__(self):
        self.thread_list=[False,False,False]
    def start(self,id):
        self.thread_list[id]=True
    def stop(self,id):
        self.thread_list[id]=False