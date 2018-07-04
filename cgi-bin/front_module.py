#!/usr/bin/env python3
"""
###################
last changes
edidted the data processing.py
    duplicate_processing funciton
    added the product id to 'query' dict
###################

"""




"""
Program:    front_module
File:       front_module.py

Version:    V1.0
Date:       10.05.18
Function:   creates and recives data from html pages. 

Copyright:  (c) Oliver Roberts, Birkbeck Bioinformatics student, 2018
Author:     Oliver Roberts
Address:     2018 Bioinformatics Course 1st year ,University of Birkbeck, London
            
--------------------------------------------------------------------------

Revision History:
=================
V1.0   10.05.18   Original   By: ORS (Oliver Roberts)
v2.0   13.05.18              By: ORS

Changelog
v2.0 - Changed preset to pre_set thoughtout program
"""

#************************************************************************
# Import libraries

#import collections
import cgitb,cgi,codecs,unittest,tempfile
cgitb.enable()
 
from middle_output_preliminar import middle_to_db
from ors_modules.data_processing_ors import gene_protein_accession_processing, location_processing, duplicate_processing, determine_type_of_middle_output

# for use in testsing, REMOVE BEFORE HAND IN
from ors_modules.dummy_data_ors import type012_dummy_data, type3_dummy_data, type4_dummy_data, type5_dummy_data
#************************************************************************


"""
#*************************************************************************
def print_page(result,results):
    inserts the html output into a string of the html file for presenting

    Input:  file       --- a html file
            results    --- a string
    Return: None  --- Prints a webpage 
                             

    10.05.18  Original   By: ORS
"""

def print_page(file, results):
    
    print("Content-Type: text/html\n")

    f=codecs.open(file, 'r')
    page = f.read()
    
# outputs results which  are embedded within the selected html
    str_results = str(results)
    
    print(page.format(output = str_results))

"""
#*************************************************************************
def print_tempate(result):
    selects which html template to embed the output data into

    Input:  results       --- a string
    
    Return: None  --- Prints a webpage 
                             

    10.05.18  Original   By: ORS
"""



def print_template(results):
    # html page that acts as a wrapper around results
    file ="template.html"
    print_page(file,results)

"""
#*************************************************************************
def data_processing(data):
    processes the data from web page forms into one form of output

    Input:  data      --- a dictionary containing cgi data
            
    Return: contents  --- a dictionary containing processed data
                             

    10.05.18  Original   By: ORS
"""    



""" The purpose of data_processing is to take the dictionary from
cgifeildstorage to dict and to check that both the keys and values are present.
It then checks the name of the dictionary and creates a dictionary with type,
pre_set, name and enzyme.

it also turns the key:valuse 'gene':'gene1' into 'type':1,'name':'gene1
which is neccisary to fit our api"""

def data_processing(data): # directs the output from forms in homepage.html     
    
    # assigns variables to values type,pre_set,name, enzyme from form
    # form.getvalue("name") stores a dictionary containing the type and name


    if "name" in data:            
        query_name = data["name"]
        
    if 'type' in data:
        query_type = data["type"]
        query_type = int(query_type)
        

# changes the data type from a string "int" to an int
#    elif "type" in data:
#        query_type = data["type"]
        
#        if type(query_type) == str:
#            query_type = int(query_type)


# changes the pre_set form types from their names to the number based api 0,1,2,3
    elif "gene" in data:
        query_name = data["gene"]
        query_type = 0
        
    elif "protein" in data:
        query_name = data["protein"]
        query_type = 1
        
    elif "acession" in data:
        query_name = data["acession"]
        query_type = 2
        
    elif "location" in data:
        query_name = data["location"]
        query_type = 3

# This creates empy values if none are found
    else:
        query_name =""
        query_type =""

        
    if "pre_set" in data:
        query_pre_set =data["pre_set"]
        
    else:
        query_pre_set = False

    if "enzyme" in data:
        query_enzyme =data["enzyme"]
        
    else:
        query_enzyme = ""

# final format for the front to middle API
    contents = {"type":query_type,"pre_set": query_pre_set,"name" : query_name,"enzyme": query_enzyme}



######################################################################
####                      Change return(query_example) to return( contents)
####################################################################
    return contents


"""
#*************************************************************************
def cgi_field_storage_to_dict(fieldStorage ):
    processes the data from web page forms into one form of output

    Input:  data      --- a dictionary containing cgi data
            
    Return: contents  --- a dictionary containing processed data
                             

    10.05.18  Original   By: ORS
""" 

""" The purpose of this function is to check the output from the middle layer
and check if there is a type = 4. A type 4 indicating that the name or protein
has multiple entires in the database. This will determine where a normal results
screen or a 'select_duplicate' is created """



