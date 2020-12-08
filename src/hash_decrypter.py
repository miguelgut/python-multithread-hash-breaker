#usr/bin/python2.7
import time
import itertools, string
import hashlib
import sys
import signal
import threading

done = False

## Função de força bruta para quebrar a hash
def _attack(chrs, inputt):
    start_time = time.time()
    total_pass_try=0
    ## Tamanho máximo da senha
    for n in range(1, 8):
      ## Esse operador realiza o produto cartesiano de "n" caracteres com todos os elementos na lista "chrs"
        for xs in itertools.product(chrs, repeat=n):  
            ## Concatena o resultado do produto cartesiano na variável saved            
            saved = (u"".join(xs)).encode('utf-8')
            stringg = saved
            m = hashlib.md5()
            
            ## Transforma o resultado em uma hash md5
            m.update(saved)
            total_pass_try +=1
            
            ## Se o resultado da hash md5 gerada agora é igual ao parâmetro de busca da função, a senha foi quebrada
            if m.hexdigest() == inputt:
                global done
                done = True

                print ("\n[!] found ", stringg)
                print ("\n[-] End Time: ", time.strftime('%H:%M:%S'))
                print ("\n[-] Total Keyword attempted: ", total_pass_try)
                print("\n---Md5 cracked at %s seconds ---" % (time.time() - start_time))
                return stringg.decode('utf-8')