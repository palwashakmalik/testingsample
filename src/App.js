//import {FontAwesomeIcon} from'@fortawesome/react-fontawesome';
//import {faCapsules} from "@fortawesome/free-solid-svg-icons"
//import {NavLink } from 'react-router-dom';
//import {Nav} from 'react-bootstrap';
import React, {useState} from "react";
//import Navbar from './components/Home-page/Navbar';
import './App.css';
import {BrowserRouter, Route,Routes} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.css';
import Place_order_basket from './components/retailer-page/Place_order_basket';
import Place_Order_header from './components/retailer-page/Place_Order_header';
import Place_Order_main from './components/retailer-page/Place_Order_main';
import {Data} from './components/retailer-page/order_items';

import { connect } from 'react-redux'
  
function App() 
{
  
  const{cartItems,setCartItems}=useState([]);
 
    return (  <div className="App"> 
      
       <Place_Order_header/>
       <Place_Order_main data={Data}></Place_Order_main>
       
        
        </div>

    
   
  );
            
      
}

export default App;