def cgi_field_storage_to_dict( fieldStorage ):
    
    #Get a plain dictionary, rather than the '.value' system used by the cgi module
    params = {}
    
    for key in fieldStorage.keys():
        params[ key ] = fieldStorage[ key ].value
        
    return params

"""
###########################################

def create_codon_table(codon_list):

    takes the nested lists that makes up the 

    Input:  data      --- nested dictionaries/lists containing proccessed data
            
    Return: final_str  --- a string to be inserted into a HTML template to generate webpage
                             

    10.05.18  Original   By: ORS

"""
def create_codon_table(codon_lists):

    
    
    dna_list = codon_lists


    inner_table = ""
    inner_table += "<table>"
    inner_table += "<tr>"
    
    # inputs the headers for each column
    inner_table += "<th>Codon</th><th>%</th><th>Ratio</th><th>Amino acid</th>"
    inner_table += "<th>Codon</th><th>%</th><th>Ratio</th><th>Amino acid</th>"
    inner_table += "<th>Codon</th><th>%</th><th>Ratio</th><th>Amino acid</th>"    
    inner_table += "<th>Codon</th><th>%</th><th>Ratio</th><th>Amino acid</th>"
    
    inner_table+="</tr>"
    for i in dna_list:
       inner_table = inner_table + "<tr>"
   
       for key in dna_list[i]:
           the_data = dna_list[i][key]
           inner_table = inner_table + "<td>" + key +"</td>"
       
           for j in the_data:
               inner_table = inner_table + "<td>" + str(j) +"</td>"
           

       inner_table = inner_table + "</tr>"
    inner_table += "</table>"
   
    return inner_table

"""
#***************************************************************

def print_formating(processed_middle_data):

    processes the input to be presented on a html page in a ordered manner

    Input:  data      --- nested dictionaries/lists containing proccessed data
            
    Return: final_str  --- a string to be inserted into a HTML template to generate webpage
                             

    10.05.18  Original   By: ORS


as the data set i got back from the middle level is not properly formated i cant print it to web page.
This is an example of the correctly formated data as dummy data
"""

def print_formating(processed_middle_data):
    data = processed_middle_data
    final_str = ""

    # if it is a type 5 which is just a dict 
    if "type" in data:
        if data["type"] == 5:
            final_str = final_str + "This return type means that no entry was found in our database. This may be because of an error in the genbank file, please try again <br>"
            for x in data:
                final_str = final_str + x + " : " +str(data[x]) +"<br>"
                return final_str
            
    # checks for a nested dict key value 'additional_data. indicates type 4 data
    elif any( 'additional_data' in d for d in data):
        final_str += final_str + "This return type means that duplicate entires were found, please select one <br> <br><br>"
        for dicts in data:
            temp_dict = str(dicts["additional_data"])
            final_str += temp_dict + "<br><br>"
        return final_str

    elif'associated_genes' in data:
        final_str += "This return type is for a Cromosomal location <br> Here accociated genes, proteins, protein IDs, Primary accesion numbers and Chromosomal Locations <br><br>" 
        final_str += data["searched_type"] + " " + data["searched_name"] +"<br>"
        
        final_str += "associated genes :" + "<br>" +  str(data["associated_genes"]) + "<br><br>"
        final_str += "associated proteins :" + "<br>" +  str(data["associated_protein"]) + "<br><br>"
        final_str += "associated primary Accesion numbers :" + "<br>"+  str(data["associated_accession"]) + "<br><br>"
        final_str += "associated cromosomal location :" + "<br>" +  str(data["associated_location"]) + "<br><br>"
        return final_str

    # This is check if a nested key exists which is found only in type012 data
    elif any( 'searched_name' in d for d in data):
        final_str += "This return type is for a gene, protein or accesion number <br> Here is the relevent data <br><br>" 
        temp_dict = data[0]
        for x in temp_dict:
            final_str += x + " : " + temp_dict[x] + "<br><br>"
        final_str += " This is the table for chromosomal codon usage<br>"
        temp_dict = create_codon_table(data[1])
        final_str += temp_dict + "<br><br>"

        final_str += " This is the table for cds codon usage<br>"        
        temp_dict = create_codon_table(data[2])
        final_str += temp_dict
        return final_str
    else:
        return ("Nothing found")
            
    




# takes middle layer output and prints to html template 
def front_to_middle():

    # collects the form data from webpage
    form_data = cgi_field_storage_to_dict(cgi.FieldStorage())
    
    # organises form data in a uniform manner
    processed_web_data = data_processing(form_data)

    # invokes middle layer and passes form data
    middle_query = middle_to_db(processed_web_data)

    # determines types and processes data
    processed_middle_data = determine_type_of_middle_output(middle_query)
       
    # modifies data for printing to html page 
    formatted_data = print_formating(processed_middle_data)


    #True ooutput
    print_template(formatted_data)
    


front_to_middle()







