import React, { useState } from "react";
import { Data } from "./order_items";
import "./Place_Order_main.scss";
import got from "got";
// ES6 Modules or TypeScript
import Swal from "sweetalert2";

// CommonJS
function Place_Order_main() {
  const [searchTerm, setSearchTerm] = useState("");

  return (
    <div className="hello">
      <div></div>
      <input
        type="text"
        placeholder="Search..."
        className="col-md-6 Placeholder"
        onChange={(event) => {
          setSearchTerm(event.target.value);
        }}
      />
      {Data.filter((val) => {
        if (searchTerm == "") {
          return val;
        } else if (val.Name.toLowerCase().includes(searchTerm.toLowerCase())) {
          return val;
        }
      }).map((val, key) => {
        return (
          <div className="row product">
            <div className="col-md-2">
              <img src={val.Image} alt="Sample Image" height="150" />
            </div>
            <div className="col-md-8 product-detail">
              <h4>{val.Name}</h4>
              <p>{val.Description}</p>
            </div>

            <div className="col-md-2 product-price">Price: {val.Price}</div>
            <div>
              <button
                className="col-md-2 button"
                onClick={() => {
                  got
                    .post("localhost:3001\test", {
                      json: {
                        hello: "world",
                      },
                    })
                    .json()
                    .then(({ data }) => {
                      console.log(data);
                    });

                  Swal.fire(
                    "Order Sent!",
                    "You have successfully made the order!",
                    "success"
                  );
                }}
              >
                Send Order Request
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default Place_Order_main;
