import booktest as bt

import test.examples.example_suite as es
import test.examples.example_book as eb
import test.test_names_test as tn

tests = bt.merge_tests([
    tn.CamelCaseNamesTestBook(),
    tn.ApiV1TestBook(),
    tn.GetURLTestBook(),
    tn.ALLCAPSTestBook(),
    tn.URLOpsTestBook(),
    es.example_suite,
    eb.ExampleTestBook(),
])
