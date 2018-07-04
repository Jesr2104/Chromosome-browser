#!/usr/bin/env python3

"""
Program:    DB_API_functions
File:       DB_API_functions.py

Version:    V1.0
Date:       05.04.18
Function:   API to access chromosome database and retrieve information requected
            by the user of the webpage.

Author:     Alina Ozuna
            
--------------------------------------------------------------------------

This program was produced as a part of Biocomputing II module assessment.

--------------------------------------------------------------------------
Description:
============
The three functions retrieve three types of information from the database -
general gene/protein/locus information, codon usage for the whole chromosome,
and restriction sites found in locus of interest.

--------------------------------------------------------------------------
Usage:
======
The general information and restriction site functions recognise the following
input format:

General information query:
{"type" : 1,"pre_set": True, "name" : "ACSF3", "enzyme": ""}

Restriction site query:
If the enzyme is pre-calculated
{"type" : 2,"pre_set": True, "name" : "AB001099", "enzyme" : 'EcoRI'}
or in the enzyme is not pre-set and the user provides its recognition sequence
{"type" : 2,"pre_set": True, "name" :'AB001099', "enzyme": "ATTGCC"}

Type 0 = gene identifier 
Type 1 = product name
Type 2 = Genbank accession number
Type 3 = cytogenetic location (showing a list of loci)
Type 4 = duplicate; it is called if the gene or product name appears more than
once as it will be determined by the middle layer before sending the query
to the database. Duplicate query will also provide product ID as the element
to seqrch with, since they are designed to always be unique.
{"type" : 4,"pre_set": True, "name" :'AB001099', "enzyme": "hba1", "product_id":"cab1234"}

The codon usage for the whole chromosome is provided together with the general
information, hence the functions are used together. The decision to make two
separate functions to ensure usage convenience and readability of the output.

--------------------------------------------------------------------------
Revision History:
=================
V1.0   05.04.18   Original   By: AO
"""

#*************************************************************************
# Import library

import pymysql.cursors

#*************************************************************************


def gen_info(middle_db_input):

    """Obtain the information on gene/protein/locus/cytogenic location required
    by the front and middle layer from the database. The output information
    presented in a form of a list of dictionaries with the original database
    column name as key and corresponding information as a value.

    Input:  middle_db_input      --- A dictionary in the given format containing
                                the information requested by the webpage user and
                                confirmed by the middle layer.
    Return: db_middle_output     --- A list of dictionaries with information
                                corresponding to a particular query type:
                                - Queries with gene identifier or product name
                                return all information for the corresponding
                                CDS and locus (with its primary accession
                                number) information.
                                - Queries with locus accession number return all
                                information for that particular locus and data on
                                all CDS regions that might be present in that locus.
                                - Queries with cytogenic location return only the
                                accession numbera of loci, all gene identifier and
                                product names for loci and CDS that share that
                                particular location.

    05.04.18  Original   By: AO
    """

    query = ""
    query_add = ""
    # Queries will be build from several part: "select" statement, followed by
    # what should be selected and what tables to select from. The last part is
    # extended using the information from the webpage request.

    # Two types of query body:
    # first to be used for selection by any accession number;
    query_t0 = "from locus l, cds c, accession a where a.locus_id=l.id and c.locus_id=l.id and "
    # second to be used in all other queries, as only primary (latest) accession
    # number will be displayed on the webpage.
    query_t1 = query_t0 + "a.latest_version='T' and "

    # Columns to be selected from the respective tables.
    locus = "l.whole_seq as locus_sequence, l.chr_location, l.locus_name, l.chr_name"
    cds = "c.gene_name, c.product_name, c.product_id, c.seq_location, c.whole_seq, c.translation, c.complement"
    accession = "a.accession_num"
    # Columns to be selected, when the user selects a cytogenic location.
    cyt_loc_cds = "c.gene_name, c.product_name, c.product_id"
    cyt_loc = "l.chr_location"
    
    # Query construction 
    search = middle_db_input["name"]
    # Type 0 (gene identifier) and 1 (product name) contain information on a
    # single element, hence no information repeats would be present in the
    # output; therefore just one query is generated
    if middle_db_input["type"]==0:
        query = "select " + accession + ", " + locus + ", " + cds + " " + query_t1 + "c.gene_name" + "=" + "'"+search+"'"
    elif middle_db_input["type"]==1:
        query = "select " + accession + ", " + locus + ", " + cds + " " + query_t1 + "c.product_name" + "=" + "'"+search+"'"
    # Type 2 (locus accession number) and 3 (cytogenic location) could have
    # multiple elements - multiple CDS or multiple loci and CDS, respetively).
    # Using one query would lead to information repeats. Using two queries 
    # avoids unnecesary repetitions.
    elif middle_db_input["type"]==2:
        query = "select " + locus + " " + query_t0 + "a.accession_num" + "=" + "'"+search+"'"
        query_add = "select " + cds + " " + query_t0 + "a.accession_num" + "=" + "'"+search+"'"
    elif middle_db_input["type"]==3:
        query = "select " + cyt_loc_cds + " " + query_t1+ "l.chr_location" + " like " + "'"+search+"%"+"'"
        query_add = "select " + accession + ", " + cyt_loc + " " + query_t1+ "l.chr_location" + " like " + "'"+search+"%"+"'"
    elif middle_db_input["type"]==4:
        search2 = middle_db_input["product_id"]
        query = "select " + accession + ", " + locus + ", " + cds + " " + query_t1 + "c.product_id" + "=" + "'"+search2+"'"
    

    db = pymysql.connect(db='0a002', user='0a002', passwd='0a002', host='hope', port=3306, cursorclass = pymysql.cursors.DictCursor)
    
    # Creating output from cursors depending on the query type.
    db_middle_output = [middle_db_input]
    if middle_db_input["type"]==0 or middle_db_input["type"]==1:
        cursor = db.cursor()
        q = cursor.execute(query)
        data = cursor.fetchall()
        db_middle_output += data
    elif middle_db_input["type"]==2 or middle_db_input["type"]==3:
        cursor1 = db.cursor()
        cursor2 = db.cursor()
        q1 = cursor1.execute(query)
        q2 = cursor2.execute(query_add)
        unit1 = cursor1.fetchall()
        unit2 = cursor2.fetchall()
        db_middle_output =db_middle_output + list(unit1) + list(unit2)
        # output includes the input dictionary for convenience of the front end.
    elif middle_db_input["type"]==4:
        cursor = db.cursor()
        q = cursor.execute(query)
        data = cursor.fetchall()
        db_middle_output += data
        

    return(db_middle_output)


