# -*- coding: utf-8 -*-
import ambry.bundle


class Bundle(ambry.bundle.Bundle):
    pass



    def foo(self):
        from csv import DictWriter
        
        s = self.source('sources')
        
        by_name = {}
        by_domain = {}
        
        
        for row in s.datafile.reader:
            row = dict(row.items())

            row['parent_name'] = row['parent_name'].strip()
            by_name[row['name']] = row
            by_domain[row['domain']] = row
            
        
        row = {
            'id': 999,
            'home_page': 'http://www.ca.gov',
            'name': "State of California",
            'domain': 'ca.gov',
            'parent_name': None
        }
        
        by_name[row['name']] = row
        by_domain[row['domain']] = row
        
        from collections import defaultdict
        by_parent = defaultdict(list)
        
        for k, v in by_name.items():
            
            if 'ca.gov' in v['domain'] and not v.get('parent_name'):
                v['parent_name'] = "State of California"
            
            if v.get('parent_name'):
                parent_name = v['parent_name']
                parts = parent_name.split('(')
                domain = parts.pop().strip(')')
                parent = by_domain.get(domain)
                
                if parent:
                    v['parent_id'] = parent['id']
                    v['parent_domain'] = parent['domain']
                    
                    by_parent[v['parent_domain']].append(v)
        
                 
        
                     

        headers = [ u'id', u'domain', u'name', u'home_page',  u'categories',
                    u'parent_name', 'parent_id','parent_domain']
                    
        from sys import stdout
        
        
        with open('foo.csv', 'w') as f:
            w = DictWriter(f, headers)
            w.writeheader()
        
        
            def rp(level, s):
                print ('    '*level), s['name'], s['domain']
                w.writerow(s)
            
                for child in sorted(by_parent.get(s['domain'], [])):
                    rp(level+1, child)
        
            for k, v in by_name.items():
                if v.get('parent_id'):
                    continue
                
                rp(0,v)