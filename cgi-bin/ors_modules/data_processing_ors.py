#!/usr/bin/env python3
"""
Program:    data_processing_ors
File:       data_processing_ors.py

Version:    V1.0
Date:       10.05.18
Function:   Process information coming from the middle layer and prepare it for output onto html pages

Copyright:  (c) Oliver Roberts, Birkbeck Bioinformatics student, 2018
Author:     Oliver Roberts
Address:     2018 Bioinformatics Course 1st year ,University of Birkbeck, London
            
--------------------------------------------------------------------------

Revision History:
=================
V1.0   10.05.18   Original   By: ORS (Oliver Roberts)
v2     13.05.18   ver 2      By: ORS - added protein_id to type3_dummy_data
"""

#*************************************************************************
# Import libraries

import collections

#************************************************************************


"""

note: The reason I imported collections was because I wanted to use collections.OrderedDict() due to the fact I gave me
greater flexibility for how I would print the output on the webpage. This is due to the controll it gives me when
generating html tags using a for loop.

When i refer to an ordered dictionary I am refering to the  collections.OrderedDict() functoin



"""





"""
--------------------------------------------------------------------------------
Codon usage dummy data
--------------------------------------------------------------------------------
i must also include the codon ratios across the chromosome and for the coding sequence
(codon, frequency_100, ratio_aa, amino_acid, chr_name) 
VALUES ('aug', 1.89, 1.0, 'met', 'chromosome 16')

I have the dictionary output_dict. Within the output dict I have a key chromosome_codon_usage with its value
being a dictiony containing all the codons and their usage for that chromosome.
Within output dict is another cds_codon usage.

each of those dictionaries have sub dictionaries of each codon key with the value a list. 

example

ouptut_dict = {'chromosome_codon_usage':{'aug':[freq_100:1.89,1.0,'met']}}
"""

 # They will follow the format 'codon':[requencey_100, ratio_aa, amino_acid]
chromosome_codon_usage = {
     'aug':[ 1.89, 1.0, 'met'],'cag':[3.91, 0.85, 'gln'],'ccg':[ 1.29, 0.18, 'pro'],'aga': [0.8, 0.12, 'arg'],
     'acu': [0.78, 0.16, 'thr'],'cuc': [2.47, 0.23, 'leu'],'guu': [0.66, 0.11, 'val'],'cug': [5.64, 0.53, 'leu'],
     'ugc': [1.63, 0.67, 'cys'],'ucc': [2.01, 0.25, 'ser'],'gug': [3.41, 0.55, 'val'],'cua': [0.45, 0.04, 'leu'],
     'aca': [1.02, 0.21, 'thr'],'ucu': [1.05, 0.13, 'ser'],'gca': [1.38, 0.17, 'ala'],'gaa': [1.65, 0.26, 'glu'],
     'gau': [1.34, 0.3, 'asp'],'uug': [0.92, 0.09, 'leu'],'gac': [3.15, 0.7, 'asp'],'ccu': [1.51, 0.21, 'pro'],
     'gga': [1.24, 0.17, 'gly'],'uuu': [1.07, 0.31, 'phe'],'aaa': [1.33, 0.3, 'lys'],'uuc': [2.34, 0.69, 'phe'],
     'cau': [0.74, 0.26, 'his'],'auc': [2.14, 0.66, 'ile'],'aau': [0.88, 0.33, 'asn'],'cca': [1.5, 0.21, 'pro'],
     'gcu': [1.56, 0.19, 'ala'],'auu': [0.8, 0.25, 'ile'],'gag': [4.8, 0.74, 'glu'],'uca': [0.84, 0.11, 'ser'],
     'aac': [1.82, 0.67, 'asn'],'acc': [2.22, 0.45, 'thr'],'agu': [0.8, 0.1, 'ser'],'ugu': [0.8, 0.33, 'cys'],
     'aag': [3.15, 0.7, 'lys'],'cgc': [1.67, 0.25, 'arg'],'uau': [0.65, 0.29, 'tyr'],'guc': [1.76, 0.28, 'val'],
     'ucg':[ 0.71, 0.09, 'ser'],'agc':[ 2.52, 0.32, 'ser'],'uac':[ 1.62, 0.71, 'tyr'],'ggc':[ 3.19, 0.43, 'gly'],
     'uua':[ 0.28, 0.03, 'leu'],'aua':[ 0.3, 0.09, 'ile'],'cgg':[ 1.73, 0.26, 'arg'],'ccc':[ 2.88, 0.4, 'pro'],
     'gcg':[ 1.41, 0.17, 'ala'],'ggg':[ 2.11, 0.28, 'gly'],'caa':[ 0.69, 0.15, 'gln'],'agg':[ 1.47, 0.22, 'arg'],
     'gua':[ 0.37, 0.06, 'val'],'cga':[ 0.55, 0.08, 'arg'],'cac':[ 2.13, 0.74, 'his'],'gcc':[ 3.9, 0.47, 'ala'],
     'cgu':[ 0.49, 0.07, 'arg'],'acg':[ 0.86, 0.18, 'thr'],'ggu':[ 0.89, 0.12, 'gly'],'ugg':[ 1.54, 1.0, 'trp'],
     'cuu':[ 0.85, 0.08, 'leu'],'uga':[ 0.25, 0.55, 'ter'],'uaa':[ 0.11, 0.25, 'ter'],'uag':[ 0.09, 0.2, 'ter'],
     }

