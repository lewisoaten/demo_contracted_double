#![feature(proc_macro_hygiene, decl_macro)]

use std::collections::HashMap;

use rocket::State;

#[macro_use]
extern crate rocket;

#[get("/add_ten/<num>")]
fn add_ten(paths: State<Paths>, num: u32) -> String {
    use serde_json::{Result, Value};
    let path = paths.paths.get("sum").unwrap();

    let text = reqwest::blocking::get(&format!("{}/10/and/{}", path, num))
        .unwrap()
        .text()
        .unwrap();

    let val: Value = serde_json::from_str(&text).unwrap();
    val["result"].to_string()
}

pub struct Paths {
    pub paths: HashMap<String, String>,
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let mut paths = Paths {
        paths: HashMap::new(),
    };
    paths.paths.insert("sum".to_owned(), format!("http://localhost:{}", args[0]));
    rocket::ignite()
        .manage(paths)
        .mount("/", routes![add_ten])
        .launch();
}

mod test {
    use std::{collections::HashMap, thread};

    use super::*;
    use pact_consumer::prelude::*;
    use pact_consumer::*;
    use rocket::local::Client;

    #[test]
    fn a_service_consumer_side_of_a_pact_goes_a_little_something_like_this() {
        let pact = PactBuilder::new("api1", "api2")
            .interaction("a request to sum 10 and 20", |i| {
                i.request.get().path("/sum/10/and/20");

                i.response
            .created()
            .json_body(json_pattern!({
                "time": term!("\\d+-\\d+-\\d+T\\d+:\\d+:\\d+\\.\\d+", "2021-02-06T10:11:27.919516"),
                "first": 10,
                "second": 20,
                "result": 30,
            }));
                // Return a location of "/quotes/12" to the client. When
                // testing the server, allow it to return any numeric ID.
            })
            .build();

        // Start the mock server running.
        let alice_service = pact.start_mock_server();

        // You would use your actual client code here.
        let url = alice_service.path("/sum");

        let mut paths = Paths {
            paths: HashMap::new(),
        };
        paths.paths.insert("sum".to_owned(), url.to_string());
        let rocket = rocket::ignite().manage(paths).mount("/", routes![add_ten]);
        let client = Client::new(rocket).expect("valid rocket instance");
        // let mut response = reqwest::blocking::get(mallory_url).expect("could not fetch URL");
        let body = client.get("/add_ten/20").dispatch().body_string().unwrap();
        assert_eq!(body, "30");

    }
}
