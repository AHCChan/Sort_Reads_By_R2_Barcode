HELP_DOC = """
SORT READS BY R2 BARCODE
(version 2.0)
by Angelo Chan

This is a program for sorting next-gen sequencing reads (FASTQ format) into one
of three pairs of output files, based on the presence, absence, or partial
presence, of a specified barcode at the start of the R2 reads.

Users may specify the mismatch threshold at which a read is considered to have a
complete match, or a partial match.

Users may specify whether to trim barcode sequences from the R1 read, the R2
read, both, or neither.

If the output file names are not specified by the user, output file names will
be automatically generated by the program.



USAGE:
    
    python27 Sort_by_r2_BCode.py <input_path_r1> <input_path_r2> <barcode>
            [-o <p1> <p2> <p3> <p4> <p5> <p6>] [-t <threshold_match>
            <threshold_partial>] [-r Y|N Y|N]



MANDATORY:
    
    input_path_r1
        
        The filepath of the input r1 file.
    
    input_path_r2
        
        The filepath of the input r2 file.
    
    barcode
        
        The nucleotide sequence being looked for in the r2 file.
        Ambiguous nucleotides accepted.OPTIONAL:

OPTIONAL:
    
    p1
        
        (DEFAULT path generation available)
        
        The filepath of the output file, for r1 reads, of pairs where the start
        of the r2 read contained a match for the barcode.
    
    p2
        
        (DEFAULT path generation available)
        
        The filepath of the output file, for r2 reads, of pairs where the start
        of the r2 read contained a match for the barcode.
    
    p3
        
        (DEFAULT path generation available)
        
        The filepath of the output file, for r1 reads, of pairs where the start
        of the r2 read contained a partial match for the barcode.
    
    p4
        
        (DEFAULT path generation available)
        
        The filepath of the output file, for r2 reads, of pairs where the start
        of the r2 read contained a partial match for the barcode.
    
    p5
        
        (DEFAULT path generation available)
        
        The filepath of the output file, for r1 reads, of pairs where the start
        of the r2 read did not contain a match for the barcode.
    
    p6
        
        (DEFAULT path generation available)
        
        The filepath of the output file, for r2 reads, of pairs where the start
        of the r2 read did not contain a match for the barcode.
    
    threshold_match
        
        (DEFAULT: 0)
        
        The maximum permissible number of mismatches, between the barcode and
        the first nucleotides of the r2 read, for a read pair to be considered
        as containing a match.
    
    threshold_partial
        
        (DEFAULT: 0)
        
        The maximum permissible number of mismatches, between the barcode and
        the first nucleotides of the r2 read, for a read pair to be considered
        as containing a partial match.
        
        If this is set to the same value as the threshold for a complete match,
        a pair of output files for partial matches will still be generated, but
        they will be empty.
    
    (-r)
        
        Y|N (1st)
            
            (DEFAULT: Y)
            
            Whether the barcodes or partial barcodes should be removed from the
            R2 output or not.
        
        Y|N (2nd)
            
            (DEFAULT: Y)
            
            Whether the barcodes or partial barcodes should be removed from the
            R1 output or not.



EXAMPLES EXPLANATION:
    
    1:
    Bare minimum use case. Only the mandatory inputs were supplied. Default
    settings were used where possible.
    
    2:
    More advanced use case with more options specified.

EXAMPLES:
    
    python27 Sort_by_r2_BCode.py reads_r1.fq reads_r2.fq CGTGAT
    
    python27 Sort_by_r2_BCode.py reads_r1.fq reads_r2.fq CGTGAT -o
            reads_match_r1.fq reads_match_r2.fq reads_partial_r1.fq
            reads_partial_r2.fq reads_absent_r1.fq reads_absent_r2.fq -t 1 2
            -r YES YES

USAGE:
    
    python27 Sort_by_r2_BCode.py <input_path_r1> <input_path_r2> <barcode>
            [-o <p1> <p2> <p3> <p4> <p5> <p6>] [-t <threshold_match>
            <threshold_partial>] [-r Y|N Y|N]
"""

