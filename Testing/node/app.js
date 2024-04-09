const { createClient } = require('node-thinkgear-sockets');
const { fromEvent } = require('rxjs/observable/fromEvent');

const client = createClient();
client.connect();

fromEvent(client, 'data')
    .subscribe(eeg => console.log(eeg));