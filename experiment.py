# -*- coding: utf-8 -*-
# author: Trung Pham 
# description: Script define experiment to build small-world network using networkx in Python
# date: December 11 2022
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np 
import os 


class SmallWorld:
    """Class represent for small-world network to experiment
    """
    def __init__(self, n, k, beta, visualize = True, fig_path = "networkx.png"):
        """Constructor for SmallWorld class

        Parameters
        ----------
        n : int
            The number of nodes
        k : int
            Each node is joined with its k nearest neighbors in a ring topology
        beta : float, int or list
            Rewiring probability
        visualize : bool, optional
            Option to visualize networks, by default True
        fig_path : str, optional
           Path to save visualized image, by default "networkx.png"
        """
        for attr in list(locals().keys()):
            setattr(self, attr, eval(attr))
        if not isinstance(beta, list):
            self.beta = [beta]
        self.g = [nx.watts_strogatz_graph(self.n, self.k, b) for b in self.beta]
        self.pos = [nx.circular_layout(g) for g in self.g]

    def visualize_graph(self):
        """Visualize graph as image

        Raises
        ------
        ValueError
            If number of nodes is too much (>5000), raise ValueError
        """
        if self.n > 5000:
            raise ValueError("Number of nodes is too much, it's hard to visualize graph as image") 
        else:
            avg_paths = self.get_avg_path()
            clusters = self.get_clustering_coefficient()
            for idx, b in enumerate(self.beta):
                labels = f"beta={b}\navg_path_length={round(avg_paths[idx], 2)}\nclustering_coefficient={round(clusters[idx], 2)}"
                plt.figure(figsize=(14,14))
                plt.title(labels, {'fontsize':24})
                nx.draw_networkx(self.g[idx], self.pos[idx])
                plt.savefig(f"graph{idx}.png")
    
    def get_avg_path(self):
        """Get average shortest path

        Returns
        -------
        float or list of float
            _description_
        """
        return [nx.average_shortest_path_length(g) for g in self.g]
    
    def get_clustering_coefficient(self):
        """Get clustering coefficient

        Returns
        -------
        float or list of float
            
        """
        result = np.zeros(len(self.beta))
        betas = np.array(self.beta)
        result = np.where(betas==0, 3*(self.k-2)/4*(self.k-1), result)
        result = np.where(betas==1, self.k/self.n, result)
        result = np.where((betas<1) & (betas>0), (3*(self.k-2)/4*(self.k-1))*((1-betas)**3), result)
        return result.tolist()
    
    def print_info(self, avg_paths, clusters):
        """Print all information to terminal as table

        Parameters
        ----------
        avg_paths : list
            Average path values corresponding beta values
        clusters : list
            Clustering coefficient values corresponding beta values
        """
        print(f"Number of nodes: {self.n}")
        print(f"K: {self.k}")
        print("{:<5} |{:>20} |{:>30} |{:>30}".format("beta", "avg shortest path", "clustering coefficient", "network category"))
        for idx, b in enumerate(self.beta):
            if b == 0:
                network_cat = "Regular network (Ring lattice)"
            elif b == 1:
                network_cat = "Random network"
            else:
                network_cat = "Small-world network"
            print("{:<5} |{:>20} |{:>30} |{:>30}".format(b, avg_paths[idx], clusters[idx], network_cat))

def main():
    network = SmallWorld(20,4,[0, 0.2, 0.4, 1])
    network.print_info(network.get_avg_path(), network.get_clustering_coefficient())
    network.visualize_graph()

if __name__ == "__main__":
    main()