NAME = "Sort_by_r2_BCode.py"



# Configurations ###############################################################

AUTORUN = True

WRITE_PREVENT = False # Completely prevent overwritting existing files
WRITE_CONFIRM = True # Check to confirm overwritting existing files

PRINT_ERRORS = True
PRINT_PROGRESS = True
PRINT_METRICS = True



# Minor Configurations #########################################################

FILEMOD__MATCH =   "__MATCH"
FILEMOD__PARTIAL = "__PARTIAL"
FILEMOD__ABSENT =  "__ABSENT"

CONFIG__N_SPAM_CUTOFF = 10 # If the first N nucleotides are all N on both reads,
#                            then regard the read as "unreadable"


# Defaults #####################################################################
"NOTE: altering these will not alter the values displayed in the HELP DOC"

DEFAULT__threshold_match = 0
DEFAULT__threshold_partial = 0

DEFAULT__remove_r1 = True
DEFAULT__remove_r2 = True



# Imported Modules #############################################################

import sys

import NSeq_Match



# Enums ########################################################################

class ALIGN:
    LEFT=1
    RIGHT=2



# Strings ######################################################################

STR__use_help = "\nUse the -h option for help:\n\t "\
        "python Sort_by_r2_BCode.py -h"

STR__no_inputs = "\nERROR: No inputs were given."
STR__insufficient_inputs = "\nERROR: Not enough inputs were given."

STR__IO_error_read = "\nERROR: Input file \"{f}\" does not exist or could not "\
        "be opened."
STR__IO_error_write_forbid = """
ERROR: You specified an output file which already exists and the administrator
for this program has forbidden all overwrites. Please specify a different
output file, move the currently existing file, or configure the default options
in Sort_by_r2_BCode.py."""
STR__IO_error_write_unable = """
ERROR: Unable to write to the specified output file "{f}\""""

STR__invalid_barcode = "\nERROR: Invalid nucleotide barcode: {s}"

STR__specify_6_arguments_for_outputs = """
ERROR: Please input 6 filepaths if you wish to specify output filepaths of your
choosing. Alternatively, you may use the default filepaths generated by this
program."""
STR__specify_2_arguments_for_thresholds = """
ERROR: Please input 2 arguments if you wish to specify cutoff thresholds for the
maximum permissible number of mismatches before a read pair is no longer
regarded as containing a perfect/partial match.
(DEFAULTS: {t1}, {t2}""".format(
        t1 = DEFAULT__threshold_match,
        t2 = DEFAULT__threshold_partial)
STR__specify_2_arguments_for_remove = """
ERROR: Please input 2 arguments if you wish to specify whether or not to remove
any complete or partial barcode matches from the sequences.
(DEFAULTS: {t1}, {t2}""".format(
        t1 = DEFAULT__remove_r1,
        t2 = DEFAULT__remove_r2)

STR__invalid_threshold = "\nERROR: Please specify a non-negative integer for "\
        "your cutoff thresholds."

STR__invalid_bool = "\nERROR: Please specify Yes/No. You specified:\n\t{s}"

STR__overwrite_confirm = "\nFile already exists:\n\t{f}\nDo you wish to "\
        "overwrite it? (y/n): "



STR__metrics_pairs =     "\nTotal Pairs:       {s}"
STR__metrics_usables =   "\nUsable Pairs:      {s} ( {p}% )"
STR__metrics_unreadables = "Unreadables Pairs: {s} ( {p}% )"
STR__metrics_matches =   "\nTotal Matches:     {s} ( {p1}% of usable, {p2}% "\
        "of total)"
STR__metrics_partials =    "Total Partials:    {s} ( {p1}% of usable, {p2}% "\
        "of total)"
STR__metrics_absents =     "Total Absents:     {s} ( {p1}% of usable, {p2}% "\
        "of total)"



STR__parsing_args = "\nParsing arguments..."

STR__sort_by_r2_bcode_begin = "\nRunning Sort_by_r2_BCode..."

