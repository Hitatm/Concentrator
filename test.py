# -*- coding: utf-8 -*-
# @Author: Guoxuenan
# @Date:   2016-11-14 23:01:33
# @Last Modified by:   Guoxuenan
# @Last Modified time: 2016-11-17 22:56:40
Dict= {"a" : "apple", "b" : "banana", "g" : "grape", "o" : "orange"}

def showdata_from_id(Dict):
    html = '''
            <div class="accordion-group">
                <div class="accordion-heading">
                    <b><a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion" href="#collapse{id}">
                        {proto}
                    </a></b><br>
                    </div>
                    <div id="collapse{id}" class="accordion-body collapse" style="height: 0px; ">
                    <div class="accordion-inner">
                        {values}
                    </div>
                </div>
            </div>
'''
    all_html = ''
    id = 0
    for proto, value in Dict.items() :
        id += 1
        html_proto =  proto
        html_values = value
        # values = value.strip().split('\n')
        # for v in values:
        #     val = v.split('  =')
        #     if len(val) == 2:
        #         html_values += '<b>{0} = {1}</b><br>'.format(val[0].strip(), val[1].strip())
        #     elif len(val) == 1:
        #         html_values += '<b>{0} = {1}</b><br>'.format('options', 'None')
        all_html += html.format(proto=html_proto, values=html_values, id=str(id))
    return all_html

# print showdata_from_id(Dict)


# print hex(2225)[2:].lower()
# print "ASEDFaE".lower()
d = {'a':[1,2,2,2], 'e':[123], 'c':[1], 'd':[0]}
for x,y in d.items():
	print x,y
c=[[0,0,0,1,2] ,d]
# c['a'][0]+=4
# c['a'][0]+=2
print c[1]
# c[1]=1090
# print 