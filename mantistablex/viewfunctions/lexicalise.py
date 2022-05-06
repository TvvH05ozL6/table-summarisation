
import subprocess
import pandas as pd
from django.shortcuts import get_object_or_404
from ..models import Tables, Table_Datas, Table_Annotations, GlobalStatusEnum, GoldStandardsEnum, OcularMovement
from pathlib import Path
from .lamapi import LamAPIWrapper

def getAnn(cta, index):
    for t in cta:
        if t[1] == index:
            if t[2].startswith("http"):
                t[2] = t[2][28:].replace("/","")
            return t[2]
    return

def getPredColIndex(cpa, pred):
    for t in cpa:
        if t[3] == pred:
            return int(t[2])
    return

def doLexicalisation(request, table_id):
    table = get_object_or_404(Tables, id=table_id)
    annotations = request.session.get('annotations')
    table_data_bootstrap = request.session.get('table_datas_bootstrap')
    table_header_bootstrap = request.session.get('table_header_bootstrap')
    familiarity = request.session.get('familiarity')
    interest = request.session.get('interest')
    triples = request.session.get('triples')
    header = ""
    if interest=="0" and familiarity=="0":
        header = table_header_bootstrap[1].lower()
    else:
        num = len(table_header_bootstrap)
        for t,j in enumerate(table_header_bootstrap):
            if t>0:
                header = header+j.lower()
                if t<num-1:
                    header = header+", "

    #print(table_data_bootstrap)
    #print(table_header_bootstrap)
    idsubj = int(annotations["CPA"][0][1])
    domainorig = annotations["CTA"][idsubj][2][28:]
    domain = domainorig.lower()
    numeric = ["xsd:double", "xsd:integer", "xsd:float"]
    dates = ["xsd:gYear", "xsd:date", "xsd:dateTime"]
    min = {}
    max = {}
    avg = {}
    df = pd.DataFrame(table_data_bootstrap)
    df.columns= df.columns.str.lower()
    sum = "There are "
    #print(df)
    first = True
    for t in annotations["CTA"]:
        index = table_header_bootstrap[int(t[1])].lower()
        if(t[2] in numeric):
            df[index] = df[index].apply(lambda x: x.replace(',', '.'))
            df[index] = pd.to_numeric(df[index], errors='coerce')
            min[index] = {"type": "num","val":df.iloc[df[index].idxmin()]}
            max[index] = {"type": "num","val":df.iloc[df[index].idxmax()]}
            avg[index] = df[index].mean()
        elif(t[2] in dates):
            df[index] = pd.to_datetime(df[index], errors='coerce')
            min[index] = {"type": "date","val":df.iloc[df[index].idxmin()]}
            max[index] = {"type": "date","val":df.iloc[df[index].idxmax()]}
            if t[2]!= "xsd:dateTime":
                #convert datetime to date
                min[index]["val"][index] = min[index]["val"][index].date()
                max[index]["val"][index] = max[index]["val"][index].date()
        else:
            if first==True:
                first=False
                continue
            uc = df[index].unique()
            uv = df[index].value_counts()
            if(len(uc)==1):
                sum = "There is "
            print(t[2])
            sum += str(len(uc))+" "+index+": "
            for k,v in enumerate(uv):
                sum+=uc[k].replace(","," -")+" ("+str(v)+" "+domain+")"
                if k==3:
                    sum+= " and "+str(len(uv)-4) + " more"
                    break
                if k<len(uv)-2 and k<3:
                    sum+=", "
                elif k<len(uv)-1:
                    sum+=" and "
                    
            sum+=". <br>"
    
    minstr=f"The { domain } with "
    maxstr=f" while the { domain } with "
    entered = False
    addmin = "the minimum"
    addmax = "the maximum"
    for j in min:
        if min[j]["type"] == "date":
            addmin = "the first"
            addmax = "the last"
        if entered==False:
            minstr+=f" {addmin} { j } is { min[j]['val'][table_header_bootstrap[idsubj].lower()] } with a value of { min[j]['val'][j] }"
            maxstr+=f" {addmax} { j } is { max[j]['val'][table_header_bootstrap[idsubj].lower()] } with a value of { max[j]['val'][j] }"
            if interest=="0" and familiarity=="0":
                break
            entered=True
        else:
            minstr+=f", {addmin} {j} is { min[j]['val'][j] } of { min[j]['val'][table_header_bootstrap[idsubj].lower()] }"
            maxstr+=f", {addmax} {j} is { max[j]['val'][j] } of { max[j]['val'][table_header_bootstrap[idsubj].lower()] }"
    minstr+=";"
    maxstr+="."
    if len(min)==0:
        minstr=""
        maxstr=""
    context = {
        'table': table,
        'table_datas_bootstrap': table_data_bootstrap,
        'table_header_bootstrap': table_header_bootstrap,
        'rows': len(table_data_bootstrap),
        'cols': len(table_data_bootstrap[0]),
        'predictions': [],
        'familiarity': familiarity,
        'interest': interest,
        'header': header,
        'min': minstr,
        'max': maxstr,
        'avg': avg,
        'domain': domain,
        'text': "",
        'triples': triples,
        'sum': sum
    }
    
    table = str(table)
    c = []
    for t in annotations["CPA"]:
        tmp = getAnn(annotations["CTA"], t[1])
        tmp2 = getAnn(annotations["CTA"], t[2])
        if t[3].startswith("http"):
            t[3] = t[3][28:].replace("/","")
        c.append(tmp+" "+t[3]+" "+tmp2)
    cstr = "\n". join(c)
    input = "NMTmodel/predictions/"+table
    output = "NMTmodel/predictions/"+table+"/out.txt"
    Path(input).mkdir(parents=True, exist_ok=True)
    input = input+"/test.txt"
    file = open(input, "w+")
    file.write(cstr)
    file.close()
    cmd = "onmt_translate -model NMTmodel/run/model_step_1000.pt -src "+input+" -output "+output
    o = subprocess.run(cmd, check=True, text=True, shell=True)
    #print(o.stdout)
    print(o.stderr)
    f = open(output, 'r')
    context["predictions"] = f.readlines()
    rng = 3
    if familiarity=="1" and interest=="0":
        rng=1
    triple = ""
    for j in range(rng):
        first = False
        replaceS = False
        for i,p in enumerate(context["predictions"]):
            if isinstance(c[i], str):
                c[i] = c[i].split(" ")
            row = df.loc[j]
            out = ", "
            subj = str(row[df.columns[idsubj]])
            colindex = getPredColIndex(annotations["CPA"], c[i][1])
            if i==len(context["predictions"])-1:
                out=" and "
                if p.index("<")>2:
                    out = str(row[df.columns[idsubj]])
                    context["text"]+=". "
            if first == False:
                out=str(row[df.columns[idsubj]])
                first= True
            data = row[table_header_bootstrap[colindex].lower()]
            annot = annotations["CTA"][colindex][2]
            if annot in dates:
                if annot == "xsd:date":
                    data = data.date()
                if annot == "xsd:gYear":
                    data = data.date().year
            tstr = p.replace("<"+c[i][0]+">", out, 1).replace("<"+c[i][2]+">", str(data).replace(","," -"), 1)
            if replaceS==True:
                tstr = tstr.replace("'s","")
            if replaceS==False:
                replaceS = True
            triple += "["+subj+"] "+c[i][1]+" ["+str(data)+"]"
            context["text"]+=tstr.replace("\n","")
            if interest=="0" and familiarity=="0":
                break
            triple+=" - "
        context["text"]+=".<br>"
        triple=triple[:-3]
        triple+="<br>"
    
    if familiarity=="0" and interest=="1":
        try:
            lamapi = LamAPIWrapper("149.132.176.84", 8097)
            r = lamapi.sameAs([domainorig])
            wd = r["dbpedia"][domainorig]
            desc = lamapi.labels([wd])["wikidata"][wd]["description"]
            context["domainSpec"] = " ("+desc+")"
        except:
            context["domainSpec"] = ""
    context["triple"] = triple
    return context