# fetcher_SRP_3.0 - VERSÃO UTILIZADAS
#================================================================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS

from Bio import Entrez

#================================================================================================================
# TERMINAL DE BUSCA INTERATIVO - OPCIONAL

# email = input('E-mail: ')
# db = input('Database: ')
# ident = input('Idtype: ') 
# ret = int(input('Max return: '))
# term = input('Query: ')
# print(50*'-')

#================================================================================================================
# BUSCA DE ID'S NO SRA DATABASE

# term = 'SRP071314'  # SE QUISER BUSCAR APENAS UM ESTUDO
# term = 'SRR8848653' # SE QUISER BUSCAR APENAS UM EXPERIMENTO (NÃO É POSSÍVEL BUSCAR VÁRIOS DE UMA VEZ, PARA ISSO PRECISA DE UM LAÇO)

term = '(heat) AND (leaf OR flag OR shoot OR rice) NOT (spikelet OR endosperm OR mutant OR seed OR floral OR panicle OR flowering OR grain OR mock-treated OR inoculated) AND (Oryza sativa OR rice) AND (RNA-seq OR transcriptome) NOT (miRNA OR ChIP-Seq OR siRNA OR CRISPR OR small RNA OR ATAC-seq OR microarray OR CAGE OR Structure-seq)'

email = 'eubiologo@usp.br'
ret = 200
ident = 'acc'
db = 'sra'

print()

Entrez.email = email

search = Entrez.esearch(db = db, term = term, idtype = ident, retmax = ret)

data = Entrez.read(search)

print(f'Database: {db} | Idtype: {ident} |', end='')
print(f" TotaL de corridas encontradas para a Query: {len(data['IdList'])}")
print(50*'-')

print()

# print(data['IdList']) # printa a lista toda

id_list = list()

# BUSCA POR TODOS AS CORRIDAS DE UM MESMO ESTUDO BASEADO NA LISTA DE IDS ESPEFICICA
# for pos, e in enumerate(data['IdList']):
#     if int(e) != (int(data['IdList'][len(data['IdList'])-1])):
#         id_list.append(e)
#         # pass
#     # else:
#     #     id_list.append(e)
# print(id_list)
# print(50*'-')
# print(f'Total ID\'s RUN filtered: {len(id_list)}')


# BUSCA DE APENAS UMA CORRIDA POR 'ESTUDO/IDr'
for pos, e in enumerate(data['IdList']):
    if int(e) == (int(data['IdList'][pos-1])-1):
        pass
    else:
        id_list.append(e)
print(id_list)
print()

print(f'Total de ID\'s de Corridas equivalentes a 1 ocorrência por Estudo: {len(id_list)}')
print(50*'-')
print()


#================================================================================================================

#================================================================================================================
# BUSCA AUTOMÁTICA DE DADOS XML REFERENTES A CADA PROJETO COM BASE EM SEU ID RUN (uid)

from urllib.request import urlopen

id_url = ','.join(id_list)

data_full = list()

for i in id_list:
    url_mont = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=',db,'&id=',i,'&rettype=fasta&retmode=xml'
    url = ''.join(url_mont)
    
    # url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=sra&id=9975967&rettype=fasta&retmode=xml' # URL PADRÃO DOCUMENTAÇÃO
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
# TESTE DE BUSCA XML - CÓDIGO SRP

link = list()
srp = list()
for i in data_full:
    for pos, e in enumerate(i):
        if 'SRP' in e and len(i[pos]) == 9 and e not in srp:
            # if e not in srp:
                srp.append(e)

print(srp)
print()

print(f'Total de estudos equivalentes às Id\'s enontradas: {len(srp)}')
print(50*'-')
print()
       

#================================================================================================================

#================================================================================================================
# BUSCA PADRÃO DE HTTPS E URLs

https = list()
urls = list()

for i in data_full:
    for pos, e in enumerate(i):
        if 'https://' in e:
            https.append(e)        

a = ''.join(https)
x = a.split()

for pos, e in enumerate(x):
    if 'url' in e and 'ncbi.nlm.nih' in e  and e not in urls:
        urls.append(e)
        
        
# ALTERNATIVA BUSCANDO APENAS OS LINKS DO NCBI
for pos, e in enumerate(x):
    if 'url="https://sra-download.ncbi.nlm.nih.gov' in e and e not in urls:
        urls.append(e)
        # if e == urls[len(urls)-1]:
        #     urls.pop(pos)
        # #print(e)

#================================================================================================================

#================================================================================================================
# PRINTAR AS URL'S NO TERMINAL - OPCIONAL

# print('Links para Download dos Datasets')
# print()
# c = 1
# for i in urls:
#     print(c, i)
#     c += 1


#================================================================================================================

#================================================================================================================
# FIM DO PROGRAMA 

print(50*'-')
print('FIM DA EXECUÇÃO DO PROGRAMA')
print(50*'-')

#================================================================================================================



        
