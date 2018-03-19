import requests
from bs4 import BeautifulSoup
import csv

URL = "https://www.vivareal.com.br/venda/sp/sao-bernardo-do-campo/apartamento_residencial/?pagina=__NUMPAG__#onde=BR%3ESao_Paulo%3ENULL%3ESao_Bernardo_do_Campo&tipo-usado=apartamento"
URLbase = "https://www.vivareal.com.br"
def obterPagPesquisada(i):
	rURL = URL.replace("__NUMPAG__", str(i))

	searchPage = requests.get(rURL)
	searchSoup = BeautifulSoup(searchPage.text, "html.parser")

	return searchSoup

def separaNumero(str):
	num = ""
	for x in str:
		if x.isdigit():
			num += x
	return num


def main():
	listaParaImprimir = []
	print("Fazendo varredura nos anuncios...")
	for i in range(1,8):
		print("Pag: "+ str(i))
		searchSoup = obterPagPesquisada(i)
		lugares = searchSoup.findAll("div", {"id": "js-results-panel"})
		lugares = searchSoup.findAll("div", {"id": "js-results-list"})
		primApto = lugares[0].div
		aptos = primApto.find_next_siblings() #todo Aptos menos o Primeiro
		aptos.insert(0,primApto)

		for apto in aptos:
			link = apto.find("a", href = True)
			link = link.get("href")
			aptoPag = requests.get(URLbase + str(link))
			urlApto = URLbase + str(link)
			aptoSoup = BeautifulSoup(aptoPag.text, "html.parser")

			try:
				condNome = aptoSoup.find(class_ = "bh").text
				condNome = condNome.replace(",", "|")
			except:
				condNome = " "

			try:
				endereco = aptoSoup.find(class_ = "bi js-title-location").text
				endereco = endereco.replace(",", "|")
			except:
				endereco = " "

			try:
				precoApto = aptoSoup.find(class_ = "bF js-detail-sale-price").text
				separaNumero(precoApto)
			except:
				precoApto = " "

			try:
				precoCond = aptoSoup.find(class_ = "bI js-detail-condo-price").text
				separaNumero(precoCond)
			except:
				precoCond = " "

			try:
				precoIPTU = aptoSoup.find(class_ = "bI js-detail-iptu-price").text
				separaNumero(precoIPTU)
			except:
				precoIPTU = " "

			try:
				numQuartos = aptoSoup.find(class_ = "by bC js-detail-rooms").text
				numQuartos = separaNumero(numQuartos)
				numQuartos = numQuartos[:1]
			except:
				numQuartos = " "

			try:
				numBanheiros = aptoSoup.find(class_ = "by bD js-detail-bathrooms").text
				numBanheiros = separaNumero(numBanheiros)
			except:
				numBanheiros = " "

			try:
				numVagas = aptoSoup.find(class_ = "by bE js-detail-parking-spaces").text
				numVagas = separaNumero(numVagas)
			except:
				numVagas = " "	

			try:
				area = aptoSoup.find(class_ = "bF js-detail-area-value").text
				area = separaNumero(area)
				area = area[:len(area) - 1]
			except:
				area = " "

			try:
				descricao = aptoSoup.find(class_ = "bQ").text
				descricao = descricao.replace(",", ".") #evitar problemas com CSV
			except:
				descricao = " "							

			linha = [condNome,endereco,precoApto,precoCond,precoIPTU,numQuartos,numBanheiros,numVagas,area, urlApto]

			print(linha)
			if precoApto != " ":
				listaParaImprimir.append(linha)

	f = open("tabelaCSV.csv", "w")
	try:
		print("Gerando arquivo .csv")
		writer = csv.writer(f)
		writer.writerow(("Endereco","PrecoApto","PrecoCond","PrecoIPTU","NumQuartos","NumBanheiros","NumVagas","Area", "URL"))
		writer.writerows(listaParaImprimir)
	finally:
		f.close()
main()

		
