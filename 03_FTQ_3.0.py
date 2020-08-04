# FTQ_3.0 - VERSÃO UTILIZADA - 
# DEVE SER EXECUTADO COM PYTHON 3 NO TERMINAL EM AMBIENTE DE DESNVOLVIMENTO SALMON (conda activate salmon)
#================================================================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS

from Bio import Entrez
import os, sys

#================================================================================================================
# REFERÊNCIA PARA AS PASTAS DOS ESTUDOS

# file_access = open('/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/listas/estudos_SRP.txt', 'r') ## HOME RUN
file_access = open('/media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/listas/estudos_SRP.txt', 'r') ## HD RUN

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
# FASTQ-DUMP e TRIMMOMATIC

for est in estudo:
    # file_access = open(f'/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/listas/{est}_SRR_Acc_List.txt', 'r') ## HOME RUN
    file_access = open(f'/media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/listas/{est}_SRR_Acc_List.txt', 'r') ## HD RUN
    
    temp_exp = list()
    
    for exp in file_access:
        if exp == '\n':
            pass
        else:
            temp_exp.append(exp)
                  
            aux_exp = exp.split()
            path_file = ''.join(aux_exp)
            
            #====================================================================================================
            # FASTq
            
            # file = os.listdir(f'/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{path_file}/') ## HOME RUN
            file = os.listdir(f'/media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/{est}/{path_file}/') ## HD RUN
            aux_file = ''.join(file)
            for i in file:
                if '.fastq' not in i:
                    aux_fast = str(i)
            # os.system(f'fastq-dump --gzip --split-spot /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{path_file}/{aux_fast} --outdir /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{path_file}') ## HOME RUN
            
            print(f'GERANDO O ARQUIVO FASTq PARA O EXPERIMENTO: {aux_fast}')
            
            falha = os.system(f'fastq-dump --gzip --split-spot /media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/{est}/{path_file}/{aux_fast} --outdir /media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/{est}/{path_file}') ## HD RUN
            print()
            
            if falha == 0:
                print(F'FASTq PARA {aux_fast} GERADO COM SUCESSO!')
            print()
            
            #====================================================================================================
            # TRIMMOMATIC
            
            for i in file:
                if '.fastq' not in i:
                    aux_trim = str(i)
                        
            # origem = f'/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{path_file}/{aux_trim}.fastq.gz' ## HOME RUN
            origem = f'/media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/{est}/{path_file}/{aux_trim}.fastq.gz' ## HD RUN
            # destino = f'/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{path_file}/{aux_trim}_trim.fastq.gz' ## HOME RUN
            destino = f'/media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/{est}/{path_file}/{aux_trim}_trim.fastq.gz' ## HD RUN
            
            print(f'APLICANDO O TRIMMOMATIC SOBRE O ARQUIVO {aux_trim}.fastq.gz')
            print()
            
            falha = os.system(f'java -jar /home/chb-sti-lubuntu/datalake_CHB/bioinfo/tools/Trimmomatic-0.39/trimmomatic-0.39.jar SE -phred33 {origem} {destino} ILLUMINACLIP:TruSeq3-SE:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')
            print()
            
            if falha == 0:
                print(F'TRIMO PARA {aux_fast}.fastq.gz GERADO COM SUCESSO!')
            print()
            
            # os.system(f'java -jar trimmomatic-0.39.jar SE -phred33 {origem} {destino} ILLUMINACLIP:TruSeq3-SE:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:17')
            
            # os.system(f'java -jar /home/chb-sti-lubuntu/datalake_CHB/bioinfo/tools/Trimmomatic-0.39/trimmomatic-0.39.jar /home/chb-sti-lubuntu/datalake_CHB/bioinfo/tools/Trimmomatic-0.39/adapters/TruSeq3-SE.fa -phred33 {origem} {destino} ILLUMINACLIP:TruSeq3-SE:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36')
                                   
    file_access.close()
    
    aux_x = ''.join(temp_exp)
    experiments = aux_x.split()
    
    print(f'Total de experimentos para o estudo {est}: {len(experiments)}')
    print(*experiments, sep='  ')
    print(50*'-')
    print()


#================================================================================================================

#================================================================================================================
# SALMON

print('INICÍO DA QUANTIFICAÇÃO COM SALMON')
print()

for est in estudo:
    # file_access = open(f'/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/listas/{est}_SRR_Acc_List.txt', 'r') ## HOME RUN
    file_access = open(f'/media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/listas/{est}_SRR_Acc_List.txt', 'r') ## HD RUN
    
    temp_exp = list()
    
    for exp in file_access:
        if exp == '\n':
            pass
        else:
            temp_exp.append(exp)
                  
            aux_exp = exp.split()
            path_file = ''.join(aux_exp)

            # file = os.listdir(f'/home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{path_file}/') ## HOME RUN
            file = os.listdir(f'/media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/{est}/{path_file}/') ## HD RUN
            aux_file = ''.join(file)
            
            for i in file:
                if 'trim' in i:
                    aux_salmon = str(i)
                
            print(f'QUANTIFICAÇÃO DO EXPERIMENTO {aux_salmon}')
            # os.system(f'salmon quant -i || athal_index || -l A -r {aux_salmon} --validateMappings -o /home/chb-sti-lubuntu/datalake_CHB/bioinfo/PUB_project/data/{est}/{path_file}/{path_file}_quant') ## HOME RUN
            os.system(f'salmon quant -i /media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/reference/oryza_index -l A -r /media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/{est}/{path_file}/{aux_salmon} --validateMappings -o /media/chb-sti-lubuntu/3342B31C7F3AD477/PUB_project/data/{est}/{path_file}/{path_file}_quant') ## HD RUN

    file_access.close()


#================================================================================================================

#================================================================================================================
# FIM DO PROGRAMA 

print(50*'-')
print('FIM DA EXECUÇÃO DO PROGRAMA')
print(50*'-')

#================================================================================================================

