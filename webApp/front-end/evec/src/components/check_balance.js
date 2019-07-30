import React from 'react';
import { Formik } from 'formik';
import axios from 'axios';


//check balance
const CheckBalance = () => (
    <div>
      <h1>Check Balance</h1>
      <Formik
        onSubmit={(values, actions) => {
          setTimeout(() => {
            alert(JSON.stringify(values, null, 2));
            actions.setSubmitting(false);
            axios.post('http://127.0.0.1:5000/balance_check/', values)
              .then(function (response) {
                console.log(response);
                console.log(values);
              })
              .catch(function (error) {
                console.log(error);
              });
          }, 1000);
        }}
        render={props => (
          <form onSubmit={props.handleSubmit}>
            <label>
            Device Name: 
              <input
                type="text"
                onChange={props.handleChange}
                onBlur={props.handleBlur}
                value={props.values.fromAccNum}
                name="device_name"
              />
            </label>
            <label>
            Account Num:
              <input
                type="text"
                onChange={props.handleChange}
                onBlur={props.handleBlur}
                value={props.values.fromPvtKey}
                name="accountNum"
              />
            </label>
            <label>
            Private Key:
              <input
                type="text"
                onChange={props.handleChange}
                onBlur={props.handleBlur}
                value={props.values.toAccNum}
                name="pvtKey"
              />
            </label>
            
            <button type="submit">Check Balance</button>
          </form>
        )}
      />
    </div>
  );
  
  export default CheckBalance