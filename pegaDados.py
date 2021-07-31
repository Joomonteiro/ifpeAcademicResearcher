from urllib.parse import uses_relative
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
import unidecode
import gspread

def ColetaDadosDoBancoEMandaProGCollector(resultado):
    gc = gspread.service_account(filename='dados-321419-a81530f4cdfb.json')
    sh = gc.open_by_key("18hwGKfZFYT6yy1PCguuBdDYdFWtFIDzNQNa9OGKEmaY") # or by sheet name: gc.open("TestList")
    worksheet = sh.sheet1

    res = worksheet.get_all_records() # list of dictionaries
    res = worksheet.get_all_values() # list of lists

    def transformaemminusculosemacentoeespaco(original):
        processamento_1 = unidecode.unidecode(original)
    
        processamento_2 = processamento_1.replace(" ", "")
    
        processamento_3 = processamento_2.lower()
    
        return processamento_3
    
    autorinput1 = resultado
    autorinput = transformaemminusculosemacentoeespaco(autorinput1)
    ##print(autorinput)

    es = Elasticsearch(['localhost'],
                       scheme="http",
                       port=9200)
    statsPage = []
    doc = {
    'size': 10000,
    'query': {
        'match_all': {}
    }
}
    try:
        res = es.search(index=autorinput, body=doc, scroll='1m')
      

    except:
        ##print("não há dados para este docente")
        exit()
    contaartigo=0

    areas = []

    def contaIndex(res):
        contaartigodehits=0
        for hit in res['hits']['hits']:
            autor_n = hit['_source']['autor']
            contaartigodehits+=1            
        return contaartigodehits,autor_n


    contaartigodehits, autor_n = contaIndex(res)

    def verificaSeJaEstaPresenteNoGoogle(autor_n):
        listaDeTitulos = []
        try:
            cell = worksheet.find(autor_n)
            cell_list = worksheet.findall(autor_n)
            tamanhoLista=len(cell_list)
            value = cell.value
    # ##print(cell_list)
            ##print("quantidade de produções já no google: "+str(tamanhoLista))
        except:
            return False
        if(autor_n==value):
            ##print("o autor já foi indexado")
            for cell in cell_list:
                row_number = cell.row
                column_number = cell.col
                val = worksheet.cell(row_number, column_number+2).value
                ##print(val)
                listaDeTitulos.append(val)


            if(contaartigodehits==tamanhoLista):
                ##print("e tem a mesma quantidade de produçoes indexadas que no google acadêmico")
                return True
            else:
                return False

    estaNoGoogle=verificaSeJaEstaPresenteNoGoogle(autor_n)
    
    ##print("quantidade de produções já no elastic: "+str(contaartigodehits))
    for hit in res['hits']['hits']:
        if(estaNoGoogle):
            break
        autor_n = hit['_source']['autor']
        areas_n = hit['_source']['areas']
        titulo_n = hit['_source']['título']
        text1_n = hit['_source']['text1']
        text2_n = hit['_source']['text2']
        citacoes_n = hit['_source']['citações']
        ano_n = hit['_source']['Ano']
        totalcitacoes_n = hit['_source']['totaldecitacoes']
    # id_n = hit['_source']['_id']
    # tipo_n = hit['_source']['_type']
        contaartigo+=1
        #print(contaartigo)
        # #print(len(res))
        try:
            worksheet.find(titulo_n)
            #print("passando pelo try vazio"+worksheet.find(titulo_n).value)
            user = []
            worksheet.append_row(user)
        except:
            try:
                #print("segundo try"+worksheet.find(titulo_n).value)
                if(worksheet.find(titulo_n).value==titulo_n):
                    user = []
                    #print("salvando user vazio de if"+ titulo_n)
                    #print(user)
                    worksheet.append_row(user)
                elif(worksheet.find(titulo_n).value!=titulo_n):
                    user = [autor_n,areas_n,titulo_n,text1_n,text2_n,citacoes_n,ano_n,totalcitacoes_n]
                    #print("salvando user cheio de wlif"+ titulo_n)
                    #print(user)
                    worksheet.append_row(user)
            except:

                user = [autor_n,areas_n,titulo_n,text1_n,text2_n,citacoes_n,ano_n,totalcitacoes_n]
                #print("salvando user cheio de except"+ titulo_n)
                #print(user)
                worksheet.append_row(user)
    # areas = [areas_n]
    
   
    # ##print(value,autor_n)
        
    ##print("o autor "+autorinput1+" possui um total de "+str(contaartigodehits)+" artigos indexados")

# ColetaDadosDoBancoEMandaProGCollector("tiago brasileiro araujo")