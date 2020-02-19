import csv
import types

def __get_common_keys( data ):

    keys = data[0].keys()

    keys = filter( lambda x: not x.startswith('_'), keys )

    return list( keys )


def export_csv( data, file_path ):

    if isinstance( data, types.GeneratorType ):
        data = list( data )

    writer = csv.writer( open(file_path, 'w', encoding='utf-8'), delimiter=',' )

    keys = __get_common_keys( data )

    print( keys )

    writer.writerow(keys)

    for d in data:
        values = []

        for key in keys:
            value = d[key]
            # value = value.replace('\n', ' ').replace('\r', ' ') ## this breaks stating that
            values.append( value )

        writer.writerow(values)


def export_xlsx( data, file_path ):

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
            value = data[row][key]
            worksheet.write(row + 1, column, value)

    workbook.close()
