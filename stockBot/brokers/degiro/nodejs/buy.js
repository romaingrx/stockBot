const DeGiro = require('degiro'); // Installed with 'npm install --save degiro'

// if environment variables (DEGIRO_USER and DEGIRO_PASS) are set
const degiro = DeGiro.create();  
// Else use this
// const degiro = DeGiro.create({username:RomainGrx, password:1234}); 

// Login to your Degiro account
degiro.login().then(session => console.log(session));

