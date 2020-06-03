html_style = """
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto+Sans:ExtraCondensed+ExtraLight" />
    <style>
        body {
            font-family: "Noto Sans";
            font-style: normal;
            font-weight: normal;
            font-size: 8px;
            line-height: 1.25;
        }
        .container {
            columns: 2;
            column-gap: 7px;
            column-fill: balance;
        }
        .tweet {
            display: flex;
            margin-bottom: 7px;
            padding: 5px;
            border-radius: 3px;
            background-color: lightskyblue;
        }
        .container .tweet:nth-child(odd) {
            background-color: whitesmoke;
        }
        .tweet-text {
            flex: 1;
            text-align: justify;
        }
        .tweet-qrcode {
            margin-left: 7px;
        }
    </style>
"""

pdf_style = """
    @page {
        size: A4;
        margin: 10mm;
    }
"""
