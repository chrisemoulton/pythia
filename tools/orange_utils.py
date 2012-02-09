'''
Created on 8 Feb 2012

@author: george

This module contains functions which perform housekeeping or other 
applications of Orange.
'''
import Orange, orange #!@UnresolvedImport

def construct_orange_table(variables, matrix):
    '''
    Constructs an ExampleTable for Orange. It takes a
    list of variables and the corresponding feature vectors along
    with row identifiers i.e if this is a tweet table rowname would be
    the tweet id.
    '''
    #First construct the domain object (top row)
    vars = []
    for var in variables:
        vars.append(Orange.data.variable.Continuous(str(var)))
    domain = Orange.data.Domain(vars, False) #The second argument indicated that the last attr must not be a class
    
    #Add data rows 
    t = Orange.data.Table(domain, matrix)        
    return t

def add_metas_to_table(table, rownames):
    '''
    Add meta attributes to the samples i.e. the id of the document
    '''
    doc_id = Orange.data.variable.String("id")
    id = Orange.data.new_meta_id()
    table.add_meta_attribute(id)
    table.domain.add_meta(id, doc_id)
    
    for i, id in enumerate(rownames):
        table[i]['id'] = str(id)
        
    return table

def orange_pca(data):
    '''
    Projects the data points on the Principal Components
    '''
    pca = Orange.projection.pca.Pca(data)
    #See Orange documentation to find out what is ignore and ignore 
    matrix, ignore, ignore = pca(data).toNumpy()
    return matrix

def construct_distance_matrix(data):
    '''
    Constructs a distance matrix using Euclidean distance
    '''
    euclidean = orange.ExamplesDistanceConstructor_Euclidean(data)
    distance = orange.SymMatrix(len(data))
    for i in range(len(data)):
        for j in range(i+1):
            distance[i, j] = euclidean(data[i], data[j])
    return distance
        
def orange_mds(distance):
    '''
    It takes as input a distance matrix (see function above)
    and projects the data points using MDS
    '''
    mds = Orange.projection.mds.MDS(distance)
    mds.run(100)
    return mds

