"""
wikipedia citation numbers appear as word followed by . followed number without any spaces, so 
need to write regex to eliminate the numbers from those patterns so that they don't show up 
in outputed text. 

We should also used the stanford parser to parse all of the sentences in our style doc and 
eliminate the sentences that don't pass the test -- these are probably headers/titles.
"""