STR__sort_by_r2_bcode_complete = "\nSorting successfully finished."



# Lists ########################################################################

LIST__help = ["-h", "-H", "-help", "-Help", "-HELP"]

LIST__yes = ["Y", "y", "YES", "Yes", "yes", "T", "t", "TRUE", "True", "true"]
LIST__no = ["N", "n", "NO", "No", "no", "F", "f", "FALSE", "False", "false"]



# Dictionaries #################################################################



# Resolve Variables ############################################################

SEQ__N_SPAM_SEQ = "N" * CONFIG__N_SPAM_CUTOFF



# File Processing Code #########################################################

def Sort_By_R2_Barcode(paths_in, paths_out, barcode, thresholds, removes):
    """
    Function which performs the FASTQ file sorting.
    
    @paths_in
            (list<str - filepath>[2])
            The filepaths of the r1 and r2 input files. 
    @paths_out
            (list<str - filepath>[6])
            The filepaths for the output files, in the following order:
                r1 reads of read pairs with a complete barcode
                r2 reads of read pairs with a complete barcode
                r1 reads of read pairs with a partial barcode
                r2 reads of read pairs with a partial barcode
                r1 reads of read pairs with no barcode
                r2 reads of read pairs with no barcode
    @barcode
            (str)
            The DNA sequence being looked for in the r2 reads.
    @thresholds
            (list<int>[2])
            The maximum permissible number of mismatches for an r2 read to be
            considered as containing a complete barcode, and the maximum
            permissible number of mismatches for an r2 read to be considered as
            containing a partial barcode.
    @removes
            (list<bool>[2])
            Whether or not to remove the R1 and R2 barcodes, if found.
            The first boolean refers to trimming the R1 sequence.
            The second boolean refers to trimming the R2 sequence.
    
    Return a value of 0 if the function runs successfully.
    
    Sort_By_R2_Barcode([str, str], [str, str, str, str, str, str], str, [int,
            int]) -> int
    """
    printP(STR__sort_by_r2_bcode_begin)

    # Unpack
    threshold_match, threshold_partial = thresholds
    remove_r1, remove_r2 = removes
    
    # Initialize File IO
    f1 = open(paths_in[0], "U")
    f2 = open(paths_in[1], "U")
    w1 = open(paths_out[0], "w")
    w2 = open(paths_out[1], "w")
    w3 = open(paths_out[2], "w")
    w4 = open(paths_out[3], "w")
    w5 = open(paths_out[4], "w")
    w6 = open(paths_out[5], "w")
    
    # Initialize Metrics
    count_total = 0
    count_NNN = 0
    count_match = 0
    count_partial = 0
    count_absent = 0
    
    # Preparatory Calculations
    length = len(barcode)
    complement = NSeq_Match.Get_Complement(barcode)
    
    # Main Loop
    r1_ID, r1_seq, r1_3rd, r1_qc = Parse_Read(f1)
    r2_ID, r2_seq, r2_3rd, r2_qc = Parse_Read(f2)

    while r1_seq and r2_seq:
        count_total += 1
        
        # Unreadable
        subseq1 = r1_seq[:CONFIG__N_SPAM_CUTOFF]
        subseq2 = r2_seq[:CONFIG__N_SPAM_CUTOFF]
        if SEQ__N_SPAM_SEQ == subseq1 == subseq2: count_NNN += 1
        
        else: # Not unreadable
            subseq = r2_seq[:length]
            mismatches = NSeq_Match.NSeq_Match(barcode, subseq)
            
            output_file_1 = None
            output_file_2 = None
            
            # Match
            if mismatches <= threshold_match:
                count_match += 1
                # Remove
                if remove_r1:
                    pos = NSeq_Match.Candidate_Match_Position__TAIL(r1_seq,
                            complement, threshold_match)
                    r1_seq = r1_seq[:pos]
                    r1_qc = r1_qc[:pos]
                if remove_r2:
                    r2_seq = r2_seq[length:]
                    r2_qc = r2_qc[length:]
                # Target
                output_file_1 = w1
                output_file_2 = w2
            
            # Partial
            elif mismatches <= threshold_partial:
                count_partial += 1
                # Remove
                if remove_r1:
                    pos = NSeq_Match.Candidate_Match_Position__TAIL(r1_seq,
                            complement, threshold_partial)
                    r1_seq = r1_seq[:pos]
                    r1_qc = r1_qc[:pos]
                if remove_r2:
                    r2_seq = r2_seq[length:]
                    r2_qc = r2_qc[length:]
                # Target
                output_file_1 = w3
                output_file_2 = w4
            
            # Absent
            else:
                count_absent += 1
                # Target
                output_file_1 = w5
                output_file_2 = w6
            
            # Build strings and write
            string1 = Create_Output(r1_ID, r1_seq, r1_3rd, r1_qc)
            string2 = Create_Output(r2_ID, r2_seq, r2_3rd, r2_qc)
            output_file_1.write(string1)
            output_file_2.write(string2)
        
        # Read next
        r1_ID, r1_seq, r1_3rd, r1_qc = Parse_Read(f1)
        r2_ID, r2_seq, r2_3rd, r2_qc = Parse_Read(f2)
    
    # Finish
    w6.close()
    w5.close()
    w4.close()
    w3.close()
    w2.close()
    w1.close()
    f2.close()
    f1.close()

    # Metrics Reporting
    count_usable = count_total - count_NNN
    
    strings = Ints_To_Aligned_Strings([count_total, count_usable, count_NNN,
            count_match, count_partial, count_absent], ALIGN.RIGHT)
    s_total, s_usable, s_NNN, s_match, s_partial, s_absent = strings
    
    p_usable, p_NNN, p2_match, p2_partial, p2_absent = Get_Percentage_Strings(
            [count_usable, count_NNN, count_match, count_partial, count_absent],
            count_total, 2, 6)
    p1_match, p1_partial, p1_absent = Get_Percentage_Strings([count_match,
            count_partial, count_absent], count_usable, 2, 6)
    
    printM(STR__metrics_pairs.format(s = s_total))
    printM(STR__metrics_usables.format(s = s_usable, p = p_usable))
    printM(STR__metrics_unreadables.format(s = s_NNN, p = p_NNN))
    printM(STR__metrics_matches.format(s = s_match, p1 = p1_match,
            p2 = p2_match))
    printM(STR__metrics_partials.format(s = s_partial, p1 = p1_partial,
            p2 = p2_partial))
    printM(STR__metrics_absents.format(s = s_absent, p1 = p1_absent,
            p2 = p2_absent))
    
    # Exit
    printP(STR__sort_by_r2_bcode_complete)
    return 0



