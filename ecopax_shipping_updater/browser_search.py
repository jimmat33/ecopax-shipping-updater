'''
module docstr
'''

from abc import ABC, abstractmethod
# pylint: disable=W0107


class BrowserSearch(ABC):
    '''
    docstr
    '''
    @abstractmethod
    def get_options(self, options):
        '''
        docstr
        '''
        pass

    @abstractmethod
    def connect(self, driver):
        '''
        docstr
        '''
        pass

    @abstractmethod
    def pull_date(self, driver, i):
        '''
        docstr
        '''
        pass

    @abstractmethod
    def modify_search(self, driver, i):
        '''
        docstr
        '''
        pass

    @abstractmethod
    def search_algorithm(self):
        '''
        docstr
        '''
        pass