#This is the same as the chromosome_codon_usage but with modified requency and aa_ratio
cds_codon_usage = {
     'aug':[ 1.83, 1.0, 'met'],'cag':[3.91, 0.35, 'gln'],'ccg':[ 1.49, 0.28, 'pro'],'aga': [0.5, 0.22, 'arg'],
     'acu': [0.68, 0.36, 'thr'],'cuc': [2.77, 0.43, 'leu'],'guu': [1.66, 0.51, 'val'],'cug': [1.64, 0.73, 'leu'],
     'ugc': [1.63, 0.87, 'cys'],'ucc': [2.01, 0.95, 'ser'],'gug': [4.41, 0.15, 'val'],'cua': [0.45, 0.24, 'leu'],
     'aca': [2.02, 0.31, 'thr'],'ucu': [1.05, 0.43, 'ser'],'gca': [0.38, 0.67, 'ala'],'gaa': [2.65, 0.26, 'glu'],
     'gau': [0.34, 0.3, 'asp'],'uug': [1.92, 0.49, 'leu'],'gac': [3.15, 0.5, 'asp'],'ccu': [2.51, 0.61, 'pro'],
     'gga': [0.24, 0.77, 'gly'],'uuu': [3.07, 0.81, 'phe'],'aaa': [1.33, 0.2, 'lys'],'uuc': [2.34, 0.49, 'phe'],
     'cau': [2.74, 0.56, 'his'],'auc': [2.14, 0.66, 'ile'],'aau': [2.88, 0.73, 'asn'],'cca': [0.5, 0.22, 'pro'],
     'gcu': [1.56, 0.39, 'ala'],'auu': [0.8, 0.45, 'ile'],'gag': [4.8, 0.14, 'glu'],'uca': [0.84, 0.31, 'ser'],
     'aac': [0.82, 0.57, 'asn'],'acc': [0.22, 0.25, 'thr'],'agu': [0.8, 0.2, 'ser'],'ugu': [0.8, 0.43, 'cys'],
     'aag': [0.15, 0.4, 'lys'],'cgc': [0.67, 0.15, 'arg'],'uau': [0.65, 0.39, 'tyr'],'guc': [1.76, 0.38, 'val'],
     'ucg':[ 0.71, 0.19, 'ser'],'agc':[ 1.52, 0.22, 'ser'],'uac':[ 1.62, 0.21, 'tyr'],'ggc':[ 2.19, 0.13, 'gly'],
     'uua':[ 0.28, 0.33, 'leu'],'aua':[ 1.3, 0.19, 'ile'],'cgg':[ 1.73, 0.26, 'arg'],'ccc':[ 2.88, 0.1, 'pro'],
     'gcg':[ 2.41, 0.27, 'ala'],'ggg':[ 1.11, 0.38, 'gly'],'caa':[ 1.69, 0.15, 'gln'],'agg':[ 2.47, 0.32, 'arg'],
     'gua':[ 0.37, 0.16, 'val'],'cga':[ 1.55, 0.38, 'arg'],'cac':[ 2.13, 0.14, 'his'],'gcc':[ 2.9, 0.47, 'ala'],
     'cgu':[ 0.49, 0.17, 'arg'],'acg':[ 1.86, 0.28, 'thr'],'ggu':[ 1.89, 0.32, 'gly'],'ugg':[ 2.54, 1.4, 'trp'],
     'cuu':[ 1.85, 0.18, 'leu'],'uga':[ 1.25, 0.25, 'ter'],'uaa':[ 1.11, 0.15, 'ter'],'uag':[ 1.09, 0.3, 'ter'],
     }
