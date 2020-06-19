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
            margin-bottom: 15px;
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
        .tweet-box {
            display: flex;
            flex-direction: column;
            margin-bottom: 5px;
            padding-bottom: 1px;
            border-bottom: 1px solid black;
        }
        .tweet-box-content {
            display: flex;
        }
        .tweet-text {
            flex: 1;
            text-align: justify;
        }
        .tweet-qrcode {
            margin-left: 10px;
        }
        .tweet-stats {
            display: flex;
            justify-content: space-between;
            font-size: 6px;
            color: gray;
            text-align: left;
            margin-top: 3px;
            margin-bottom: 0px;
        }

    </style>
"""

pdf_style = """
    @page {
        size: A4;
        margin: 10mm;
    }
"""
