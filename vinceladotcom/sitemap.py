class SitemapEntry(dict):
    def __init__(self, *args, **kwargs):
        super(SitemapEntry, self).__init__(*args, **kwargs)
        
    def to_string(self, site_url):
        ret = ''
        ret += '<url>\n'
        
        for k, v in self.items():
            if k == 'loc':
                v = site_url + v
            
            ret += '\t<{key}>{val}</{key}>\n'.format(
                key=k, val=v)
            
        ret += '</url>\n'
        return ret