#!/usr/bin/python
import time
import importlib
from threading import Thread, Semaphore
import string
import queue as Queue
import socket
import os.path
import yaml
import hash_decrypter

## Declarando as variáveis globais para utilização no arquivo

global hashes
global results
global current_directory
global chars 

## Iniciando a fila
queue = Queue.Queue()
## Setando os caracteres possíveis
chars = string.ascii_letters + string.digits + "!@#$%&*()_-+=[]{}?/\\|><"
## Pasta atual 
current_directory = os.path.dirname(__file__)
## Auxilia para printar as threads de maneira organizada
screen_lock = Semaphore(value=1)

## Rotina principal
def main():	
	print("[+] Start Time: ", time.strftime('%H:%M:%S'))
	
	## Inicializa as variáveis com o arquivo de resultados e arquivo de hashes
	loadHashes()
	
	## Faz um laço inicializando as threads
	for i in range(4):
		## Cada thread aponta para a função run, passando a fila como parâmetro
		worker = Thread(target=run, args=(i, queue))
		worker.setDaemon(True)
		worker.start()

	## Cada hash é inserida na fila para ser executada
	for h in hashes :
		queue.put(h)
	
	## Ao finalizar todos os elementos da fila, o código encerra-se
	queue.join()
	print ("\n[-] End Time: ", time.strftime('%H:%M:%S'))

## Função de execução de cada hash da fila
def run(i, q):
	while True:
		## Essa função trava a tela para printar melhor a thread que está executando
		screen_lock.acquire()
		print ('%s: Buscando a próxima thread\n' % i, flush=True)
		## Obtem a hash atual na fila
		hash = q.get()
		print ('%s: Executando:\n' % i, hash, flush=True)
		screen_lock.release()

		## Verifica se a hash já possui um resultado na lista de resultados
		if(checkHashIfDecrypted(hash) == False):
			## Se não, chama a função _attack para decodificar
			result = hash_decrypter._attack(chars,hash)
			## Por fim salva o resultado no arquivo de resultados
			saveResult(hash, result)	
		
		q.task_done()

## Carrega os arquivos para buscar as hashes e os arquivos
def loadHashes():	
	global hashes
	global results
	
	with open(os.path.join(current_directory, 'hashes.yaml'),'r') as f:	
		hashes = yaml.safe_load(f)

	with open(os.path.join(current_directory, 'results.yaml'),'r') as f:
		results = yaml.safe_load(f)

## Função para verificar se essa hash já foi decodificada
def checkHashIfDecrypted(hashToCheck):
	global results

	if results == None:
		return False

	## Se está no arquivo de results, já foi decodificada
	if hashToCheck in results:
		return True
	else:
		return False

## Salva o resultado no arquivo de resultados
def saveResult(hash, result):
	global results
	if results == None:
		results = {}
	
	results[hash] = result

	if results:
		with open(os.path.join(current_directory, 'results.yaml'),'w') as f:
			yaml.safe_dump(results, f)


if __name__ == "__main__":
	main()