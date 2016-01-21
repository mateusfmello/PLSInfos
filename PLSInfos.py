# coding: utf-8
# Script destinado a colher informações de uma determinada página na web
# Informações que seram retornadas

try:
	import sys
	import os
	import urllib2
	import re
	from urlparse import urlparse
	from subprocess import Popen, PIPE
	from datetime import datetime
except :
	quit(st('vermelho') + st('negrito') + '\n\n\nPLSInfos :: Erro ao importar bibliotecas \n\n\n ' + st('reset'))

# FORMATADOR DE URL
def getUrl(url, formatUrl):
	uri = urlparse(url)
	return formatUrl.format(uri=uri)

# SETA O ESTILO DE UM DETERMINADO TEXTO
def st(arg):

	a = '\033['

	if arg == 'rosa':
		b = '95'
	elif arg == 'azul':
		b = '94'
	elif arg == 'verde':
		b = '92'
	elif arg == 'amarelo':
		b = '93'
	elif arg == 'vermelho':
		b = '91'
	elif arg == 'reset':
		b = '0'
	elif arg == 'negrito':
		b = '1'
	elif arg == 'sublinhado':
		b = '4'

	return a + b + 'm'

# FUNÇÃO QUE EXTRAI CONTEÚDO DE DENTRO DE DOIS PONTOS INFORMADOS (START E END)
def getVal(content, start, end):
	i = content.find(start)+len(start)
	if end != '':
		i2 = content[i:].find(r''+end)
	else:
		i2 = len(content)
	return content[i:i+i2]

# CABEÇALHO
def getCabecalho(clear = True):
	if clear:
		os.system('clear')
	return '##### Obrigado por usar o ' + st('negrito') + st('vermelho') + 'PLSInfos' + st('reset') + ' #####\n##### Versão: ' + st('azul') + st('negrito') + '1' + st('reset') + '\n##### Dia/Hora: ' + datetime.now().strftime('%d/%m/%Y %H:%M:%S') + '\n\n'

print getCabecalho()

# OPÇÕES QUE O SCRIPT ACEITA
opcoes = {
	'-v':{
		'long': '--verbose',
		'desc': 'Modo verbose, será exibido uma mensagem infortiva a cada ação relevante do script.'},
	'-h':{
		'long':'--help',
		'desc':'Mostra essa mensagem.'},
	'-ai':{
		'long':'--allinfo',
		'desc':'Mostra todas informações possíveis.'},
	'-s':{
		'plus':'=<local>',
		'long':'--save',
		'desc':'Salva o resultado completo da pesquisa.'}}

# MENU DE AJUDA
def getHelp():
	getCabecalho(False)
	print(st('verde') + st('sublinhado') + 'Uso:' + st('reset') + ' python ' + sys.argv[0] + ' <host> [OPÇÕES]')
	print('\n-- Ex.: python ' + sys.argv[0] + ' <host> ou python ' + sys.argv[0] + ' --help')
	print('\nOpções'.ljust(18) + 'Opções longas'.ljust(25) + 'Descrição'.ljust(100))
	
	# LISTA O CONTEÚDO DO ARRAY OPCOES
	for opcao in opcoes:
		text = ' ' + opcao
		
		try:
			opcoes[opcao]['plus']
		except Exception, e:
			text = text.ljust(15)
		else:
			text += opcoes[opcao]['plus']
			text = text.ljust(15)

		text2 = opcoes[opcao]['long']
		
		try:
			opcoes[opcao]['plus']
		except Exception, e:
			text2 = text2.ljust(23)
		else:
			text2 += opcoes[opcao]['plus']
			text2 = text2.ljust(23)

		text = text + text2 + opcoes[opcao]['desc'].ljust(100)

		print(text)
	print('\nContato: mt@mfmello.com ou 48 9908 3655 (Whatsapp e Telegram)\n')
	quit()

