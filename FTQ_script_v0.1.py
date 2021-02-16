# FTQ_script_v0.1
#================================================================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS

from Bio import Entrez
from urllib.request import urlopen
import os, sys

#================================================================================================================
#================================================================================================================
# SETAGEM DA PASTA RAIZ PARA O ESTUDO ##

raiz = input('Cole o path completo da pasta raiz do estudo: ') # /home/chb-sti-lubuntu/paper_trans_oryza

os.system(f'mkdir {raiz}/data')

data_path = raiz + '/data'

os.system(f'mkdir {data_path}/quantificações')

#================================================================================================================
#================================================================================================================
## BUSCA E ORGANIzAÇÃO DA LISTA DE ESTUDOS - SRP ##

file_access = open(f'{raiz}/listas/estudos_SRP.txt', 'r')

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
    
    c = 0
    
    file_access = open(f'{raiz}/listas/{est}_SRR_Acc_List.txt', 'r')
    
    
    #-----> criação da pasta do estudo e pasta para quants (SRP)
    os.system(f'mkdir {data_path}/{est}')
    os.system(f'mkdir {data_path}/quantificações/{est}')
    
    temp_exp = list()
    
    for exp in file_access:
        if exp == '\n':
            pass
        else:
            temp_exp.append(exp)

#================================================================================================================
#================================================================================================================
# BUSCAR POR CADA EXPERIMENTO NO NCBI/SRA
    
            links_full = list()
                       
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
        
               
            id_url = ','.join(id_list) # adaptador da string UID obtida na fase anterior para montagem correta da url
        
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
        
#-----> filtragem por https

            https_temp = list()
                
            for i in data_full:
                for pos, e in enumerate(i):
                    if 'https://' in e:
                        https_temp.append(e)        
            
            aux_x = ''.join(https_temp)
            https = aux_x.split()
        
#-----> filtragem especfica por url e dominio NCBI entre os https

            urls = list()
            
            for pos, e in enumerate(https):
                if 'url' in e and 'ncbi.nlm.nih.gov' in e and e not in urls:
                    urls.append(e[5:len(e)-1])
            
            
#-----> apenas links st-va ou be-md (evita links duplicados para o mesmo dataset)
            while len(urls) > 1: 
                urls.pop()
    
            links_full.append(urls[:])
        
       
#================================================================================================================
#================================================================================================================
# DOWNLOAD DO DATASET E EXPORTAÇAO DOS LINKS GERADOS PARA ARQUIVO .txt NA PASTA LISTAS
                       
            aux_exp = exp.split()
            path_file = ''.join(aux_exp)
            
            c_exp = 0
            
            for i in links_full:
                link = ''.join(i)
                
                os.system(f'echo {link} >> {raiz}/listas/links_{est}.txt')
                              
               
                os.system(f'mkdir {data_path}/{est}/{path_file}')
                
                print(f'Baixando dataset {exp}')
               
                os.system(f'wget -c --show-progress -P {data_path}/{est}/{path_file} {link}')
                                
                c_exp += 1
               
#================================================================================================================
#================================================================================================================
# FASTQ-DUMP - TRIMMOMATIC - SALMON
        
            file = os.listdir(f'{data_path}/{est}/{path_file}/')    #-----> execução adaptada por caminho padrão
            
            aux_file = ''.join(file)
            for i in file:
                if '.fastq' not in i:
                    aux_fast = str(i)    #-----> pegando o nome do arquivo SRA para fazer o dump
         
            
            print(f'GERANDO O ARQUIVO FASTq PARA O EXPERIMENTO: {aux_fast}')
            
            falha = os.system(f'fastq-dump --gzip --split-spot {data_path}/{est}/{path_file}/{aux_fast} --outdir {data_path}/{est}/{path_file}')
            
            print()
            
            if falha == 0:
                print(f'FASTq PARA {aux_fast} GERADO COM SUCESSO!')
            print()
            
#====================================================================================================
# TRIMMOMATIC
            
            for i in file:
                if '.fastq' not in i:
                    aux_trim = str(i)
            
            origem = f'{data_path}/{est}/{path_file}/{aux_trim}.fastq.gz'
            destino = f'{data_path}/{est}/{path_file}/{aux_trim}_trim.fastq.gz'
            
            
            print(f'APLICANDO O TRIMMOMATIC SOBRE O ARQUIVO {aux_trim}.fastq.gz')
            print()
            
            falha = os.system(f'java -jar {raiz}/tools/Trimmomatic-0.39/trimmomatic-0.39.jar SE -phred33 {origem} {destino} ILLUMINACLIP:TruSeq3-PE-2:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')
            
            print()
            
            if falha == 0:
                print(F'TRIMO PARA {aux_fast}.fastq.gz GERADO COM SUCESSO!')
            print()
            
#====================================================================================================
# SALMON
            
            file = os.listdir(f'{data_path}/{est}/{path_file}/')
            aux_file = ''.join(file)
            
            for i in file:
                if 'trim' in i:
                    aux_salmon = str(i)
                
            print(f'QUANTIFICAÇÃO DO EXPERIMENTO {aux_salmon}')
           
            os.system(f'salmon quant -i oryza_index -l A -r {data_path}/{est}/{path_file}/{aux_salmon} --validateMappings -o {data_path}/quantificações/{est}/{path_file}_quant')
        
            # deleção dos arquivos após quantificação
            os.system(f'rm -r {data_path}/{est}/{path_file}')
            print()            
                        
#================================================================================================================
#================================================================================================================
# DELEÇÃO DA PASTA DOS DATASETS E ARQUIVOS FASTq E TRIMO

    os.system(f'rm -r {data_path}/{est}')    
    
#================================================================================================================
#================================================================================================================
# FIM DO PROGRAMA 

print(50*'-')
print('FIM DA EXECUÇÃO DO PROGRAMA')
print(50*'-')

#================================================================================================================
