from tracker.models import RequestLogs

class RequestLogin:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_info=request
        print("Request path:",request_info.path)
        print("Request method:",request_info.method)
        RequestLogs.objects.create(
            request_info=str(request_info),
            request_type=request_info.path,
            request_METHOD=request_info.method
        )
        

        return self.get_response(request)
       
