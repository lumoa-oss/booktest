# description:

this test creates a test of other tests and checks their dependencies

# test suites:

 * test/dependencies/data_source
 * test/dependencies/cross_dependency
 * test/dependencies/data_user1
 * test/dependencies/data_user2
 * test/dependencies/parametrized1
 * test/dependencies/parametrized2

# test cases:

 * test/dependencies/data_source/create_data
 * test/dependencies/data_source/use_data
 * test/dependencies/cross_dependency/cross_use_data
 * test/dependencies/data_user1/use_data
 * test/dependencies/data_user2/use_data
 * test/dependencies/parametrized1/create_data
 * test/dependencies/parametrized1/process_data
 * test/dependencies/parametrized1/use_processed_data
 * test/dependencies/parametrized2/create_data
 * test/dependencies/parametrized2/process_data
 * test/dependencies/parametrized2/use_processed_data

# case dependencies:

 * test/dependencies/data_source/create_data:
 * test/dependencies/data_source/use_data:
     * test/dependencies/data_source/create_data
 * test/dependencies/cross_dependency/cross_use_data:
     * test/dependencies/data_source/create_data
 * test/dependencies/data_user1/use_data:
     * test/dependencies/data_source/create_data
 * test/dependencies/data_user2/use_data:
     * test/dependencies/data_source/create_data
 * test/dependencies/parametrized1/create_data:
 * test/dependencies/parametrized1/process_data:
     * test/dependencies/parametrized1/create_data
 * test/dependencies/parametrized1/use_processed_data:
     * test/dependencies/parametrized1/create_data
     * test/dependencies/parametrized1/process_data
 * test/dependencies/parametrized2/create_data:
 * test/dependencies/parametrized2/process_data:
     * test/dependencies/parametrized2/create_data
 * test/dependencies/parametrized2/use_processed_data:
     * test/dependencies/parametrized2/create_data
     * test/dependencies/parametrized2/process_data
