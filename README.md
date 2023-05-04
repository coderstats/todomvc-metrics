# todomvc-metrics

Code for aggregating metrics and creating graphs to compare TodoMVC example
applications based on code complexity measures.

Related article: [How Complex are TodoMVC Implementations](https://geeksta.net/geeklog/todomvc-complexity/)

## How to reproduce the reports

Below I outline the steps to create these reports using the scripts in this repository.

Install the complexity-report node package

    npm install

Clone the todomvc repository

    git clone https://github.com/tastejs/todomvc.git

To automate report and image generation the Python libraries fabric, Pandas and matplotlib are required. I recommend to install them in a virtual environment.

    pip install -r requirements

Now run the following commands

    fab clean
    python gen_reports.py
    aggregate.py