"""
this will turn the dictary of conds into 16 lists of 4 lists each

dnaList = []
dnaList[0] = {"CCU":["CCP","CCQ","CCT"],"ABC":["ABD","ABE","ABF"],"EFG":["657","AasdE","AasdBF"] }
dnaList[1] = {"CCU":["CCP","CCQ","CCT"],"ABC":["ABD","ABE","ABF"] }
dnaList[2] = {"CCU":["CCP","CCQ","CCT"],"ABC":["ABD","ABE","ABF"] 


"""




"""
--------------------------------------------------------------------------------
Type 0,1,2 Middle Layer Dummy data example
--------------------------------------------------------------------------------
{'output':
 {'type': 2, 'pre_set': True, 'name': 'AB001090', 'enzyme': 'ecori'},

 'originaldata': {'locus_sequence': 'aggagcagagcaggcaatttcaccaccaaattatgtatg', 
'chr_location': '16q24', 
'locus_name': 'AB001103', 
'chr_name': 'chromosome 16', 
'gene_name': '', 
'product_name': 'H-cadherin', 
'product_id': 'BAA32411.1',
'seq_location': '1669..1713,6321..6463,6818..7051,7358..7576,7950..7957', 
'whole_seq': 'atgcagccgagaactctgcaacgcggcgggggccctgcgcttcagcctgccctcagtcctgctcctcagcctcttcagcttagcttgtctgtga', 
'translation': 'MQPRTPLVLCVLLSQVLDLLRFSLPSVLLLSLFSLACL'}, 

'cds_translation_alignment': {'whole_seq': 'atgcagctacG<SPAN STYLE=BACKGROUND-COLOR:#0081D5>ATACACACCCTCNNNNTTCAG<SPAN STYLE=BACKGROUND-COLOR:#0081D5>GTCTGTGA</SPAN>GAACTCCTGTCAAAAGAC'}
"""

"""
this is an example of the dummy data i would expect to recieve from the middle layer. 
"""
type012_dummy_data = {'output'      :{'type': 2, 'pre_set': True, 'name': 'AB001090', 'enzyme': 'ecori'},         
                  'originaldata':{'locus_sequence': 'aggagcagagcaggcaatttcaccaccaaattatgtatg',
                                'chr_location': '16q24',
                                'locus_name': 'AB001103',
                                'chr_name': 'chromosome 16',
                                'gene_name': '',
                                'product_name': 'H-cadherin', 
                                'product_id': 'BAA32411.1',
                                'seq_location': '1669..1713,6321..6463,6818..7051,7358..7576,7950..7957', 
                                'whole_seq': 'atgcagccgagaactctgcaacgcggcgggggccctgcgcttcagcctgccctcagtcctgctcctcagcctcttcagcttagcttgtctgtga', 
                                'translation': 'MQPRTPLVLCVLLSQVLDLLRFSLPSVLLLSLFSLACL'},          
    'cds_translation_alignment' :{'whole_seq': 'atgcagctacG<SPAN STYLE=BACKGROUND-COLOR:#0081D5>ATACACACCCTCNNNNTTCAG<SPAN STYLE=BACKGROUND-COLOR:#0081D5>GTCTGTGA</SPAN>GAACTCCTGTCAAAAGAC'},
        'chromosome_codon_usage': chromosome_codon_usage,
              'cds_codon_usage' : cds_codon_usage}





"""
----------------------------------------------------------------------------------------------------------------
Type 3 cromosomal location dummy data
---------------------------------------------------------------------------------------------------------------

 This is the format that data from the middle layer should return to the front layer from a location query.
 . This returns as 1 dictionary of the origonal input for identifying purposes. It then returns 3 dicts each
 containg a list of the associated genes, proteins and accession numbers for that location query. 
"""
type3_dummy_data = {
               'output'     :{'type': 3, 'pre_set': True, 'name': 'AB001090', 'enzyme': 'ecori'},
               'gene'       :['gene1','gene2','gene3','gene4'],
               'protein'    :['protein1','protein2','protein3','protein4'],               
               'accession'  :['accession1','accession2','accession3','accession4'],
               'location'   :['location1','locatoin2','location3','location4'],
               
               }


