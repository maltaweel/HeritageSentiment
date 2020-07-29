'''
Created on Jul 29, 2020

@author: mark
'''
import csv
import os
import networkx as nx
from os import listdir
import matplotlib.pyplot as plt

#use this as the starting pathway (the src folder)
pn=os.path.abspath(__file__)
pn=pn.split("src")[0]



class NetworkWords():
    
    topics={}
    terms={}

    def loadData(self):
        
        #the pathway to the data to analyze
        directory=os.path.join(pn,'topic_model_results')
        
        #get the text file from the directory
        try:
            for f in listdir(directory):
                
                
                if '.csv' not in f:
                    continue
                
                #open the text
                with open(os.path.join(directory,f),'rt') as csvfile:
                    
                    #get the reader
                    reader = csv.DictReader(csvfile)
            
                    #get single reader
                    for row in reader:
                        
                        #get text
                        topic=row['Topic']
                        term=row['Term']
                        value=row['Value']
                        
                        term=term.replace("b'","")
                        term=term.replace('b"',"")
                        term=term.replace("'","")
                        term=term.replace('"',"")
                        
                        tps=[]
                        if topic in self.topics:
                            tps=self.topics[topic]

                        tps.append(term)
                        self.topics[topic]=tps
                        
                        tms={}
                        if topic in self.terms:
                            tms=self.terms[topic]
                        
                        tms[term]=value
                        self.terms[topic]=tms
                
      
                        
        # the exception handling           
        except IOError:
            print ("Could not read file:", csvfile)               
    
    def createNetwork(self):
        # Create network plot 
        G = nx.Graph()
      
        for topic in self.topics:
            tps=self.topics[topic]
            tms=self.terms[topic]
            
            for t in tps:
                es=G.edges(t)
                
                for e in list(es):
                    if e[0]==t:
                        G.add_edge(t, e[0])
                    if e[1]==t:
                        G.add_edge(t, e[1])  
                    
                G.add_edge(topic, t, weight=tms[t])
                
        return G
    
    def displayNetwork(self,G):
        
        fig, ax = plt.subplots(figsize=(20, 18))

        pos = nx.fruchterman_reingold_layout(G)

        # Plot networks
        nx.draw_networkx(G, pos,
                 font_size=8,
                 width=2,
                 node_size=50,
                 edge_color='grey',
                 node_color='red',
                 with_labels = False,
                 ax=ax,
                 alpha=0.8)
       
        nx.draw_networkx(G, pos,
                 font_size=8,
                 width=2,
                 node_size=120,
                 nodelist=["0","1","2","3","4","5","6","7","8","9"],
                 edge_color='grey',
                 node_color='blue',
                 with_labels = False,
                 ax=ax,
                 alpha=0.8)
        # Create offset labels
        for key, value in pos.items():
            x, y = value[0]+.0135, value[1]+.045
            ax.text(x, y,
                    s=key,
                    bbox=dict(facecolor='red', alpha=0.25),
                    horizontalalignment='center', fontsize=8)
    
#        plt.show()
        
        path=os.path.join(pn,'figure','layout.jpg')
        fig.savefig(path,dpi=300)
        plt.close(fig)
        
        
def run():
    nw=NetworkWords()
    nw.loadData()        
    G=nw.createNetwork()
    nw.displayNetwork(G)

#run the module
if __name__ == '__main__':
    run()


