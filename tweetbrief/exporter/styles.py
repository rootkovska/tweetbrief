html_style = """
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto+Sans:ExtraCondensed+ExtraLight" />
    <style>
        h1 {
            text-align: center;
            font-family: "Noto Sans";
            font-style: normal;
            font-weight: bold;
            font-size: 14px;
            line-height: 1;
        }
        h2 {
            text-align: center;
            font-family: "Noto Sans";
            font-style: normal;
            font-weight: normal;
            font-size: 8px;
            color: gray;
            line-height: 1;
        }
        body {
            font-family: "Noto Sans";
            font-style: normal;
            font-weight: normal;
            font-size: 8px;
            line-height: 1;
        }
        .container {
            columns: 2;
            column-gap: 20px;
            column-fill: balance;
        }
        .tweet {
            display: flex;
            margin-bottom: 10px;
            padding-bottom: 9px;
            border-bottom: 1px solid black;
        }
        .tweet-text {
            flex: 1;
            text-align: justify;
        }
        .tweet-qrcode {
            margin-left: 10px;
        }
    </style>
"""

pdf_style = """
    @page {
        size: A4;
        margin: 10mm;
    }
"""
