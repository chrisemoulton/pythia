# -*- coding: utf-8 -*-
'''
Created on 13 Nov 2011

@author: george

Unit tests for the analysis.clustering package.
'''
import datetime, unittest 
from database.warehouse import WarehouseServer
from analysis.clustering.kmeans import OrangeKmeansClusterer, CustomClusterer
from tests.test_document import get_orange_clustering_test_data

###########################################
# GLOBALS                                #
###########################################
ws = WarehouseServer()
sample_docs = get_orange_clustering_test_data()

oc = OrangeKmeansClusterer(k=2)
for s in sample_docs:
    oc.add_document(s)
   
#===============================================================================
# cc = CustomClusterer()
# for s in sample_docs:
#    cc.add_document(s)
#    
# cc.construct_term_doc_matrix()
# cc.save_table("custom_clustering_test.txt")
#===============================================================================
    
class TestOrangeClustering(unittest.TestCase):
    
    ###########################################
    # ORANGE TESTS                            #
    ###########################################       
    def test_orange_sample_doc_kmeans(self):
        km = oc.run("orange_clustering_test")
        expected = [0, 0, 0, 1, 1, 1]
        self.assertEqual(expected, km.clusters)

    def test_orange_with_tweets_kmeans(self):            
        from_date = datetime.datetime(2011, 1, 25, 0, 0, 0)
        to_date = datetime.datetime(2011, 1, 26, 0, 0, 0) 
        items = ws.get_documents_by_date(from_date, to_date, limit=200)

        print len(items)
        ##################
        #Index retrievals#
        ##################
        from analysis.index import Index
        index = Index("kmeans_index")
        index.add_documents(items)
        index.finalize()
        print index.get_top_terms()
        ids = index.get_top_documents(lowestf=0.01, highestf=0.2)
        items = []
        for id in ids:
            items.append(ws.get_document_by_id(id))
        ##################
        #Index retrievals#
        ##################
        print len(items)
        
        oc = OrangeKmeansClusterer(k=4, ngram=1)
        oc.add_documents(items)
        oc.run("orange_clustering_test", pca=False)
        oc.plot_timeline(cumulative=True)
        #oc.plot_scatter()
        oc.dump_clusters_to_file("kmeans_with_tweets_orange")
        
#===============================================================================
#        #Experiments
#        max = (0, 0)
#        for i, cluster in enumerate(oc.clusters):
#            if cluster.get_size() > max[1]:
#                max = (i, cluster.get_size())
# 
#        oc_new = OrangeKmeansClusterer(k=5, ngram=2)
#        for doc_id in oc.clusters[max[0]].get_documents().keys():
#            oc_new.add_document(ws.get_document_by_id(doc_id))         
#        oc_new.run("orange_clustering_test")
#        oc_new.dump_clusters_to_file("re-kmeans_with_tweets_orange")
#        #End of experiments      
#===============================================================================
        
    #===========================================================================
    # def test_orange_with_tweets_hierarchical(self):
    #    data = oc.load_table()
    #    sample = data.selectref(orange.MakeRandomIndices2(data), 0)
    #    root = orngClustering.hierarchicalClustering(sample)
    #    orngClustering.dendrogram_draw("hclust-dendrogram.png", root, data=sample, labels=[str(d["id"]) for d in sample]) 
    #===========================================================================
        
    ##########################################
    # CUSTOM TESTS                            #
    ##########################################       
    #===========================================================================
    # def test_sample_doc_hierarchical(self):        
    #    rownames, colnames, data = cc.load_table()
    #    cluster = hierarchical(data, similarity=cosine)
    #    cluster.print_it(rownames)
    #    
    #    dendro = Dendrogram(cluster, rownames, "cluster.jpg", cluster.get_height(), cluster.get_depth())
    #    dendro.draw_node(10, cluster.get_height()/2)
    #   
    # def test_sample_doc_kmeans(self):
    #    rownames, colnames, data = cc.load_table()
    #    
    #    clusters = kmeans(data=data, similarity=cosine, k=2)
    #    c2dp = Cluster2DPlot(data=data, labels=rownames, filename="2dclusters.jpg")
    #    c2dp.draw()
    #   
    # def test_tweet_hierarchical_clustering(self):        
    #    from_date = datetime.datetime(2011, 1, 24, 0, 0, 0)
    #    to_date = datetime.datetime(2011, 1, 25, 0, 0, 0) 
    #    items = ws.get_documents_by_date(from_date, to_date)
    #    
    #    cc = CustomClusterer()
    #    for i in items:
    #        cc.add_document(i.id, i.content)
    #    
    #    cc.construct_term_doc_matrix()
    #    cc.save_table("custom_cluster_with_tweets.txt")
    #    rownames, colnames, data = cc.load_table()
    #    cluster = hierarchical(data)
    #    
    #    rownames = [cc.get_document_by_id(id)["raw"][:140] for id in rownames]
    #    
    #    dendro = Dendrogram(cluster, rownames, "hierarchical_custom_cluster_with_tweets.jpg", cluster.get_height(), cluster.get_depth())
    #    dendro.draw_node(10, cluster.get_height()/2)
    #   
    # def test_tweet_kmeans_clustering(self):        
    #    from_date = datetime.datetime(2011, 1, 24, 0, 0, 0)
    #    to_date = datetime.datetime(2011, 1, 25, 0, 0, 0) 
    #    items = ws.get_documents_by_date(from_date, to_date, 5)
    #    
    #    cc = CustomClusterer()
    #    for i in items:
    #        cc.add_document(i.id, i.content)
    #    
    #    cc.construct_term_doc_matrix()
    #    cc.save_table("custom_cluster_with_tweets.txt")
    #    rownames, colnames, data = cc.load_table()
    #    k=5
    #    km = kmeans(data, similarity=cosine, k=5)
    #    cc.split_documents(km, k)
    #    cc.dump_clusters_to_file("kmeans_with_tweets_custom")
    #===========================================================================
        
            
if __name__ == "__main__":
    unittest.main()