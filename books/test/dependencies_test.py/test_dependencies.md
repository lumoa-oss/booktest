# description:

this test creates a test of other tests and checks their dependencies

# test suites:

 * test/dependencies_test.py::DataSourceBook
 * test/dependencies_test.py::CrossDependencyTest
 * test/dependencies_test.py::DataUser1Book
 * test/dependencies_test.py::DataUser2Book
 * test/dependencies/parametrized1
 * test/dependencies/parametrized2

# test cases:

 * test/dependencies_test.py::DataSourceBook/test_create_data
 * test/dependencies_test.py::DataSourceBook/test_use_data
 * test/dependencies_test.py::CrossDependencyTest/test_cross_use_data
 * test/dependencies_test.py::DataUser1Book/test_use_data
 * test/dependencies_test.py::DataUser2Book/test_use_data
 * test/dependencies/parametrized1/test_create_data
 * test/dependencies/parametrized1/test_process_data
 * test/dependencies/parametrized1/test_use_processed_data
 * test/dependencies/parametrized2/test_create_data
 * test/dependencies/parametrized2/test_process_data
 * test/dependencies/parametrized2/test_use_processed_data

# case dependencies:

 * test/dependencies_test.py::DataSourceBook/test_create_data:
 * test/dependencies_test.py::DataSourceBook/test_use_data:
     * test/dependencies_test.py::DataSourceBook/test_create_data
 * test/dependencies_test.py::CrossDependencyTest/test_cross_use_data:
     * test/dependencies_test.py::DataSourceBook/test_create_data
 * test/dependencies_test.py::DataUser1Book/test_use_data:
     * test/dependencies_test.py::DataSourceBook/test_create_data
 * test/dependencies_test.py::DataUser2Book/test_use_data:
     * test/dependencies_test.py::DataSourceBook/test_create_data
 * test/dependencies/parametrized1/test_create_data:
 * test/dependencies/parametrized1/test_process_data:
     * test/dependencies/parametrized1/test_create_data
 * test/dependencies/parametrized1/test_use_processed_data:
     * test/dependencies/parametrized1/test_create_data
     * test/dependencies/parametrized1/test_process_data
 * test/dependencies/parametrized2/test_create_data:
 * test/dependencies/parametrized2/test_process_data:
     * test/dependencies/parametrized2/test_create_data
 * test/dependencies/parametrized2/test_use_processed_data:
     * test/dependencies/parametrized2/test_create_data
     * test/dependencies/parametrized2/test_process_data
