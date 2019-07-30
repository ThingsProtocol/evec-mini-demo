import React from 'react';
import { Formik } from 'formik';
import axios from 'axios';


//transfer fund
const TransferForm = () => (
  <div>
    <h1>Send Fund</h1>
    <Formik
      onSubmit={(values, actions) => {
        setTimeout(() => {
          alert(JSON.stringify(values, null, 2));
          actions.setSubmitting(false);
          axios.post('http://127.0.0.1:5000/transfer_fund/', values)
          .then(res => {
            console.log(res);
            console.log(res.data);
            const output = res.data;
            this.setState({ output });
          })




          // .then(function (response) {
            //   console.log(response);
            //   //console.log(values);
            // })
            // .catch(function (error) {
            //   console.log(error);
            // });
        }, 1000);
      }}
      render={props => (
        <form onSubmit={props.handleSubmit}>
          <label>
          fromAccNum: 
            <input
              type="text"
              onChange={props.handleChange}
              onBlur={props.handleBlur}
              value={props.values.fromAccNum}
              //defaultValue = 'fromAccNum'
              name="fromAccNum"
            />
          </label>
          <label>
          fromPvtKey:
            <input
              type="text"
              onChange={props.handleChange}
              onBlur={props.handleBlur}
              value={props.values.fromPvtKey}
              name="fromPvtKey"
            />
          </label>
          <label>
          toAccNum:
            <input
              type="text"
              onChange={props.handleChange}
              onBlur={props.handleBlur}
              value={props.values.toAccNum}
              //label = 'email'
              name="toAccNum"
            />
          </label>
          <label>
          amount:
            <input
              type="text"
              onChange={props.handleChange}
              onBlur={props.handleBlur}
              value={props.values.amount}
              name="amount"
            />
          </label>
          <button type="submit">Send Fund</button>
        </form>
      )}
    />
  </div>
);

export default TransferForm




