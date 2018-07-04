#!/usr/bin/env python3

"""
Date: 01.05.18
Program: Tools
Author: Elena S. Alvarez Ortega
------------------------------------------
General information: A class defined as "Tools" which will retrieve information
                     depending on the query the user does.

"""

# ----------------------------------------
#   Class applied for general tools
# ----------------------------------------

class Tools:
    # -------------------
    #   Variables
    # -------------------
    counter = 0
    list_start = []
    list_end = []


    """ This first method creates a html tag where gives an specific color to the background of a text, in this
     casi it will be called within the method 'highlight'. It has been defined as a private method as its use it will
     be exclusive for 'highlight' method."""

    def __html_tag_highlight(self, a=0, b=0, string=""):

        final_result = ""
        initial_tag = "<span style=""background-color:#0081d5"">"
        ending_tag = "</span>"

        final_result += string[0:a - 1]
        final_result += initial_tag
        final_result += string[a - 1:b]
        final_result += ending_tag
        final_result += string[b:string.__len__()-1]

        return final_result

    """ In this method named 'ignore_digits' digits are being deleted from the string,
    with the function 'isdigit' already provided for Python, which one allows to check if that
    string is a digit or not, and if it is not a digit, then, do not take it under consideration
    and not include it in the new string created. """

    def __ignore_digits(self, string=""):

        initial_string = ""
        self.counter

        while self.counter < string.__len__():

            if not string[self.counter].isdigit() or string[self.counter] == " ":
                if self.counter == 1:
                    self.counter += 1
                else:
                    initial_string += string[self.counter]
                    self.counter += 1
            else:
                self.counter += 1

        return initial_string

    """This method defined as 'line_break' is deleting any line break at the end of every string
    that presents an string with '\r\n' at the end, giving a final outpus with any line break in it"""

    def __line_break (self, string=""):

        initial_string = ""
        self.counter = 0

        while self.counter < string.__len__():

            if string[self.counter] != '\r' and string[self.counter] != '\n':
                initial_string += string[self.counter]
                self.counter += 1
            else:
                self.counter += 1


        return initial_string

    """ The next method called 'delete_spaces' what is being defined is that present spaces
    from the string created in the previous method will be eliminated. """

    def __delete_spaces(self, string_nodigit=""):

        self.counter = 0
        new_str = ""

        while self.counter < string_nodigit.__len__():
            if string_nodigit[self.counter] == " ":
                self.counter += 1
            else:
                new_str += string_nodigit[self.counter]
                self.counter += 1

        return new_str

    """ The method named 'locus_seq_modified' is a easy method to call to where some of the previous methods before 
    have been call in it, as the output needed is the one received by the variable 'Locus_seq' from the database 
    but without digit,spaces and breaklines. """

    def locus_seq_modified(self, Locus_seq=""):

        locus_seq_obtained = self.__delete_spaces(self.__line_break(self.__ignore_digits(Locus_seq)))

        return locus_seq_obtained

    """ In the next method it is being taking under consideration the range of the CDS and then,
     creating two strings, one for starting range and one for ending range, making sure it is taking
     the digits under consideration. """


    def __indexing(self, indexes=""):

        self.counter = 0
        rang = indexes.split(",")
        starting_string = ""
        ending_string = ""
        index1 = True
        index2 = True

        for x in rang:
            while self.counter < x.__len__():
                if index1:
                    if x[self.counter].isdigit():
                        starting_string += x[self.counter]
                        self.counter += 1
                    else:
                        index1 = False
                        self.counter += 2
                elif index2:
                    if x[self.counter].isdigit():
                        ending_string += x[self.counter]
                        self.counter += 1
                    else:
                        index2 = False
                else:
                    self.counter += 1

            index1 = True
            index2 = True
            self.counter = 0
            self.list_start.append(int(starting_string))
            self.list_end.append(int(ending_string))
            starting_string = ""
            ending_string = ""



    """ This next method defines with a highlight in html code where is the CDS in all the whole
    sequence. """

    def hightlight(self, indexes, locus_seq):

        counter = 0
        data_str = ""
        cds_seq = ""
        x = 0
        index_control = 44  # This number 44 is related to the html_tag created in the first method, because
                            # in every new index added there is that shift in the code. It does not have ""
                            # underconsideration.

        self.__indexing(indexes)
        data_str = self.__delete_spaces(self.__line_break(self.__ignore_digits(locus_seq)))
        cds_seq = data_str
        tag_counter = 0


        while self.list_start.__len__() > counter:
            cds_seq = self.__html_tag_highlight(self.list_start[counter] + (index_control * counter), self.list_end[counter] + (index_control * counter), cds_seq)

            counter += 1

        return cds_seq.upper()


    """ The functionaility of this method returns 'codon' variable in groups of 3 characters, anytime the 'whole_seq'
    it is divisible by 3. """

    def __cluster(self, whole_seq=""):
        codon = ""
        string = ""
        if whole_seq.__len__() % 3 == 0:
            for x in whole_seq:
                string += x
                if string.__len__() % 3 == 0:
                    codon += string + " "
                    string = ""
        else:
            print("Whole sequence not divisible by three.")

        return self.__remove_codon_stop(codon.upper())

    """ This 'alignment' method creates a dictionary where every 3 characters belonging to the variable 'codon' are
    matched with every single aminoacid from 'translation' string, being 'codon' the key and 'translation_str'
    the value. """

    def alignment(self, whole_seq="", translation=""):

        codon_list = self.__cluster(self.__cds_to_rna(whole_seq)).split(" ")
        translation_list = []
        codon_trans_list = []


        for x in translation:
            translation_list.append(x)

        codon_trans_list.append(codon_list)
        codon_trans_list.append(translation)

        return codon_trans_list

    """ 'alignment_2' method introduces the string corresponding to 'whole_seq' and 'translation' in an empty dictionary
    being 'whole_seq' the key and 'translation' the value. """

    def alignment_2 (self, whole_seq = "", translation = ""):
        aligned_dictionary= {}

        aligned_dictionary["whole_seq"] = whole_seq
        aligned_dictionary["translation"] = translation

        return aligned_dictionary

    """ The main function of '__remove_codon_stop' eliminates the last 3 characters from the string plus
     the empty spaces."""

    def __remove_codon_stop(self, codon=""):

        return codon[0:codon.__len__() - 5]

    """ This method is creating a list of lists which each of it contains the start positions of the restriction enzyme 
    and the end position, respectively."""

    def index_restriction_enzymes (self, db_output_re = []):

        start_index = []
        end_index = []
        index_list = []

        for x in db_output_re:

            if 'start_position' in x:
                start_index.append(x['start_position'])
                end_index.append(x['end_position'])

        index_list.append(start_index)
        index_list.append(end_index)
        return index_list

    """ With 'colour_text_html_tag' method the string where it matches with the rang between the 'start' and the 'end' 
    position will be displayed with a distinctive colour into the html."""

    def colour_text_html_tag (self, indexes_res="", locus_seq = ""):

        start = indexes_res[0]
        end = indexes_res[1]

        counter = 0
        new_index_counter = 0
        counter1 = 0
        counter2 = 0
        final_result = ""

        while locus_seq.__len__() > counter:

            if locus_seq[counter] == '<':
                while locus_seq[counter] != '>':
                    if locus_seq[counter + 1] == '>':
                        new_index_counter += 1
                    new_index_counter += 1
                    final_result += locus_seq[counter]
                    counter += 1

            if counter1 < start.__len__():
                if ((start[counter1] + new_index_counter) -1) == counter:
                    final_result += "<font color=red>"
                    counter1 += 1

            if counter2 < end.__len__():
                if end[counter2] + new_index_counter == counter:
                    final_result += "</font>"
                    counter2 += 1
            final_result += locus_seq[counter]
            counter += 1

        return final_result

    """ This method displays as a list of list the output received from database as a list of dictionaries. """

    def codon_usage_chromosome (self, db_output_codon_usage):

        list_codons = []
        list_freq_100 = []
        list_ratio_aa = []
        list_amino_acid = []
        new_list = []

        for x in db_output_codon_usage:
            if 'codon' in x:
                list_codons.append(x['codon'])
                list_freq_100.append(x['frequency_100'])
                list_ratio_aa.append(x['ratio_aa'])
                list_amino_acid.append(x['amino_acid'])

        new_list.append(list_codons)
        new_list.append(list_freq_100)
        new_list.append(list_ratio_aa)
        new_list.append(list_amino_acid)

        return new_list

    """ This method changes the character 't' to an 'u' in the string received. """

    def __cds_to_rna (self, whole_seq =""):

        whole_seq_rna = whole_seq.replace("t", "u")
        return whole_seq_rna

    """ Calculations regardind to the frequency of the codon in the sequence and it RCSU are provided through
    this method. """

    def codon_ratio(self, seq_aligned, db_output_codon_usage):

        amino_acid=[]
        codon=[]
        data1 = seq_aligned[1]
        data2 = seq_aligned[0]
        exists = False
        codon_dict={}
        num = 0
        total_codon = {}
        initial_counter = 0
        Nlen = seq_aligned[0].__len__() + 1
        result_avg_codon = {}
        aa_codon = []
        rcsu = {}
        unique_valor_aa = {}
        new_codon_list = []

    # ******************************************************
    # List of amino acids with single letter added.
    # ******************************************************

        aa_single_letter = []
        aa_single_letter.append(["phe", "F"])
        aa_single_letter.append(["leu", "L"])
        aa_single_letter.append(["ile", "I"])
        aa_single_letter.append(["met", "M"])
        aa_single_letter.append(["val", "V"])
        aa_single_letter.append(["ser", "S"])
        aa_single_letter.append(["pro", "P"])
        aa_single_letter.append(["thr", "T"])
        aa_single_letter.append(["ala", "A"])
        aa_single_letter.append(["tyr", "Y"])
        aa_single_letter.append(["his", "H"])
        aa_single_letter.append(["gln", "Q"])
        aa_single_letter.append(["asn", "N"])
        aa_single_letter.append(["lys", "K"])
        aa_single_letter.append(["asp", "D"])
        aa_single_letter.append(["glu", "E"])
        aa_single_letter.append(["cys", "C"])
        aa_single_letter.append(["trp", "W"])
        aa_single_letter.append(["arg", "R"])
        aa_single_letter.append(["gly", "G"])
        aa_single_letter.append(["ter", "*"])
        aa_single_letter.append(["phe", "F"])
        aa_single_letter.append(["leu", "L"])
        aa_single_letter.append(["ile", "I"])
        aa_single_letter.append(["met", "M"])
        aa_single_letter.append(["val", "V"])
        aa_single_letter.append(["ser", "S"])
        aa_single_letter.append(["pro", "P"])
        aa_single_letter.append(["thr", "T"])
        aa_single_letter.append(["ala", "A"])
        aa_single_letter.append(["tyr", "Y"])
        aa_single_letter.append(["his", "H"])
        aa_single_letter.append(["gln", "Q"])
        aa_single_letter.append(["asn", "N"])
        aa_single_letter.append(["lys", "K"])
        aa_single_letter.append(["asp", "D"])
        aa_single_letter.append(["glu", "E"])
        aa_single_letter.append(["cys", "C"])
        aa_single_letter.append(["trp", "W"])
        aa_single_letter.append(["arg", "R"])
        aa_single_letter.append(["gly", "G"])
        aa_single_letter.append(["ter", "*"])

        for x in db_output_codon_usage:
            for y  in aa_single_letter:
                if x["amino_acid"] == y[0]:
                    aa_codon.append([y[1], x["codon"]])



    # ******************************************************
    # Exclussive amino acids in the sequence as a list.
    # ******************************************************

        for x in data1:
            for v in amino_acid:
                if x == v:
                    exists = True
                    break

            if exists == False:
                amino_acid.append(x)
            else:
                exists = False
    # ******************************************************

    # ******************************************************
    # Exclussive codons in the sequence as a list.
    # ******************************************************
        for x in data2:
            for v in codon:
                if x == v:
                    exists = True
                    break

            if exists == False:
                codon.append(x)
            else:
                exists = False

    # ******************************************************

        for x in amino_acid:
            for q in aa_codon:
                if q[0] == x:
                    new_codon_list.append(q[1])
            unique_valor_aa[x] = new_codon_list
            new_codon_list = []


    # ******************************************************
    # Joined data related to its amino acid.
    # ******************************************************

        for x in amino_acid:
            codon_dict[x] = self.join(x, seq_aligned)

        for k in codon:
            for s in data2:
                if k == s:
                    initial_counter += 1
            total_codon[k] = initial_counter
            initial_counter = 0

    # ******************************************************
    # Average frequency of each codon for that sequence
    # ******************************************************

        for u in codon:
            result_avg_codon[u] = "{0:.2f}".format(((total_codon[u]/Nlen)*100))

    # ******************************************************
    # Ratio of each codon related to its amino_acid
    # ******************************************************
        counter = 0

        for x in amino_acid:
            for u in codon:
                for f in seq_aligned[1]:
                    if x == f:
                        counter += 1

                result1 = unique_valor_aa[x].__len__()
                result2 = total_codon[u]
                result3 = Nlen

                rscu = "{0:.2f}".format(((result2/result3)/(1/result1)*result2))

        return [result_avg_codon, rscu]



    """ Creates a list whith the codons and its amino acid through all the sequence. """

    def join(self, amino_acid, seq_aligned):

        list = []
        cont = 0

        for x in seq_aligned[1]:
            if x in amino_acid:
                list.append([seq_aligned[0][cont], seq_aligned[1][cont]])

            cont += 1


        return list
