html_style = """
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto+Sans:ExtraCondensed+ExtraLight" />
    <style>
        body {
            font-family: "Noto Sans", sans-serif;
            font-size: 8px;
            line-height: 1.25;
        }

        .title {
            font-weight: bold;
            font-size: 14px;
            text-align: center;
        }

        .subtitle {
            font-style: italic;
            text-align: center;
            margin-bottom: 20px;
            color: gray;
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
            border-bottom: 1px solid black;
        }

        .tweet-content {
            display: flex;
        }

        .tweet-text {
            flex: 1;
            text-align: justify;
        }

        .tweet-author {
            font-weight: bold;
        }

        .tweet-qrcode {
            margin-left: 10px;
        }

        .tweet-stats {
            display: flex;
            justify-content: space-between;
            margin: 1px 0;
            font-style: italic;
            font-size: 6px;
            color: gray;
        }
    </style>
"""

pdf_style = """
    @page {
        size: A4;
        margin: 10mm;
    }
"""