def Parse_Read(file_):
    """
    Parse an entry from a FASTQ file. Return a list containing the read's ID,
    sequence, placeholder line, and QC scores.
    
    Return an empty list if there are no reads left.
    
    Parse_Read(file) -> list<str>[4]
    """
    # Read
    ID = file_.readline()
    seq = file_.readline()
    placeholder = file_.readline()
    scores = file_.readline()
    # Strip
    ID = ID.strip("\n")
    seq = seq.strip("\n")
    placeholder = placeholder.strip("\n")
    scores = scores.strip("\n")
    # Return
    return [ID, seq, placeholder, scores]



def Create_Output(ID, seq, placeholder, scores):
    """
    Take the data for FASTQ read and generate a string that can be written to
    file.
    
    Create_Output(str, str, str, str) -> str
    """
    sb = ID + "\n" + seq + "\n" + placeholder + "\n" + scores + "\n"
    return sb



def Ints_To_Aligned_Strings(list1, alignment):
    """
    Convert a list of integers into a series of strings of equal length.
    
    @list1
            (list<int>)
            The integers which need to be converted to text
    @alignment
            (int)
            An integer denoting the direction of alignment:
                1: LEFT
                2: RIGHT
    
    Return a list of strings corresponding to the integers.
    
    Ints_To_Aligned_Strings(list<int>, int) -> list<str>
    """
    # Initialize
    max_length = 0
    temp = []
    result = []
    # First run through
    for integer in list1:
        string = str(integer)
        length = len(string)
        if length > max_length: max_length = length
        temp.append(string)
    # Pad strings
    for string in temp:
        length = len(string)
        if length == max_length: result.append(string)
        else:
            dif = max_length - length
            pad = dif*" "
            if alignment == ALIGN.LEFT:
                string = string+pad
            elif alignment == ALIGN.RIGHT:
                string = pad+string
            result.append(string)
    # Return
    return result

