import readline from "readline";

import { connectAsync } from 'mqtt'

const broker = "mqtt://192.168.1.10"
const topic = "portable/owi535";
let defaultSpeed = 5;

const client = await connectAsync(broker);

readline.emitKeypressEvents(process.stdin);
process.stdin.setRawMode(true);

type Payload = {
  motor: string,
  speed: number,
  direction: number,
  duration: number
};

const map: { [key: string]: [string, number] } = {
  q: ["wrist", 0],
  w: ["wrist", 1],
  a: ["elbow", 0],
  s: ["elbow", 1],
  z: ["shoulder", 0],
  x: ["shoulder", 1],
  e: ["grip", 0],
  r: ["grip", 1],
  c: ["base", 0],
  v: ["base", 1],
};

console.log(`Publishing to ${topic} on ${broker}`);

process.stdin.on('keypress', async (str, key) => {
  if (key.ctrl && key.name === 'c') {
    process.exit();
  } else {
    console.log(`Pressed: '${str}'`);

    let payload: Payload = {
      motor: "base",
      speed: 0,
      direction: 0,
      duration: 0
    };
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