parametros = sys.argv
verbose = False # VARIÁVEL RESPOSÁVEL POR DETERMINAR SE SERÃO OU NÃO EXIBIDAS AS MENSAGENS INFORMATIVAS
allInfo = False # VARIÁVEL RESPOSÁVEL POR DETERMINAR SE O USUÁRIO DEFINIU VIA PARÂMETRO QUE O SCRIPT DEVE EXIBIR TODAS AS INFORMAÇÕES ARRECADADAS
salvar = False # VARIÁVEL RESPONSÁVEL POR DETERMINAR SE O USUÁRIO DEFINIU OU NÃO DEFINIU VIA PARÂMETRO SE O SCRIPT DEVE SALVAR EM UM DETERMINADO ARQUIVO TODAS INFORMAÇÕES EXIBIDAS NA PESQUISA
destinoFile = '~/PLSInfos/' # LOCAL PADRÃO PARA SALVAR OS ARQUIVOS COM OS RESULTADOS
conHosts = None
conHosts3 = None
conMails = None

# PEGANDO HOST SEJA POR PARÂMETRO OU "INPUT"
try:
	if not sys.argv[1].startswith('-'): # VERIFICA SE O PRIMEIRO PARÂMETRO NÃO É UMA OPÇÃO AO EM VEZ DO HOST
		host = sys.argv[1]
	else:
		if sys.argv[1].startswith('-'): # CASO O PRIMEIRO PARÂMETRO SEJA UMA OPÇÃO
			getHelp() # EXIBINDO O MENU DE AJUDA POIS O USUÁRIO ESTA UTILIZANDO O SCRIPT DE FORMA ERRADA
		host = raw_input('Por favor, insira o Host: ') # COMO O USUÁRIO NÃO INFORMOU NENHUM PARÂMETRO O SCRIPT SOLICITA O HOST
		parametros = raw_input('Insira os parâmetros que deseja ou deixe em branco: ') # COMO O USUÁRIO NÃO INFORMOU NENHUM PARÂMETRO CORRETO O SCRIPT SOLICITA AS OPÇÕES
		parametros = parametros.split(' ') # SEPARANDO OPÇÕES
except Exception, e:
	host = raw_input('Por favor, insira o Host: ')
	parametros = raw_input('Insira os parâmetros que deseja ou deixe em branco: ')
	parametros = parametros.split(' ')

# PEGA O LOCAL ONDE O RESULTADO SERÁ SALVO, ESSE VALOR VEM VIA PARÂMETRO (OPÇÕES)
def defSaveFile(exibeHelp, destinoFile, salvar, argMin,arg):
	temPlus = False
			
	try:
		opcoes[argMin]['plus']
	except Exception, e:
		temPlus = False
	else:
		temPlus = True

	if (opcoes[argMin]['long'] == arg) and (temPlus == False):
		exibeHelp = False
	elif (arg.startswith(opcoes[argMin]['long'])) and temPlus:
		if arg.startswith('--save'):
			if arg.startswith('--save='):
				val = getVal(arg, '--save=', '')
				if len(val) > 0:
					destinoFile = val;
			exibeHelp = False
			salvar = True
	elif temPlus:
		if arg.startswith('-s'):
			if arg.startswith('-s='):
				val = getVal(arg, '-s=', '')
				if len(val) > 0:
					destinoFile = val;
			exibeHelp = False
			salvar = True
	return {'exibeHelp':exibeHelp, 'destinoFile':destinoFile, 'salvar':salvar}

# TRATANDO AS OPÇÕES
for i,arg in enumerate(parametros):
	exibeHelp = True
	if (i>1) and (arg not in opcoes):
		for argMin in opcoes:
			retorno = defSaveFile(exibeHelp, destinoFile, salvar, argMin,arg)
			exibeHelp = retorno['exibeHelp']
			destinoFile = retorno['destinoFile']
			salvar = retorno['salvar']

	elif arg.startswith('-s'):
		retorno = defSaveFile(exibeHelp, destinoFile, salvar, '-s', arg)
		exibeHelp = retorno['exibeHelp']
		destinoFile = retorno['destinoFile']
		salvar = retorno['salvar']
	else:
		exibeHelp = False

	if exibeHelp:
		getHelp()