def Get_Percentage_Strings(numerators, denominator, decimal_places, length=0):
    """
    Calculate a percentage using numerators and a denominator, then return a
    list of strings of the percentages with the specified number of decimal
    places. The string is also padded to the specified length.
    
    @numerators
            (list<int/float>)
    @denominator
            (int/float)
    @decimal_places
            (int)
    @length
            (int)
    
    Get_Percentage_String(list<int/float>, int/float, int, int) -> list<str>
    """
    results = []
    for n in numerators:
        string = Get_Percentage_String(n, denominator, decimal_places, length)
        results.append(string)
    return results
    
def Get_Percentage_String(numerator, denominator, decimal_places, length=0):
    """
    Calculate a percentage using a numerator and a denominator, then return the
    string of that percentage with the specified number of decimal places.
    The string is also padded to the specified length.
    
    @numerator
            (int/float)
    @denominator
            (int/float)
    @decimal_places
            (int)
    @length
            (int)
    
    Get_Percentage_String(int/float, int/float, int, int) -> str
    """
    length_x = length - (decimal_places + 1)

    if denominator != 0: percentage = (numerator*100.0)/denominator
    else: percentage = 0.0
    
    string = str(percentage)
    
    part_1, part_2 = string.split(".")
    length_1 = len(part_1)
    length_2 = len(part_2)

    dif_1 = length_x - length_1
    if dif_1: part_1 = dif_1*" " + part_1

    dif_2 = decimal_places - length_2
    if dif_2 > 0: part_2 = part_2 + dif_2*"0"
    else: part_2 = part_2[:decimal_places]

    result = part_1 + "." + part_2
    return result



# Command Line Parsing #########################################################

