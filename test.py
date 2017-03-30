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

        all_html += html.format(proto=html_proto, values=html_values, id=str(id))
    return all_html


d = {'a':[1,2,2,2], 'e':[123], 'c':[1], 'd':[0]}
for x,y in d.items():
	print x,y
c=[[0,0,0,1,2] ,d]

print c[1]
