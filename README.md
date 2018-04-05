# pleiades.refbot

A collection of python modules and scripts for working with bibliographic data for the [Pleiades gazetteer of ancient places](https://pleiades.stoa.org).

## scripts

### validate_zotero.py

Does (at present very basic) validation on a [Zotero](https://zotero.org) library that has been exported to a CSV file. Run it like:

```
python scripts/validate_zotero.py -h
usage: validate_zotero.py [-h] [-l LOGLEVEL] [-o OUTPUT] [-v] [-w] zotero_csv

Validate the Pleiades Zotero Library

positional arguments:
  zotero_csv            path to the Zotero csv file

optional arguments:
  -h, --help            show this help message and exit
  -l LOGLEVEL, --loglevel LOGLEVEL
                        desired logging level (case-insensitive string: DEBUG,
                        INFO, WARNING, or ERROR (default: NOTSET)
  -o OUTPUT, --output OUTPUT
                        path to directory for CSV output of errors (default:
                        NOTSET)
  -v, --verbose         verbose output (logging level == INFO) (default:
                        False)
  -w, --veryverbose     very verbose output (logging level == DEBUG) (default:
                        False)
```

All that's considered is whether there are values present in each record for the "Title" and "Short Title" fields.

## modules

See the tests for usage details. I aim to keep test coverage at 100% for all module code.

### module: ```walker```

Provides two classes for working with a collection of files in a possibly hierarchical directory structure on disk:

#### class: ```walker.Walker```

A base class that can selectively visit files in a tree and act on them. The class is instantiated with an optional list of filename extensions to detect (if ignored, all files are considered). The ```walk``` method makes use of the ```walk``` function from the standard library, calling stub methods for loading files, cleaning data read from files, and acting on that data. These are meant to be overridden when subclassing ```Walker```.

#### class ```walker.JsonWalker```

Subclasses ```Walker``` to find all JSON files (extension='.json') in the specified directory subtree and read their content into memory (using the standard library ```json.load``` method). It does not override ```Walker._clean``` or ```Walker._do``` methods. It is meant to be further subclassed for specific tasks.

### module: ```zotero```

Provides two classes for working with Zotero bibliographic data:

#### class ```zotero.ZoteroRecord```

A modestly subclassed ```dict``` for storing and manipulating data from a single Zotero record. Right now, all that's overridden is the ```__str__``` function to give a helpfully abbreviated serialization.

#### class ```zotero.ZoteroCollection```

A class for storing and manipulating data for a collection of ```ZoteroRecord```s. This class knows how to:

 - Construct itself using a list of dictionaries, each of which provides field+value pairs for a record.
 - Load ```ZoteroRecord```s from a CSV file.
 - Add a single ```ZoteroRecord``` to the collection from a dictionary of field+value pairs.
 - Get a single ```ZoteroRecord``` from the collection, given its "Key"
 - Match a subset of ```ZoteroRecords``` from the collection, given a dictionary of field+value pairs to be matched.
 - Validate ```ZoteroRecords``` in the collection, given a dictionary of criteria statements.
 
