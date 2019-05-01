# Strategy

This document describes the connect-process and the connection between the
different modules.

## Connection process

### Naming

* Process: A process is a algorithm which transform data and has in- and out-
ports.

* Port: A port is a connection which is fluwn by data.

* Outputdata: The outputdata is proced by the process. The naming of the data
fits into the following pattern:

```[txt]
process__featureA_datum_a
process__featureA_datum_b
process__featureB_datum_a
```

* Datapool: A datapool is represented by one folder. The folder contains
 different data. The folder is named by the process itself.

## Architecture

### Processes

`rawmaker`: the rawmaker converts pdf to document raw data.

Input:

* pdf-file    (jobid.pdf)
  the-hanumann(54235232.pdf)

Output:

* rawmaker/rawmaker__tableofcontent.yaml

```[txt]
A list of the table of content of the pdf document. The headlines are given
with the level/value of the chapter.
```

* rawmaker/rawmaker__text.yaml
