import React from 'react';
import {Navbar,Nav} from 'react-bootstrap';
import "./Place_Order_header.scss";

function Place_Order_header() {
  
  return (
    
    <header className='row'>
      
                <Navbar bg='dark' variant='dark' >
                  <div>
                  <Nav.Link href="#/"><h1>Pharma-B</h1></Nav.Link>              
                  </div>
                  <div>
                  <Nav>
                    
                      
                    <Nav.Link href="#/Inventory"><i class="fa fa-fw fa-search"></i>Inventory</Nav.Link>
                    <Nav.Link href="#/Order">Place Order</Nav.Link>
                    <Nav.Link href='#/Cart'>Cart</Nav.Link>
                  </Nav>
                  </div>
          
                </Navbar>
                </header>
  )
}

export default Place_Order_header