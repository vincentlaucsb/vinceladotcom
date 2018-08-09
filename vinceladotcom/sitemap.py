class Sitemap(object):
    ''' Sitemap generator '''
    
    def __init__(self, url_root):
        ''' url_root: A string that gets prepended to every (relative) URL in self.entries '''
        super(Sitemap, self).__init__()
        self.entries = []
        self.url_root = url_root
    
    def add(self, entry):
        ''' Add a sitemap entry '''
        self.entries.append(entry)
    
    def __str__(self):
        ''' Generate an XML string '''
        entries = ''
        
        for i in self.entries:
            entries += i.to_string(self.url_root)
            
        return entries

class SitemapEntry(dict):
    ''' Used for storing the XML keys and attributes for each unique URL '''
    
    def __init__(self, *args, **kwargs):
        super(SitemapEntry, self).__init__(*args, **kwargs)
        
    def to_string(self, site_url: str):
        ret = ''
        ret += '\t<url>\n'
        
        for k, v in self.items():
            if k == 'loc':
                if (v[0] == '/'): # Strip out leading /
                    v = v[1:]
                v = site_url + v
            
            ret += '\t\t<{key}>{val}</{key}>\n'.format(
                key=k, val=v)
            
        ret += '\t</url>\n'
        return ret