if ('-h' in parametros) or ('--help' in parametros):
	getHelp()
if ('-v' in parametros) or ('--verbose' in parametros):
	verbose = True
if ('-ai' in parametros) or ('--allinfo' in parametros):
	allInfo = True

if not host.startswith('http://') and not host.startswith('https://'): # VERIFICANDO SE O HOST NÃO INICIA COM HTTP:// OU HTTPS://
	hostProt = 'http://' + host # CASO NÃO INICIE É ADICIONADO HTTP:// NO COMEÇO PARA QUE O SCRIPT FUNCIONE CORRETAMENTE
else:
	hostProt = host # SETANDO VARIÁVEL DO HOST COM PROTOCOLO HTTP OU HTTPS
	host = getUrl(host, '{uri.netloc}') # REMOVENDO PROTOCOLOS HTTP, HTTPS E SETANDO VARIÁVEL COM HOST "PURO"

if verbose:
	print(st('azul') + '[i]' + st('reset') + ' Acessando o host ' + st('sublinhado') + hostProt + st('reset')) # MENSAGEM PARA NÃO DEIXAR O USUÁRIO PERDIDO CASO A CONEXÃO E RESPOSTA DO HOST DEMORE
else:
	print(st('azul') + '[i]' + st('reset') + ' Aguarde processando...') # MENSAGEM PARA NÃO DEIXAR O USUÁRIO PERDIDO CASO A CONEXÃO E RESPOSTA DO HOST DEMORE

# PEGANDO PÁGINA E FAZENDO A LEITURA DA MESMA, ESSA LEITURA É INSERIDA EM UMA VARIÁVEL
try:
	pg = urllib2.urlopen(hostProt) # PEGANDO PÁGINA
	if verbose:
		print(st('verde') + '[ok]' + st('reset') + ' Página baixada')
except Exception, e: # CASO OCORRA ERROS É EXIBIDO UMA MENSAGEM AO USUÁRIO E O SCRIPT É FINALIZADO
	quit(st('vermelho') + st('negrito') + '\n\n\nPLSInfos :: Erro ao acessar a página \n\n\n ' + st('reset'))

try:
	content = pg.read() # LENDO CONTEÚDO DA PÁGINA
	if verbose:
		print(st('verde') + '[ok]' + st('reset') + ' Leitura da página foi feita\n')
except Exception, e: # CASO OCORRA ERROS É EXIBIDO UMA MENSAGEM AO USUÁRIO E O SCRIPT É FINALIZADO
	print(pg)
	quit(st('vermelho') + st('negrito') + '\n\n\nPLSInfos :: Erro ao ler a página \n\n\n ' + st('reset'))

conteudoPorLink = re.split(r'<a ', content) # DIVIDINDO PARTES DOS LINKS

# SETANDO ALGUMAS VARIÁVEIS QUE RECEBERAM ENDEREÇOS DE E-MAIL OU HOSTS
hosts = {}
if allInfo:
	hosts3 = {}
else:
	hosts3 = []
mails = []

# SETANDO VARIÁVEL DE HOST SEM WWW
hostSemWww = host.split('www.')
if len(hostSemWww) > 1:
	hostSemWww = hostSemWww[1]
else:
	hostSemWww = hostSemWww[0]

# FUNÇÃO PARA PEGAR DADOS DO HOST
def getHost(host):
	if verbose:
		print(st('azul') + '[i]' + st('reset') + ' Pegando dados do host ' + st('sublinhado') + host + st('reset'))
	p = Popen(['host', getUrl(host, '{uri.netloc}')], stdout=PIPE)
	retorno = []
	while True:
		line = p.stdout.readline()
		retorno.append(line)
		if not line:
			break
	if verbose:
		print(st('verde') + '[ok]' + st('reset') + ' Dados do host ' + st('sublinhado') + host + st('reset') + ' recebidos\n')
	return retorno

