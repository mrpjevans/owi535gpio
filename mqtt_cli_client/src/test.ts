import readline from "readline";

import { connectAsync } from 'mqtt'

const broker = "mqtt://192.168.1.10"
const topic = "portable/owi535";
let defaultSpeed = 5;

const client = await connectAsync(broker);

readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);

type Payload = {
  motor?: number,
  speed?: number,
  direction?: number
};

const map: { [key: string]: [number, number] } = {
  q: [0, 0],
  w: [0, 1],
  a: [1, 0],
  s: [1, 1],
  z: [2, 0],
  x: [2, 1],
  e: [3, 0],
  r: [3, 1],
  c: [4, 0],
  v: [4, 1],
};

console.log(`Publishing to ${topic} on ${broker}`);

process.stdin.on('keypress', async (str, key) => {
  if (key.ctrl && key.name === 'c') {
    process.exit();
  } else {
    console.log(`Pressed: '${str}'`);

    let payload: Payload = {};
    if (str === " ") {
      payload.speed = 0;
    } else if (str === "f" && defaultSpeed < 10) {
      defaultSpeed += 1;
      payload.speed = defaultSpeed
    } else if (str === "d" && defaultSpeed > 1) {
      defaultSpeed -= 1;
      payload.speed = defaultSpeed;
    } else if (str in map) {
      payload.motor = map[str][0];
      payload.direction = map[str][1];
      payload.speed = defaultSpeed;
    } else {
      console.log("That doesn't do anything");
      return;
    }

    const stringPayload = JSON.stringify(payload);

    console.log(`Publishing: ${stringPayload}`)
    await client.publishAsync(topic, stringPayload);

  }
});

console.log('Ready');