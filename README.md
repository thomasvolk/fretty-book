# fretty-book

fretty-book can replace inline [fretty](https://github.com/thomasvolk/fretty) markup within documents with the generated images.

## Installation

    pip install fretty-book

## Usage

    fretty-book example/simple.html -o simple.html


## Markup

fretty-book can process HTML and XHTML documents. All `<fretty>` tags will be replaced with the image generated with the included markup. 

### html

This markup ...

```
<!DOCTYPE html>
<html>
    <head>
        <title>test document</title>
    </head>
    <body>

        <h3>Fretty test document for html processing</h3>

        <p>Tabs for C major scale</p>
        <fretty width="400">
            III
            --o-o1
            --oo-o
            -o1-o-
            o-o-o-
            1-o-o-
            o-o-o-
        </fretty>
    </body>
</html>
```
will produce this result:

---

<h3>Fretty test document for html processing</h3>

<p>Tabs for C major scale</p>

<img src="example/simple/fretty-0.svg"/>

---