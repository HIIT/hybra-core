Examples
=======

Find mentions to cats and print them
*************************************
::

  from hybra.core import hybra

  hybra.set_data_path('.')

  data_yle = hybra.load('media', folder='yle/')

  data_yle_cats = hybra.filter_from_text( data_yle , ['kiss'] )

  for data_entry in data_yle_cats:
    print data_entry['text_content']
    print '' ## empty line makes it easier to work on
