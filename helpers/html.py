from helpers.postgresql import *

def dropdown(query,name,label):

    select_dropdown = fetchall(query)

    isi_select_dropdown = ''
    for i in select_dropdown:
        isi_select_dropdown += '<option value="'+str(i['id'])+'" >'+i['name']+'</option>' 
    select_select_dropdown = """
        <div class="form-group">
            <label for="{name}">{label}</label>
            <select class="form-control" id="{name}" name="{name}" >
                {isi_select_dropdown}
            </select>
        </div>
    """.format(isi_select_dropdown=isi_select_dropdown,name=name,label=label)


    return select_select_dropdown