"""
--------------------------------------------------------------------------------
TYPE 4 duplicate dummy data 
--------------------------------------------------------------------------------
The type being changed to type 4 (as opposed to type 0 =gene, 1= protein, 3 = accession, 4 =location) indicates
that there has been multiple returns for that "name" and type. The returned data aslo includes the
product_name,gene_name,	product_id, accession_num as stored in the middle layer.

front_layer_output = {'type': 2, 'pre_set': True, 'name': 'AB001090', 'enzyme': 'ecori'}



The additional data is to help identify to the user which version they want to query. 
give them the optoin to select which version they would like. I then return to the middle layer 


once a version is selected  i return a single dictionry of the selected version to the middle layer consisting of the normal output + the product_id as a unique identifier.


front_layer_duplicate_output = {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori', 'product_id':'BAA32411.1'}

"""
 

type4_dummy_data = [
                {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori', 'product_id':'BAA32411.1','product_name':'-14 gene' , 'gene_name':'nthl1/nth1','accession_num':'ab014460'},
                {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori', 'product_id':'cab06556.1','product_name':'-14 gene protein ', 'gene_name':'','accession_num':'z84722'},
                {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori', 'product_id':'abd95907.1','product_name':'11 beta-hydroxysteroid dehydrogenase 2', 'gene_name': 'c16orf35','accession_num':'dq431198'}
                ]






"""
-------------------------------------------------------------------------------
TYPE 5 Not found dummy data 
-------------------------------------------------------------------------------
A found found dummy data is if the request is a user input and does not have an entry
in our database of if there is an entry in our database and it. It is returned to the middle layer
as a dictionary in the same format as the middle layer output but with the "type" value changed.

This is then presented to the user with a message saying that 
"""

type5_dummy_data = {'type': 5, 'pre_set': True, 'name': 'AB001090', 'enzyme': 'ecori'}






"""
----------------------------------------------------------------------------------------------
Programs
----------------------------------------------------------------------------------------------
"""
"""
--------------------------------------------------------------------------------------
codon_organiser
---------------------------------------------------------------------------------------

input: Dictionary

a dict with the condons as the key and the [requencey_100, ratio_aa, amino_acid] as values

output: Dictionary

a dict with 16 sub dicts. each sub dict representing a row on a codon table

"""

def codon_organiser(codons):
    d = codons

    dna_list = {}
    dna_list[0]={'uuu': d['uuu'],'ucu': d['ucu'],'uau': d['uau'],'ugu': d['ugu']}
    dna_list[1]={'uuc': d['uuc'],'ucc': d['ucc'],'uac': d['uac'],'ugc': d['ugc']}
    dna_list[3]={'uua': d['uua'],'uca': d['uca'],'uaa': d['uaa'],'uga': d['uga']}
    dna_list[4]={'uug': d['uug'],'ucg': d['ucu'],'uag': d['uag'],'ugg': d['ugg']}

    dna_list[5]={'cuu': d['cuu'],'ccu': d['ccu'],'cau': d['cau'],'cgu': d['cgu']}
    dna_list[6]={'cuc': d['cuc'],'ucc': d['ccc'],'cac': d['cac'],'ugc': d['cgc']}
    dna_list[7]={'cua': d['cua'],'cca': d['cca'],'caa': d['caa'],'cga': d['cga']}
    dna_list[8]={'cug': d['cug'],'ccg': d['ccu'],'cag': d['cag'],'cgg': d['cgg']}

    dna_list[9]={'auu': d['auu'],'acu': d['acu'],'aau': d['aau'],'agu': d['agu']}
    dna_list[10]={'auc': d['auc'],'acc': d['acc'],'aac': d['aac'],'agc': d['agc']}
    dna_list[11]={'aua': d['aua'],'aca': d['aca'],'aaa': d['aaa'],'aga': d['aga']}
    dna_list[12]={'aug': d['aug'],'acg': d['acu'],'aag': d['aag'],'agg': d['agg']}

    dna_list[13]={'guu': d['guu'],'gcu': d['gcu'],'gau': d['gau'],'ggu': d['ggu']}
    dna_list[14]={'guc': d['guc'],'gcc': d['gcc'],'gac': d['gac'],'ggc': d['ggc']}
    dna_list[15]={'gua': d['gua'],'gca': d['gca'],'gaa': d['gaa'],'gga': d['gga']}
    dna_list[16]={'gug': d['gug'],'gcg': d['gcu'],'gag': d['gag'],'ggg': d['ggg']}

    return(dna_list)





"""
----------------------------------------------------------------------------------------------
program for type 0,1,2 processing (gene, protein and accession)
----------------------------------------------------------------------------------------------



The purpose of this program is to take the output from a gene, protein or accesion query (types 0,1,2,) respectivly)
 and order them into a output list that i can pass to the websites as an array.


 input : a dictionry

 containing 4 sub dictionaries
 input = {
          output:{output values},
          origonal_data :{ retreived data from Database},
          chromosome_codon_usage : {codons as keys and value attribues },
          chromosome_codon_usage : {codons as keys and value attribues}
          }
          

 output: a list
 a list of 4 dicts. 1st an ordered dict containg the product information name, type, seq etc
         2nd containg  a list containing 16 dicts. And each dict containg 4 sub dicts.
         ( this represents the structure i will use for making a table.")
         3nd containg  16 lists, each of which contains a dicts with 4 codons.

          input = [
                   'general_data':{output values},
                   origonal_data :{ retreived data from Database},
                   chromosome_codon_usage : {codons as keys and value attribues },
                   chromosome_codon_usage : {codons as keys and value attribues}
                  ]


 variables
 
    middle_data = output from the middle layer
    output_dict = collections.OrderedDict()

 
"""

def gene_protein_accession_processing(middle_data):

    list_of_dicts = []
    
    output_dict = collections.OrderedDict()
    output = middle_data

    output_dict['searched_name']=output['output']['name']
    
    
    if output['output']['type'] == 0:
        output_dict['searched_type'] = "gene"
        
    elif output['output']['type'] == 1:
        output_dict['searched_type'] = "protein"
        
    elif output['output']['type'] == 2:
        output_dict['searched_type'] = "acession"
        
        
    else:
        output_dict['searched_type']= "not found"

        
    output_dict['chromosome']           =output['originaldata']['chr_name']
    output_dict['chromosomal location'] =output['originaldata']['chr_location']
    output_dict['locus name']           =output['originaldata']['locus_name']
    
    # not sure if we need the whole sequence
    #output_dict['locus sequence']       =output['originaldata']['locus_sequence']
    output_dict['gene name']            =output['originaldata']['gene_name']
    output_dict['cds']                  =output['originaldata']['whole_seq']
    output_dict['product name']         =output['originaldata']['product_name']
    output_dict['translation']          =output['originaldata']['translation']
    output_dict['whole sequence']       =output['cds_translation_alignment']['whole_seq']

    

    

    organised_chromosome_codon = (codon_organiser(chromosome_codon_usage))
    organised_cds_codon = (codon_organiser(cds_codon_usage))

    list_of_dicts += [output_dict]
    list_of_dicts += [organised_chromosome_codon]
    list_of_dicts += [organised_cds_codon]
    
    
    return list_of_dicts


"""
------------------------------------------------------------------------------------------------
Program for Type 3 processing (location)
-----------------------------------------------------------------------------------------------

input: a dictionary


output: a dictionary

an ordered dictionary with 6 keys. searched_name, type, associated_genes, associated_proteins,
associated_accession, associated_locatoin. 

variables: middle_data
           output_dict


"""

def location_processing(middle_data):
    
    output_dict =  collections.OrderedDict()
    output = middle_data
    output_dict["searched_name"]= output["output"]["name"]

    if output['output']['type'] == 3:
        output_dict['searched_type'] = "location"
        
    else:
        return TypeError("This is in locaiton_processing but is not type 3")
    
    output_dict["associated_genes"] = output["gene"]
    output_dict["associated_protein"] = output["protein"]
#    output_dict["associated_protein_id"] = output['protein_id']    
    output_dict["associated_accession"] = output["accession"]
    output_dict["associated_location"] = output["location"]

    
    return(output_dict)


"""
------------------------------------------------------------------------------------------------
Program for Type 4 processing (duplicate)
-----------------------------------------------------------------------------------------------

input: dictionary/list

This contains the query sent to middle layer and additional information brought back. it
can take the form of 
i) type 0,1,2,3 a dictionary
ii) type 4 a list 
iii) type 5 a dictionary



output: dictionary

each entry will give a ordered dict of d = collections.OrderedDict() with the

key being query and returned data and the value being a dict containing the origonal query
"""
   


"""
The additional data is to help identify to the user which version they want to query. 
give them the optoin to select which version they would like. I then return to the middle layer 


once a version is selected  i return a single dictionry of the selected version to the middle layer consisting of the normal output + the product_id as a unique identifier.


front_layer_duplicate_output = {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori', 'product_id':'BAA32411.1'}

example of input
"""
type4_output = [
                {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori', 'product_id':'BAA32411.1','product_name':'-14 gene' , 'gene_name':'nthl1/nth1','accession_num':'ab014460'},
                {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori', 'product_id':'cab06556.1','product_name':'-14 gene protein ', 'gene_name':'','accession_num':'z84722'},
                {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori', 'product_id':'abd95907.1','product_name':'11 beta-hydroxysteroid dehydrogenase 2', 'gene_name': 'c16orf35','accession_num':'dq431198'}
                ]
"""
example of output

type4_processed_data =  [
                        {'query':  {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori'}, "additional_data" : {'product_id':'BAA32411.1','product_name':'-14 gene' , 'gene_name':'nthl1/nth1','accession_num':'ab014460'}},
                        {'query':  {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori'}, "additional_data" : {'product_id':'C34511.1','product_name':'-14 gene' , 'gene_name':'nthl1/nth1','accession_num':'ab014460'}},
                        {'query':  {'type':4, 'pre_set':True, 'name':'AB001090', 'enzyme':'ecori'}, "additional_data" : {'product_id':'A523162411.1','product_name':'-14 gene' , 'gene_name':'nthl1/nth1','accession_num':'ab014460'}}
                        ]

       variables: middle_layer_data                 
"""





def duplicate_processing(duplicate_data):
    
    output_list = []
    output = duplicate_data
    
    for d in output:
        temp_dict = {}
    

        temp_dict["query"] = {'name': d['name'], 'type' : d['type'],'pre_set' : d['pre_set'],'enzyme':d['enzyme'],"product_id": d['product_id']}
        temp_dict["additional_data"] = {
                                        'product_id' : d['product_id'], 'product_name' : d['product_id'],
                                        'gene_name' : d['gene_name'], 'accession_num' : d['accession_num']
                                        }
        output_list.append(temp_dict)

    return output_list





"""
------------------------------------------------------------------------------------------------
Program for Type 5 processing (No entry found)
-----------------------------------------------------------------------------------------------

Input : a dict of the origonal query with the type changed to 5
       type5_output = {'type': 5, 'pre_set': True, 'name': 'AB001090', 'enzyme': 'ecori'}

output: {'type': 5, 'pre_set': True, 'name': 'AB001090', 'enzyme': 'ecori'}

The data is passed though unmodified so there is actually no program required 

"""




"""
------------------------------------------------------------------------------------------------
Program for determining Type of middle layer output
-----------------------------------------------------------------------------------------------

INPUT:  The output from the middle layer. This can take the form of either a nested dict,. 

OUTPUT: Dictionary

an ordered dict with the correctly formated data for that call

This determines what type the output data is [0,1,2,3,4] and which processing operatoins to apply to them.

variables :
             

"""

def determine_type_of_middle_output(middle_layer_return):
    middle_data = middle_layer_return
    if "output" in middle_data:
        
# output in middle_data indicates it is a type 0,1,2 dict of dicts or type 3 return from the middle layer

        if middle_data["output"]["type"] == 0:
            processed_data = gene_protein_accession_processing(middle_data)
            return(processed_data)
        
        elif middle_data["output"]["type"] == 1:
            processed_data = gene_protein_accession_processing(middle_data)
            return(processed_data)
        
        elif middle_data["output"]["type"] == 2:  
            processed_data = gene_protein_accession_processing(middle_data)
            return(processed_data)
        
# this indicates a type 3 list of dicts for a location answer

        elif middle_data["output"]["type"] ==3:
            processed_data = location_processing(middle_data)
            return(processed_data)
        
        #This was required as if is search for key == 4 where there is no key due
        # to it being a list of lists of a list of dicts it will throw a type error
        
    elif 'type' in middle_data:
        processed_data = middle_data
        return(middle_data)

    
    elif any( 'type' in d for d in middle_data):     
        temp_val = ([d['type'] for d in middle_data if 'type' in d])
        if 4 in temp_val :
            
            processed_data = duplicate_processing(middle_data)     
            return(processed_data)

        
    else:
        return TypeError("middle_layer_output_processing could not determine data catagory ")

    


#print(determine_type_of_middle_output(type3_dummy_data))




"""
This would be a dummy example of the output from middle_layer to front_layer, where it contains the initial output with the query, 
the db dictionary without being modified and the extra information modified, sent as a dictionary of dictionaries.
 """
          