# TRATANDO INFORMAÇÕES DO HOST
def getInfos(url):
	dadosHost = getHost(url)
	dados = {}
	dados['ip4'] = []
	dados['ip6'] = []
	dados['alias'] = []
	dados['mails'] = []
	dados['erros'] = []

	for dadoHost in dadosHost:
		dadoHost = dadoHost.replace('\n','')

		if dadoHost != '':
			if dadoHost.find('has address') > -1:
				dadoHost = dadoHost.split(' ')[3]
				dados['ip4'].append(dadoHost)
			elif dadoHost.find('IPv6') > -1:
				dadoHost = dadoHost.split(' ')[4]
				dados['ip6'].append(dadoHost)
			elif dadoHost.find('alias') > -1:
				dadoHost = dadoHost.split(' ')[5]
				dados['alias'].append(dadoHost)
			elif dadoHost.find('mail') > -1:
				dadoHost = dadoHost.split(' ')[6]
				dados['mails'].append(dadoHost)
			else:
				dados['erros'].append(dadoHost)

	return dados

for link in conteudoPorLink: # PERCORRENDO A PÁGINA DIVIDIDA NOS LINKS (<a)

	# PEGANDO O CONTEÚDO DENTRO DO HREF
	url = getVal(link,'href="','"')
	
	if url.startswith('http://') or url.startswith('https://') or url.startswith('//'):
		url = getUrl(url, '{uri.scheme}://{uri.netloc}') # LIMPANDO URL, DEIXANDO APENAS PROTOCOLO E HOST

		if (url.find(hostSemWww) > -1) and (url not in hosts):
			hosts[url] = getInfos(url)
		elif (url.find(hostSemWww) == -1) and (url not in hosts3):
			if allInfo:
				hosts3[url] = getInfos(url)
			else:
				hosts3.append(url)
	elif url.startswith('mailto:'):
		url = url.split('mailto:')[1]
		if url not in mails:
			mails.append(url)

def exibeInfos(info, title, removeCrt = None, resetSt = False):
	qnt = len(info)
	msg = ''
	if qnt > 0:
		msg += '\n====== ' + title + ': '
		for ii,val in enumerate(info):
			if removeCrt != None:
				msg += val[0:(len(val)-removeCrt)]
			else:
				msg += val
			if ii < (qnt-1):
				msg += ', '
			else:
				msg += ';'
	return msg + (st('reset') if resetSt else '')

def preExibeInfos(hosts):
	text = ''
	for h in hosts:
		text += '\n>>> Host: ' + st('negrito') + st('sublinhado') + h + st('reset')
		text += exibeInfos(hosts[h]['ip4'], 'IPv4')
		text += exibeInfos(hosts[h]['ip6'], 'IPv6')
		text += exibeInfos(hosts[h]['alias'], 'Alias', 1)
		text += exibeInfos(hosts[h]['mails'], 'Server' + ('s' if len(hosts[h]['mails']) > 1 else '') + ' e-mail', 1)
		text += exibeInfos(hosts[h]['erros'], st('vermelho') + 'Erro' + ('s' if len(hosts[h]['erros']) > 1 else ''), None, True)
		text += '\n'
	return text

# EXIBINDO OU NÃO, HOST ENCONTRADOS NA PÁGINA
if len(hosts) > 0:
	conHosts = st('azul') + '\n:::::::::: Hosts baseados em ' + st('sublinhado') + hostSemWww + st('reset') + st('azul') + ' ::::::::::' + st('reset')
	conHosts += preExibeInfos(hosts)
	print(conHosts)
else:
	conHosts = st('vermelho') + 'Nessa página não existem outros hosts baseados em ' + st('sublinhado') + st('negrito') + hostSemWww + st('reset') + st('vermelho') + st('reset')
	print(conHosts)

# PEGANDO INFORMAÇÕES DE HOSTS DE TERCEIROS ENCONTRADOS NA PÁGINA DO HOST INFORMADO AO SCRIPT
def infosHosts3(hosts3):
	msg = ''
	if len(hosts3) > 0:
		msg += st('azul') + '\n:::::::::: Hosts de ' + st('negrito') + 'terceiros' + st('reset') + st('azul') + ' ::::::::::' + st('reset')
		msg += preExibeInfos(hosts3)
	else:
		msg += st('vermelho')+'\nNão existem hosts de terceiros na página'+st('reset')
	return msg

