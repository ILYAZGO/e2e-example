HOW TO RUN LOCALLY:

install requirements and browsers:

    pip install -r requirements.txt  (for install requirements)
    playwright install (for install browsers)

from main directory:

   # for e2e tests (change url if needed. define test-set if needed):

    pytest -n auto --base-url https://app.stand.imot.io/ tests/

   # for api tests:

    pytest -n auto api_tests/

   !!!!PROFIT!!!!


you can add some parameteres:

    --headed  (with browser head)
    --slowmo 3000  (if you want to slow tests down in 3000 ms)
    --numprocesses auto / -n auto (few workers same time. will parallel tests)

    -m {some marker}  (you can call test-sets. look markers in pytest.ini)


    preconditions:
    admin : login-4adminIM name-adminIM

    user for import : importFromLogin importFrom
    with group 11111 rule 22222 inside
    with rule 33333 without group





