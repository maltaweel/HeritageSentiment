'''
Class to create a network of topic model terms and topics.

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
    
    #topics (numbers) and terms to track
    topics={}
    
    #terms from given topics and the term values from topic model
    terms={}

    '''
    Method to load data from topic model results.
    '''
    def loadData(self):
        
        #the pathway to the data to analyze
        directory=os.path.join(pn,'topic_model_results')
        
        #get the text file from the directory
        try:
            for f in listdir(directory):
                
                #only .csv files should open
                if '.csv' not in f:
                    continue
                
                #open the text
                with open(os.path.join(directory,f),'rt') as csvfile:
                    
                    #get the reader
                    reader = csv.DictReader(csvfile)
            
                    #get single reader
                    for row in reader:
                        
                        #get topic number
                        topic=row['Topic']
                        
                        #get the term number
                        term=row['Term']
                        
                        #get the value
                        value=row['Value']
                        
                        #do some replacements to clean the term text
                        term=term.replace("b'","")
                        term=term.replace('b"',"")
                        term=term.replace("'","")
                        term=term.replace('"',"")
                        
                        #now organise into topic and term dictionaries 
                        tps=[]
                        
                        #check to see if topic number is there already
                        if topic in self.topics:
                            tps=self.topics[topic]

                        #append the term to the topic
                        tps.append(term)
                        self.topics[topic]=tps
                        
                        #now do the same thing with terms and their values
                        tms={}
                        
                        #check to see if the topic is associated with the terms
                        if topic in self.terms:
                            tms=self.terms[topic]
                        
                        #add term value (for topic) to the terms
                        tms[term]=value
                        self.terms[topic]=tms
                
      
                        
        # the exception handling           
        except IOError:
            print ("Could not read file:", csvfile)               
    
    '''
    Method to create a networkx network with terms and topics.
    @return G- the undirected network
    '''
    def createNetwork(self):
        
        # create undirected network 
        G = nx.Graph()
      
        #get the topics
        for topic in self.topics:
            
            #get the containers for the topics and terms in topics
            tps=self.topics[topic]
            tms=self.terms[topic]
            
            #now create the graph edges
            for t in tps:
                
                #first check if the given term in topic is in the edges
                es=G.edges(t)
                
                #check both nodes in the edge to see if the term is already there
                for e in list(es):
                    
                    #if the term is in the graph already and is in mulitple topics, then link
                    if e[0]==t:
                        G.add_edge(t, e[0])
                    if e[1]==t:
                        G.add_edge(t, e[1])  
                
                #add the term and topic number edge
                G.add_edge(topic, t, weight=tms[t])
                
        return G
    
    '''
    This method displays the network from a graph given.
    @param G- the network
    '''
    def displayNetwork(self,G):
        
        #create the subplot area to display network
        fig, ax = plt.subplots(figsize=(14, 12))

        #create the network layout
        pos = nx.fruchterman_reingold_layout(G)

        # plot the network (red colour term nodes)
        nx.draw_networkx(G, pos,
                 font_size=12,
                 width=2,
                 node_size=50,
                 edge_color='grey',
                 node_color='red',
                 with_labels = False,
                 ax=ax,
                 alpha=0.8)
       
        # plot the topic numbers (blue colour nodes)
        nx.draw_networkx(G, pos,
                 font_size=12,
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
            x, y = value[0]+.00135, value[1]+.015
            ax.text(x, y,
                    s=key,
                    bbox=dict(facecolor='red', alpha=0.25),
                    horizontalalignment='center', fontsize=8)
    
#        plt.show()
        
        #now output the image to a figure with the pathway in the figure folder
        path=os.path.join(pn,'figure','layout.jpg')
        
        #save the output
        fig.savefig(path,dpi=300)
        
        #close the figure
        plt.close(fig)
        
'''
Method to run the module and call the NetworkWords class.
'''        
def run():
    #create the NetworkWords object
    nw=NetworkWords()
    
    #load data from topic model output
    nw.loadData()
    
    #create the network        
    G=nw.createNetwork()
    
    #output the network to a layout and figure in the figure folder
    nw.displayNetwork(G)
    
    print("Finished")

#run the module
if __name__ == '__main__':
    run()


