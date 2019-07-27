// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

// this node function is an example to add device into Azure IoT Hub
// in project Sarah, it is called in the register device function

'use strict';

var iothub = require('azure-iothub');
var uuid = require('uuid');

var connectionString = 'HostName=IoTHub-Yudi.azure-devices.net;SharedAccessKeyName=iothubowner;SharedAccessKey=Ffju9UYKUQrVITQhkPeUrlM/PdfovWnl9K77mwaeWxo=';

var registry = iothub.Registry.fromConnectionString(connectionString);

// Specify the new devices.
var deviceAddArray = [
  {
    deviceId: 'Device1', // can we get this device name info from WebApp???
    status: 'disabled',
    authentication: {
      symmetricKey: {
        primaryKey: Buffer.from(uuid.v4()).toString('base64'),
        secondaryKey: Buffer.from(uuid.v4()).toString('base64')
      }
    }
  }
];

console.log('Adding devices: ' + JSON.stringify(deviceAddArray));

// add one device
registry.addDevices(deviceAddArray, printAndContinue( 'adding', function next() {}));

function printAndContinue(op, next) {
  return function printResult(err, resultData) {
    if (err) console.log(op + ' error: ' + err.toString());
    if (resultData) {
      var arrayString = resultData.errors.length === 0 ? 'no errors' : JSON.stringify(resultData.errors);
      console.log(op + ' isSuccessful: ' + resultData.isSuccessful + ', errors returned: ' + arrayString);
    }
    if (next) next();
  };
}