exibe = False
if allInfo:
	conHosts3 = infosHosts3(hosts3)
	print (conHosts3)
else:
	exibe = (True if raw_input('\nVocê deseja visualizar informações de hosts de terceiros? [s/n] ').lower() == 's' else False)

if exibe:
	hosts3Tmp = {}
	for host in hosts3:
		hosts3Tmp[host] = getInfos(host)
	conHosts3 = infosHosts3(hosts3Tmp)
	print conHosts3
	hosts3Tmp.clear()

# EXIBE E-MAILS
def exibeMails():
	msg = ''
	if len(mails) > 0:
		msg += st('azul') + '\n:::::::::: E-mails encontrados na página ::::::::::' + st('reset')
		for m in mails:
			msg += '\n' + m + ';'
	else:
		msg += st('vermelho')+'Não existem links de e-mails na página'+st('reset')

	return msg

exibe = False
if allInfo:
	conMails = exibeMails()
	print conMails
else:
	exibe = (True if raw_input('Você deseja visualizar os links de e-mails contidos na página? [s/n] ').lower() == 's' else False)

if exibe:
	conMails = '\n' + exibeMails()
	print conMails

if salvar == False:
	salvar = (True if raw_input('Você deseja salvar essas informações? [s/n] ').lower() == 's' else False)

# RODAPÉ
footer = '\nPesquisa finalizada!!! \n\nDesevolvedor: Mateus Fernandes de Mello \nWebsite: mfmello.com \nGithub: https://github.com/mateusfmello/PLSInfos \n\n' + st('verde') + st('negrito') + 'Finalizando execução.\n' + st('vermelho') + 'PLSInfos\n\n' + st('reset')

if salvar:
	partNome = datetime.now().strftime('%d%m%Y%H%M%S')
	nomeArquivo = hostSemWww + '-' + str(partNome) + '.txt'

	continua = True
	perguntaDestino = False
	while continua:
		newDestinoFile = ''
		if destinoFile == '~/PLSInfos/' or perguntaDestino:
			newDestinoFile = raw_input('\nDigite o local onde deseja salvar (Padrão: ~/PLSInfos/' + nomeArquivo + '):')
			if newDestinoFile == '':
				destinoFile = '~/PLSInfos/'
			else:
				destinoFile = newDestinoFile

			if destinoFile.startswith('~'):
				destinoFile = os.path.expanduser("~") + destinoFile.split('~')[1]

		if (destinoFile != '~/PLSInfos/'):

			if not os.path.isdir(destinoFile):
				res = raw_input(st('vermelho') + '\n[!] ' + st('reset') + 'Esse diretório (' + destinoFile + ') não existe! \nDigite ' + st('negrito') + st('sublinhado') + '1' + st('reset') + ' para cria-lo ou ' + st('negrito') + st('sublinhado') + '2' + st('reset') + ' para inserir um novo caminho: ')
				if res == '1':					
					os.makedirs(destinoFile)
					continua = False
				else:
					perguntaDestino = True
			else:
				continua = False
		else:
			continua = False

	caminhoNome = (destinoFile + nomeArquivo) if destinoFile.endswith('/') else (destinoFile + '/' + nomeArquivo)

	try:
		arquivo = open(caminhoNome, 'w')
		arquivo.write(getCabecalho(False))
		
		if conHosts != None:
			arquivo.write(conHosts)
		
		if conHosts3 != None:
			arquivo.write(conHosts3)
		
		if conMails != None:
			arquivo.write('\n' + conMails)
		
		arquivo.write('\n' + footer)
		arquivo.close()
	except Exception, e:
		print(st('vermelho') + st('negrito') + '[!]' + st('reset') + ' Erro ao criar arquivo')
	else:
		print(st('verde') + '\n[ok]' + st('reset') + ' Arquivo criado com sucesso.')


print(footer)

if salvar:
	quit('CTRL+C and CTRL+V:  cat ' + caminhoNome + '\n')