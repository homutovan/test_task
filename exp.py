import pychrome
from pprint import pprint

url = 'https://online.sbis.ru/auth/?ret=%252Fauth'

target = [
            ('auth-MainTabs__buttonCaption', 2),
            ('demo-Auth__item documents', 0),
            ('edo3-Browser-Main__header1-text edo3-Browser__text-ellipsis', 0)
        ]

# target = [
#             ('auth-MainTabs__buttonCaption', 1),
#             ('auth-MainTabs__buttonCaption', 2),
#             ('auth-MainTabs__buttonCaption', 0),
#             ('auth-MainTabs__buttonCaption', 1),
#             ('auth-MainTabs__buttonCaption', 2),
#             ('auth-MainTabs__buttonCaption', 0),
#             ('auth-MainTabs__buttonCaption', 1),
#             ('auth-MainTabs__buttonCaption', 2),
#             ('auth-MainTabs__buttonCaption', 0),
#             ('auth-MainTabs__buttonCaption', 1),
#             ('auth-MainTabs__buttonCaption', 2),
#             ('auth-MainTabs__buttonCaption', 0)
#         ]

class EventHandler:

    def __init__(self, browser, tab):
        self.browser = browser
        self.tab = tab
        self.start = 0
        self.stop = 0
        self.all_metrics = []
        self.duration = []
            
    def request(self, **kwargs):
        if not self.start:
            self.start = kwargs.get('timestamp')
            
    def response(self, **kwargs):
        self.stop = kwargs.get('timestamp')
            
    def click(self, CSS_class, number):
        if not self.duration:
            self.slice_duration()
        self.tab.Runtime.evaluate(expression = f'document.getElementsByClassName("{CSS_class}")[{number}].click()')
        self.tab.wait(10)
        self.slice_duration()
    
    def slice_duration(self):
        self.duration.append(self.stop - self.start)
        self.start = 0
        self.stop = 0
        
    def add_metrics(self):
        raw_metrics = self.tab.Performance.getMetrics()['metrics']
        metrics = {metric['name']: metric['value'] for metric in raw_metrics if metric['value']}
        self.all_metrics.append(metrics)
        
    def get_metrics(self):
        for i, metric in enumerate(self.all_metrics):
            metric = 0
            
        return self.all_metrics
            
def case1():
    pass
    
def case2():
    browser = pychrome.Browser()
    tab = browser.new_tab()
    eh = EventHandler(browser, tab)
    
    tab.Network.clearBrowserCache()
    tab.Network.requestWillBeSent = eh.request
    tab.Network.responseReceived = eh.response
    
    tab.start()
    
    tab.Network.enable()
    tab.Performance.enable()
    tab.Page.enable()
    
    tab.Page.stopLoading()
    tab.Page.navigate(url = url)
    tab.wait(5)
    
    for CSS_class, number in target:
        print(CSS_class, number)
        eh.click(CSS_class, number)
        #tab.Page.enable()
        #eh.add_metrics()
        #tab.Page.disable()
    #pprint(eh.all_metrics)
    #eh.get_metrics()
    tab.stop()
    print(f'время открытия карточки документа {eh.duration[-1]}')
    #browser.close_tab(tab.id)

if __name__ == '__main__':
    case2()
    
