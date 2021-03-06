from trello import TrelloClient
import os, sys, datetime, subprocess
#add current directory to sys.path to import my_trell_info as a module
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
#import your trello info via the module
import my_trello_info

def connectToTrello(api_key,token):
	client = TrelloClient(api_key, token)
	return client
	
def createLatexDocument(client,outfile):
	now = datetime.datetime.now()
	date_str = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
	outfile.write("\documentclass{article}"+"\n")
	outfile.write("\usepackage{fullpage}"+"\n")
	outfile.write("\\begin{document}"+"\n")
	outfile.write("\\noindent Trello summary list created "+date_str+"\n")
	
	for board in client.list_boards():
		outfile.write("\section*{"+board.name+"}"+"\n")
		for list in board.all_lists():
			if list.closed == 0:
				outfile.write("\paragraph{"+list.name+"}"+"\n")
				outfile.write("\\begin{itemize} \itemsep1pt \parskip0pt \parsep0pt"+"\n")
				for card in list.list_cards():
					outfile.write("\item "+card.name.replace("&","\\&")+"\n")
				outfile.write("\end{itemize}"+"\n")						
	outfile.write("\end{document}")
	outfile.close()
	print("Latex File created")
	print
	subprocess.call(("pdflatex","summary_list.tex"))
	print("PDF File created")
#Example Use
def main():
	my_trello_api_key = os.environ['TRELLO_API_KEY']
	my_trello_token = os.environ['TRELLO_TOKEN']
	if my_trello_api_key and my_trello_token:
		outfile = open("summary_list.tex","w")
		client = connectToTrello(my_trello_api_key,my_trello_token)
		createLatexDocument(client,outfile)
	else:
		print("No api key or trello token set")
		
main()