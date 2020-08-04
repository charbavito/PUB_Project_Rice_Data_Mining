# CATCHER_SRX_3.0 - VERSÃO UTILIZADA
#================================================================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS

from Bio import Entrez
from urllib.request import urlopen
import os, sys

#================================================================================================================
# BUSCA DE DADOS E CRIAÇÃO DA ESTRUTURA DE DIRETÓRIOS COM BASE NAS LISTAS GERADAS COM
# DADOS OBTIDOS DO SRA DATABASE PARA OS ESTUDOS ATRAVÉS DO fetcher_SRP_3.0


os.system('mkdir /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data')

#================================================================================================================
# LISTA DE ESTUDOS

file_access = open('/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/listas/estudos_SRP.txt', 'r')

temp_estudo = list()

for estudo in file_access:
    if estudo == '\n':
        pass
    else:
        temp_estudo.append(estudo)
file_access.close()

aux_x = ''.join(temp_estudo)
estudo = aux_x.split()

print(*estudo, sep='  ')
print(f'Total de estudos para o projeto: {len(estudo)}')
print(50*'-')
print()
#================================================================================================================

#================================================================================================================
# LISTA DE EXPERIMENTOS

for est in estudo:
    file_access = open(f'/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/listas/{est}_SRR_Acc_List.txt', 'r')
    
    os.system(f'mkdir /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}')
    
    temp_exp = list()
    
    for exp in file_access:
        if exp == '\n':
            pass
        else:
            temp_exp.append(exp)
    file_access.close()
    
    aux_x = ''.join(temp_exp)
    experiments = aux_x.split()
    
    print(*experiments, sep='  ')
    print(f'Total de experimentos para o estudo {est}: {len(experiments)}')
    print(50*'-')
    print()

#================================================================================================================

#================================================================================================================
# BUSCA POR CADA EXPERIMENTO NO NCBI/SRA (USA BASICAMENTE O CORE DO fetcher_SRP_3.0)
    
    links_full = list()
    
    for exp in experiments:
        # os.system(f'mkdir /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project_teste/data/{est}/{exp}')
        
        term = exp
        email = 'eubiologo@usp.br'
        ret = 200
        ident = 'acc'
        db = 'sra'

        Entrez.email = email
    
        search = Entrez.esearch(db = db, term = term, idtype = ident, retmax = ret)
    
        data = Entrez.read(search)
    
    
        id_list = list()
    
        # BUSCA DE APENAS UMA CORRIDA POR 'ESTUDO/IDr'
        for pos, e in enumerate(data['IdList']):
            if int(e) == (int(data['IdList'][pos-1])-1):
                pass
            else:
                id_list.append(e)
        
          
#================================================================================================================

#================================================================================================================
# BUSCA PELOS METADADOS DE CADA EXPERIMENTO NO NCBI/SRA

        id_url = ','.join(id_list) ## ??????? não lembro e estou sem cabeça pra pensar nisso agora
    
        data_full = list()
    
        for i in id_list:
            url_mont = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=',db,'&id=',i,'&rettype=fasta&retmode=xml'
            url = ''.join(url_mont)
            page = urlopen(url)
            raw = page.read().decode('utf8')
            
            data = list()
            
            for pos, i in enumerate(raw):
                if i == '<':
                    ini_in = pos
                elif i == '>':
                    end_in = pos
                    data.append(raw[ini_in+1:end_in])
                    ini_in = end_in = 0
                    
                if i == '>':
                    ini_out = pos
                elif i == '<' and pos != 0:
                    end_out = pos
                    data.append(raw[ini_out+1:end_out])
                    ini_out = end_out = 0
            
            for pos, e in enumerate(data):
                if e == '\n' or e == '':
                    data.pop(pos)
        
            data_full.append(data[:])
    

#================================================================================================================

#================================================================================================================
# BUSCA PELOS LINKS DE DOWNLOAD DE CADA EXPERIMENTO

        ## filtragem por https
        https_temp = list()
            
        for i in data_full:
            for pos, e in enumerate(i):
                if 'https://' in e:
                    https_temp.append(e)        
        
        aux_x = ''.join(https_temp)
        https = aux_x.split()
    
        ## filtragem especfica por url e dominio NCBI
        urls = list()
        
        for pos, e in enumerate(https):
            if 'url' in e and 'ncbi.nlm.nih.gov' in e and e not in urls:
                urls.append(e[5:len(e)-1])
        
        
        ## apenas links st-va ou be-md
        while len(urls) > 1: 
            urls.pop()

        links_full.append(urls[:])
        
#================================================================================================================

#================================================================================================================
# DOWNLOAD DO DATASET E EXPORTAÇAO DOS LINKS GERADOS PARA ARQUIVO .txt NA PASTA LISTAS
    c_exp = 0
    for i in links_full:
        link = ''.join(i)
        os.system(f'echo {link} >> /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/listas/links_{est}.txt')
        os.system(f'mkdir /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{experiments[c_exp]}')
        os.system(f'wget -c -P /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{experiments[c_exp]} {link}')
        c_exp += 1
        
    ## visualizaçao dos links exportados
    c = 0
    file_links = open(f'/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/listas/links_{est}.txt', 'r')
    for i in file_links:
        print(i, end='')
        c += 1
    file_links.close()
    print()
    print(f'Total de links adicionados à lista: {c}')
    print(50*'-')
    print()


#================================================================================================================

#================================================================================================================
# FIM DO PROGRAMA 

print(50*'-')
print('FIM DA EXECUÇÃO DO PROGRAMA')
print(50*'-')

#================================================================================================================



        