def Parse_Command_Line_Input__Sort_By_R2_BCode(raw_command_line_input):
    """
    Parse the command line input and call the Table_To_Table function with
    appropriate arguments if the command line input is valid.
    """
    printP(STR__parsing_args)
    # Remove the runtime environment variable and program name from the inputs
    inputs = Strip_Non_Inputs(raw_command_line_input)

    # No inputs
    if not inputs:
        printE(STR__no_inputs)
        printE(STR__use_help)
        return 1
  
    # Help option
    if inputs[0] in LIST__help:
        print(HELP_DOC)
        return 0

    # Initial validation
    if len(inputs) < 3:
        printE(STR__insufficient_inputs)
        printE(STR__use_help)
        return 1
    
    # Validate inputs
    path_in_r1 = inputs.pop(0)
    valid_in_r1 = Validate_Read_Path(path_in_r1)
    if valid_in_r1 == 1:
        printE(STR__IO_error_read.format(f = path_in_r1))
        return 1
    
    path_in_r2 = inputs.pop(0)
    valid_in_r2 = Validate_Read_Path(path_in_r2)
    if valid_in_r2 == 1:
        printE(STR__IO_error_read.format(f = path_in_r2))
        return 1
    
    barcode = inputs.pop(0)
    valid_barcode = Validate_Barcode(barcode)
    if valid_barcode == 1:
        printE(STR__invalid_barcode.format(s = barcode))
        return 1
    
    # Set up rest of the parsing
    paths_in = [path_in_r1, path_in_r2]
    paths_out = Generate_Default_Output_Paths(path_in_r1, path_in_r2)
    thresholds = [DEFAULT__threshold_match, DEFAULT__threshold_partial]
    removes = [DEFAULT__remove_r1, DEFAULT__remove_r2]
    
    # Parse the rest
    while inputs:
        arg = inputs.pop(0)
        if arg == "-o": # Output files
            try:
                paths_out = [inputs.pop(0), inputs.pop(0), inputs.pop(0),
                        inputs.pop(0), inputs.pop(0), inputs.pop(0)]
            except:
                printE(STR__specify_6_arguments_for_outputs)
        elif arg == "-t": # Thresholds
            try:
                t1 = inputs.pop(0)
                t2 = inputs.pop(0)
            except:
                printE(STR__specify_2_arguments_for_thresholds)
            v1 = Validate_Threshold(t1)
            v2 = Validate_Threshold(t2)
            if v1 == -1 or v2 == -1:
                printE(STR__invalid_threshold)
                return 1
            thresholds = [v1, v2]
        elif arg in ["-r", "-a"]: # Remove barcodes
            try:
                r1 = inputs.pop(0)
                r2 = inputs.pop(0)
            except:
                printE(STR__specify_2_arguments_for_remove)
            r1 = Validate_Boolean(r1)
            r2 = Validate_Boolean(r2)
            if r1 == None:
                printE(STR__invalid_bool.format(s = r1))
                return 1
            if r2 == None:
                printE(STR__invalid_bool.format(s = r2))
                return 1
            removes = [r1, r2]
        else: # Invalid
            arg = Strip_X(arg)
            printE(STR__invalid_argument.format(s = arg))
            printE(STR__use_help)
            return 1
    
    # Validate output paths
    for path in paths_out:
        valid_out = Validate_Write_Path(path)
        if valid_out == 2: return 0
        if valid_out == 3:
            printE(STR__IO_error_write_forbid)
            return 1
        if valid_out == 4:
            printE(STR__In_error_write_unable)
            return 1
    
    # Run program
    Sort_By_R2_Barcode(paths_in, paths_out, barcode, thresholds, removes)
    
    # Safe exit
    return 0



def Validate_Read_Path(filepath):
    """
    Validates the filepath of the input file.
    Return 0 if the filepath is valid.
    Return 1 otherwise.
    
    Validate_Read_Path(str) -> int
    """
    try:
        f = open(filepath, "U")
        f.close()
        return 0
    except:
        return 1



def Validate_Barcode(string):
    """
    Validates the string being used as a target barcode.
    Return 0 if the barcode is valid.
    Return 1 otherwise.

    Validate_Barcode(str) -> int
    """
    for c in string:
        if c not in NSeq_Match.LIST__all_n: return 1
    return 0



def Generate_Default_Output_Paths(path_in_r1, path_in_r2):
    """
    Generate six output filepaths based on the two provided input filepaths.

    Generate_Default_Output_Paths(str, str) -> list<str>[6]
    """
    # Get indexes
    index_1 = Find_Period_Index(path_in_r1)
    index_2 = Find_Period_Index(path_in_r2)
    # Get paths
    paths_1 = Modify_Path(path_in_r1, index_1)
    paths_2 = Modify_Path(path_in_r2, index_2)
    # Return final
    return [paths_1[0], paths_2[0], paths_1[1], paths_2[1],
            paths_1[2], paths_2[2]]

def Modify_Path(filepath, index):
    """
    Return 3 filepaths based on a modification of [filepath], using [index] to
    determine where the file extension begins.
    
    Expand_Path(str, int) -> [str, str, str]
    """
    if index == -1:
        p1 = filepath + FILEMOD__MATCH
        p2 = filepath + FILEMOD__PARTIAL
        p3 = filepath + FILEMOD__ABSENT
    else:
        path = filepath[:index]
        extension = filepath[index:]
        p1 = path + FILEMOD__MATCH + extension
        p2 = path + FILEMOD__PARTIAL + extension
        p3 = path + FILEMOD__ABSENT + extension
    return [p1, p2, p3]   

