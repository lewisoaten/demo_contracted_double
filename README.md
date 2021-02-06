# Test Double with Contract
## Introduction
Python example of a test double, which is verified with a contract. TL;DR: Better Integration Testing!

Inspired by Martin Fowlers 
view of [Integration Testing](https://martinfowler.com/bliki/IntegrationTest.html).

The consumer of a microservice runs it as a TestDouble and executes a full suite of testing. All interactions are captured 
in a contract. This contract can then be executed against the real service along with any other consumer contracts to ensure changes to that 
service do not break that interface.

These integration tests run in each services' Unit Testing framework! This means they run FAST and aid service-independent development. 

Uses the wonderful:
 - [FastAPI](https://github.com/tiangolo/fastapi) - for effortless APIs.
 - [Pact](https://github.com/pact-foundation/pact-python) - for mocking dependent services while capturing the contract, and seperately executing 
   the contract as a unit test.
 - [PyTest](https://github.com/pytest-dev/pytest) - to execute all of the tests

## How it Works
![Interaction Diagram](https://docs.pact.io/assets/images/pact-test-and-verify-7ae6e70a9a42ffa4ac8373ba294b19d9.png)

To run:
1. Install dependencies.
2. Run `python -m pytest demo_contracted_double/tests/api1/` to run api1 unit tests, and integration tests against a TestDouble.
3. Run `python -m pytest demo_contracted_double/tests/api2/` to run api2 unit tests, and integration tests against the contract defined by the 
   previous step.