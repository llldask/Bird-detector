class NotExistPathError(BaseException):
    pass
  
class FileExist(BaseException):
    pass

class StreamUrlError(BaseException):
    pass

class VideoDownloadError(BaseException):
    pass

class VideoProcessingError(BaseException):
    pass