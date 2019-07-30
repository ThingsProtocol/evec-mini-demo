import React from "react";
import TransferForm from './components/transfer_fund'
import CheckBalance from './components/check_balance'

import { BrowserRouter as Router, Route, Link } from "react-router-dom";

function BasicExample() {
  return (
    <Router>
      <div>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/transfer">Transfer Fund</Link>
          </li>
          <li>
            <Link to="/check">Check Balance</Link>
          </li>

        </ul>

        <hr />

        <Route exact path="/" component={Home} />
        <Route path="/transfer" component={Transfer} />
        <Route path="/check" component={Check} />
        
      </div>
    </Router>
  );
}

function Home() {
  return (
    <div>
      <h2>This is the homepage.</h2>
    </div>
  );
}

function Transfer() {
  return (
    <div>
      <TransferForm/>
    </div>
  );
}

function Check() {
  return (
    <div>
      <CheckBalance/>
    </div>
  );
}


export default BasicExample;
