import csv
import types

def __get_common_keys( data ):

    keys = []

    for key in data[0].keys():
        if key[0] != '_':
            keys.append(key)

    return keys


def export_csv( data, file_path ):

    if isinstance( data, types.GeneratorType ):
        data = list( data )

    writer = csv.writer( open(file_path, 'wb'), delimiter=',' )

    keys = __get_common_keys( data )

    writer.writerow(keys)

    for d in data:
        values = []

        for key in keys:
            value = unicode( d[key] )
            value = value.replace('\n', ' ').replace('\r', ' ')
            values.append( value.encode('utf8') )

        writer.writerow(values)


def export_xlsx( data, file_path ):

    if isinstance( data, types.GeneratorType ):
        data = list( data )

    import xlsxwriter

    workbook = xlsxwriter.Workbook( open(file_path, 'wb'), {'strings_to_urls': False} )

    keys = __get_common_keys( data )

    worksheet = workbook.add_worksheet()

    for column in range( 0, len(keys) ):
        worksheet.write( 0, column, keys[column] )

    for row in range( 0, len(data) ):

        for column in range( 0, len(keys) ):
            key = keys[column]
            value = unicode( data[row][key] )
            worksheet.write(row + 1, column, value)

    workbook.close()
