Examples
=========

Find mentions to cats in Yle data and print them
************************************************
::
.. literalinclude:: examples/yle_cats.py


Find ten most common authors in Facebook data and print them
************************************************************
::

  from collections import Counter

  authors = [] ## create an empty list for the authors

  for data_entry in data_fb: ## go through the loaded Facebook data
    authors.append( data_entry['creator'] ) ## and add authors on the list

  most_common_authors = Counter(authors).most_common(10) ## save 10 most common authors

  for author, count in most_common_authors: ## go through the most common authors
    print author + ' ' + str(count) ## and print them