#*************************************************************************


def chr_codon_usage():

    """Obtain the information on the codon usage within the whole chromosome
    from the database. This function should be used when gene/protein
    information is required, as it complements the information on the web page

    Return: db_middle_output     --- A list of dictionaries with the original
                                database column name as key and corresponding
                                information as a value. Each dictionary contains
                                data for a particular codon.

    05.04.18  Original   By: AO
    """
    # Selecting everything from the codon usage table for further processing.
    query = "select * from codon_usage"

    db = pymysql.connect(db='0a002', user='0a002', passwd='0a002', host='hope', port=3306, cursorclass = pymysql.cursors.DictCursor)
    
    cursor = db.cursor()
    q = cursor.execute(query)


    db_middle_output=cursor.fetchall()
    return(db_middle_output)


#*************************************************************************

def restriction_sites(middle_db_input):

    """Obtain the information on the restriction site location in a particular
    locus if the enzyme information is present in the front end request. The
    output information presented in a form of a list of dictionaries with the
    original database column name as key and corresponding information as a
    value. 

    Input:  middle_db_input      --- A dictionary in the given format containing
                                the information of the target gene/protein/locus
                                ancd target enzyme.
    Return: db_middle_output     --- A list of dictionaries with information
                                corresponding to the request:
                                - If the restriction enzyme cut sites are pre-
                                calculated, all corresponding data for the enzyme
                                of interest will be returned.
                                - If the enzyme is not in the database and the
                                recognition site is given, the function returns
                                the whole locus sequence for the middle layer
                                to calculate the restriction site location.

    05.04.18  Original   By: AO
    """

    # Two types of queries to retrieve the restriction site information and
    # locus sequence separately prevents information repeats.
    # Queries if the user is interested in the gene or protein.
    query1 = "select s.start_position, s.end_position, e.recogn_seq from locus l, restriction_enzyme e, restriction_sites s, cds c where c.locus_id=l.id and s.locus_id=l.id and s.re_id=e.id and "
    query2 = "select c.gene_name, c.product_name, c.seq_location, l.whole_seq from locus l, cds c where c.locus_id=l.id and "
    
    # Queries if the user is searching using the locus accession number.
    query3 = "select s.start_position, s.end_position, e.recogn_seq from locus l, restriction_enzyme e, restriction_sites s, accession a where a.locus_id=l.id and s.locus_id=l.id and s.re_id=e.id and "
    query4 = "select l.whole_seq from locus l, accession a where a.locus_id=l.id and "
    query5 = "select c.gene_name, c.product_name, c.seq_location from locus l, cds c, accession a where a.locus_id=l.id and c.locus_id=l.id and "


    # A list of enzymes present in the database.
    preset = ["ecori", "bamhi", "bsumi"]
    search = middle_db_input["name"]
    enzyme = middle_db_input["enzyme"]

    db = pymysql.connect(db='0a002', user='0a002', passwd='0a002', host='hope', port=3306, cursorclass = pymysql.cursors.DictCursor)
    
    # If the user searches for the restrictions sites produced by a preset enzyme:
    if middle_db_input["enzyme"] in preset:
        # The function works, if the user searches with the gene identifier,
        # protein name or locus accession number. Cytogenetic location can be
        # shared by many loci, therefore it cannot be used to avoid confusion.
        if middle_db_input["type"]==0:
            query_x = query1 + "c.gene_name =" + "'"+search+"'" + "and e.name = " + "'"+enzyme+"'"
            query_y = query2 + "c.gene_name =" + "'"+search+"'"
        elif middle_db_input["type"]==1:
            query_x = query1 + "c.product_name =" + "'"+search+"'" + "and e.name = " + "'"+enzyme+"'"
            query_y = query2 + "c.product_name =" + "'"+search+"'"
        elif middle_db_input["type"]==2:
            query_x = query3 + "a.accession_num =" + "'"+search+"'" + "and e.name = " + "'"+enzyme+"'"
            query_y = query4 + "a.accession_num =" + "'"+search+"'"
            query_z = query5 + "a.accession_num =" + "'"+search+"'"
        elif middle_db_input["type"]==4:
            search2 = middle_db_input["product_id"]
            query_x = query1 + "c.product_id =" + "'"+search2+"'" + "and e.name = " + "'"+enzyme+"'"
            query_y = query2 + "c.product_id =" + "'"+search2+"'"

        cursor1 = db.cursor()
        cursor2 = db.cursor()
    
        q_x = cursor1.execute(query_x)
        q_y = cursor2.execute(query_y)

        r_sites = cursor1.fetchall()
        sequence = cursor2.fetchall()

        if middle_db_input["type"]==0 or middle_db_input["type"]==1:
            db_middle_output = [middle_db_input] + list(r_sites) + list(sequence)
        if middle_db_input["type"]==2:
            cursor3 = db.cursor()
            q_z = cursor3.execute(query_z)
            cds = cursor3.fetchall()
            db_middle_output = [middle_db_input] + list(r_sites) + list(sequence) + list(cds)
        if middle_db_input["type"]==4:
            db_middle_output = [middle_db_input] + list(r_sites) + list(sequence)
            
        return(db_middle_output)
        
    # If the enzyme is not present in the database, the query will return only
    # the sequence for a corresponding locus for the middle layer to
    # calculate the  restriction sites, given the recognition site.
    elif middle_db_input["enzyme"] not in preset:
        if middle_db_input["enzyme"]=="":
            return(middle_db_input)
        elif middle_db_input["enzyme"]!="":
            if middle_db_input["type"]==0:
                query = query2 + "c.gene_name =" + "'"+search+"'"
            elif middle_db_input["type"]==1:
                query = query2 + "c.product_name =" + "'"+search+"'"
            elif middle_db_input["type"]==2:
                query = query4 + "a.accession_num =" + "'"+search+"'"
                query_extra = query5 + "a.accession_num =" + "'"+search+"'"
            elif middle_db_input["type"]==4:
                search2 = middle_db_input["product_id"]
                query = query2 + "c.product_id =" + "'"+search2+"'"

            cursor = db.cursor()
            
            q = cursor.execute(query)
            
            sequence = cursor.fetchall()

            if middle_db_input["type"]==0 or middle_db_input["type"]==1 or middle_db_input["type"]==4:
                db_middle_output = [middle_db_input] + sequence
            if middle_db_input["type"]==2:
                cursor_e = db.cursor()
                q_e = cursor_e.execute(query_extra)
                cds = cursor_e.fetchall()
                db_middle_output = [middle_db_input] + sequence + cds
            

            return(db_middle_output)
            

    
        


