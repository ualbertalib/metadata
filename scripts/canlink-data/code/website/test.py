from pymarc import MARCReader

def getField(record, tag_value, subfield_value=None):
    # tag ex: "710"
    # subfield ex: "b"
    # need this function since just doing record["710"]["b"] doesn't work if
    # there are multiple lines of the same tag
    results = []
    for field in record.get_fields(tag_value):
        if not subfield_value:
            return(field)
        for subfield in field:
            if subfield[0] == subfield_value:
                results.append(subfield[1])

    # remove the duplicate results because sometimes they exist
    results = list(set(results))
    return(results)

with open('MUN_4971_Theses_for_CLDI_linked.mrc', "rb") as marc_file:
    reader = MARCReader(marc_file, force_utf8=True)
    for record in reader:
        value_856u = getField(record, "856", "u")
        print (value_856u)