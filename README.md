# fretty-book

fretty-book can replace inline [fretty](https://github.com/thomasvolk/fretty) markup within documents with the generated images.

## Installation

    pip install fretty-book

## Usage

    fretty-book example/document.html -o out/document.html


## Markup

### html

```
<!DOCTYPE html>
<html>
    <head>
        <title>test document</title>
    </head>
    <body>

        <h1>Fretty test document for html processing</h1>

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