def Find_Period_Index(filepath):
    """
    Return the index of a filepath's file extension string. (The index of the
    period.)
    
    Return -1 if the file name has no file extension.
    
    Find_Period_Index(str) -> int
    """
    # Find period
    index_period = filepath.rfind(".")
    if index_period == -1: return -1 # No period
    # Slash and backslash
    index_slash = filepath.rfind("/")
    index_bslash = filepath.rfind("\\")
    if index_slash == index_bslash == -1: return index_period # Simple path
    # Complex path
    right_most = max(index_slash, index_bslash)
    if right_most > index_period: return -1 # Period in folder name only
    return index_period


    
def Validate_Write_Path(filepath):
    """
    Validates the filepath of the input file.
    Return 0 if the filepath is writtable.
    Return 1 if the user decides to overwrite an existing file.
    Return 2 if the user declines to overwrite an existing file.
    Return 3 if the file exists and the program is set to forbid overwriting.
    Return 4 if the program is unable to write to the filepath specified.
    
    Validate_Write_Path(str) -> int
    """
    try:
        f = open(filepath, "U")
        f.close()
    except: # File does not exist. 
        try:
            f = open(filepath, "w")
            f.close()
            return 0 # File does not exist and it is possible to write
        except:
            return 4 # File does not exist but it is not possible to write
    # File exists
    if WRITE_PREVENT: return 3
    if WRITE_CONFIRM:
        confirm = raw_input(STR__overwrite_confirm.format(f=filepath))
        if confirm not in LIST__yes: return 2
    # User is not prevented from overwritting and may have chosen to overwrite
    try:
        f = open(filepath, "w")
        f.close()
        if WRITE_CONFIRM: return 1 # User has chosen to overwrite existing file
        return 0 # Overwriting existing file is possible
    except:
        return 4 # Unable to write to specified filepath



def Strip_X(string):
    """
    Strips leading and trailing inverted commans or brackets if a matching pair
    are flanking the string.
    
    Strip_X(str) -> str
    """
    if (    (string[0] == string[-1] == "\"") or
            (string[0] == string[-1] == "\'") or
            (string[0] == "(" and string[-1] == ")") or
            (string[0] == "{" and string[-1] == "}") or
            (string[0] == "[" and string[-1] == "]") or
            (string[0] == "<" and string[-1] == ">")
            ):
        return string[1:-1]
    return string



def Validate_Threshold(string):
    """
    Validates and returns the threshold number specified.
    Return -1 if the input is invalid.
    
    @string
        (str)
        A string denoting a non-negative thrshold
        
    Validate_Column_Number(str) -> int
    """
    try:
        n = int(string)
    except:
        return -1
    if n < 0: return -1
    return n



def Validate_Boolean(string):
    """
    Validates and returns a boolean, based on the string given.
    Return None if the input is invalid.
    
    @string
        (str)
        A string denoting either True, False, Yes, or No.
        
    Validate_Column_Number(str) -> bool
    OR
    Validate_Column_Number(str) -> None
    """
    if string in LIST__yes: return True
    if string in LIST__no: return False
    return None



def Strip_Non_Inputs(list1):
    """
    Remove the runtime environment variable and program name from the inputs.
    Assumes this module was called and the name of this module is in the list of
    command line inputs.
    
    Strip_Non_Inputs(list<str>) -> list<str>
    """
    if NAME in list1[0]: return list1[1:]
    return list1[2:]



# Controlled Print Statements ##################################################

def printE(string):
    """
    A wrapper for the basic print statement.
    It is intended to be used for printing error messages.
    It can be controlled by a global variable.
    """
    if PRINT_ERRORS: print(string)

def printP(string):
    """
    A wrapper for the basic print statement.
    It is intended to be used for printing progress messages.
    It can be controlled by a global variable.
    """
    if PRINT_PROGRESS: print(string)

def printM(string):
    """
    A wrapper for the basic print statement.
    It is intended to be used for printing file metrics.
    It can be controlled by a global variable.
    """
    if PRINT_METRICS: print(string)



# Main Loop ####################################################################

if AUTORUN and (__name__ == "__main__"):
    exit_code = Parse_Command_Line_Input__Sort_By_R2_BCode(sys.argv)
