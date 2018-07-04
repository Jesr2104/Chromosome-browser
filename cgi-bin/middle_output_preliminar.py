#!/usr/bin/env python3

"""
Date: 01.05.18
Program: middle_layer_module
Author: Elena S. Alvarez Ortega
------------------------------------------
General information: A main function where it will return an output of a dictionary of
                     dictionaries named 'middle_output' regarding which statements
                     accomplish.
"""

# ----------------------------------------
#   Import
# ----------------------------------------

from DB_API import gen_info
from DB_API import chr_codon_usage
from DB_API import restriction_sites
from db_contents_for_middle_layer import checker
from Tools import Tools

#----------------------------------------
#   Function statement
#----------------------------------------
""" Main function called 'middle_to_db' will check first about duplicates or if the name matches 
in the database. After it, depending on the query will return specific information, but there is 
some general data that will be always returned as an output from middle layer to front layer.
"""

def middle_to_db(front_middle_input):

    new_dictionary = {}
    middle_output = {}
    middle_output_q3 = {}
    tools_fun = Tools()
    db_query = {}

    if front_middle_input["type"]==4:
        db_query = front_middle_input
        
    else:
        check_front_middle_input = checker(front_middle_input)
        check_list = []
        if isinstance(check_front_middle_input, list)==False:
            check_list = [check_front_middle_input]
        else:
            check_list = check_front_middle_input
        check_first_element = check_list[0]
        
        if check_first_element["type"]==0 or check_first_element["type"]==1 or check_first_element["type"]==2 or check_first_element["type"]==3:
            db_query = check_front_middle_input
            

        if check_first_element["type"]==4 or check_first_element["type"]==5:
            
            return(check_front_middle_input)



    db_output = []
    db_output_codons = []
    db_output_re = []

    db_output = gen_info(db_query)
    db_output_codons = chr_codon_usage()

    if db_query["enzyme"]!="":
        db_output_re = restriction_sites(db_query)



    if db_query["type"]==0 or db_query["type"]==1 or db_query["type"]==2 or db_query["type"]==4:
        for x in db_output:
            if "name" in x.keys():
                middle_output["output"]=x
            if "translation" in x.keys():
                middle_output["originaldata"]=x

                # cds translation alignment
                seq_location = x['seq_location']
                locus_seq = x['locus_sequence']
                highlight_tag = tools_fun.hightlight(seq_location, locus_seq)
                restr_list = []
                restriction_sites_tag = ""
                if db_query["enzyme"]!="":
                    for x in db_output_re:
                        if 'start_position' in x.keys():
                            restr_list.append(x)
                        else:
                            pass
                if len(restr_list)>0:
                    indexes_res = tools_fun.index_restriction_enzymes(db_output_re)
                    restriction_sites_tag = tools_fun.colour_text_html_tag(indexes_res, highlight_tag)
                else:
                    restriction_sites_tag = highlight_tag

                align_dict = {}
                align_dict["whole_seq"] = restriction_sites_tag
                middle_output["cds_translation_alignment"]=align_dict
                
        
        

    
        codon = {}
        for i in db_output_codons:
            codon[i['codon']] = [i['frequency_100'], i['ratio_aa'], i['amino_acid']]
        middle_output["chromosome_codon_usage"] = codon

        #cds codon usage
        # .....
        middle_output["cds_codon_usage"] = codon

        # restriction sites????

    if db_query["type"]==3:
        genes = []
        proteins = []
        protein_IDs = []
        accessions = []
        locations = []
        for x in db_output:
            if "name" in x.keys():
                middle_output["output"]=x
            if "gene_name" in x.keys():
                if len(x["gene_name"])>0:
                    genes.append(x["gene_name"])
                if len(x["product_name"])>0:
                    proteins.append(x["product_name"])
                if len(x["product_id"])>0:
                    protein_IDs.append(x["product_id"])
            if "accession_num" in x.keys():
                if len(x["accession_num"])>0:
                    accessions.append(x["accession_num"])
                if len(x["chr_location"])>0:
                    locations.append(x["chr_location"])
        middle_output["gene"] = genes
        middle_output["protein"] = proteins
        middle_output["protein_ID"] = protein_IDs
        middle_output["accession"] = accessions
        middle_output["location"] = locations

    return(middle_output)
            
    
    

