# -*- coding: utf-8 -*-
# @Author: Guoxuenan
# @Date:   2016-11-14 23:01:33
# @Last Modified by:   Guoxuenan
# @Last Modified time: 2016-11-15 08:54:51
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

print showdata_from_id(Dict)





def showdata_from_id(PCAPS, dataid):
    Dict = topodict[dataid]
    # return str(item)
    #输出重定向数据
    # show_temp_name = tempfile.NamedTemporaryFile(prefix='show_', dir='/tmp')
    # old = sys.stdout
    # show_file = open(show_temp_name.name, 'w')
    # sys.stdout = show_file
    # # pcap.show()
    # sys.stdout = old
    # show_file.close()
    # #读取数据
    # with open(show_temp_name.name, 'r') as showf:
    #     data = showf.read()
    # result = data.strip().split('###')[1:]
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
        html_proto = proto.strip()[1:-1].strip()
        html_values = ''
        values = value.strip().split('\n')
        for v in values:
            val = v.split('  =')
            if len(val) == 2:
                html_values += '<b>{0} = {1}</b><br>'.format(val[0].strip(), val[1].strip())
            elif len(val) == 1:
                html_values += '<b>{0} = {1}</b><br>'.format('options', 'None')
        all_html += html.format(proto=html_proto, values=html_values, id=str(id))
    return all_html