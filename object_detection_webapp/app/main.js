/*
This is the main javascript file for the application. The script will setup
a model, a video-stream, keybinds, and start the prediction loop with bounding box plotting.

Resources:
 * https://www.tensorflow.org/js/models
 * https://github.com/tensorflow/tfjs-models/tree/master/coco-ssd
 * https://s3.amazonaws.com/ir_public/academy/cheat+sheet/tensorflowJS.pdf
 * https://github.com/tensorflow/tfjs-models
 * https://erdem.pl/2020/02/making-tensorflow-js-work-faster-with-web-workers
 * https://github.com/eisbilen/TFJS-ObjectDetection/blob/master/src/app/app.component.ts
 */

// Setup global variables
let video = document.getElementById('video');
let canvas = document.getElementById("detections");
let ctx = canvas.getContext("2d");
let button = document.getElementById('toggle')

function setupVideo() {
    /* Setup video by starting to stream the media from the webcam. */
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices
            .getUserMedia({
                video: true,
                audio: false
            })
            .then((stream) => {
                video.srcObject = stream;
                video.play();
            },
            err => console.error(err)
        );
    }
}

function setupCanvas() {
    /* Setup canvas to have the same intrinsic size as resolution. */
    const width = canvas.clientWidth;
    const height = canvas.clientHeight;
    if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width;
        canvas.height = height;
    }
}

function setupKeybinds() {
    /* Setup space-bar to toggle the prediction loop. */
    should_run = true;
    document.onkeypress = function (e) {
        e = e || window.event;
        if (e.code == "Space") {
            toggle();
        }
    };
}

function toggle() {
    /* Toggle the state of the prediction loop. */
    should_run = !should_run;
    if (should_run) {
        console.log("Resuming!");
        button.innerText = "Pause";
    } else {
        console.log("Pausing!");
        button.innerText = "Resume";
    }
}

function sleep(ms) {
    /* Sleep for <ms> milliseconds. */
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function loop(model, height, width, scaleFactor) {
    /* Loop with sleep of 200ms followed by object detection prediction and drawing of bounding boxes. */
    while (true) {
        await sleep(200);

        if (!should_run) {
            continue;
        }

        // Make predictions
        const image = tf.image.resizeBilinear(tf.browser.fromPixels(video), [height, width]).asType("int32");
        const predictions = await model.detect(image);

        // Plot boxes and text background
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const font = "16px sans-serif";
        ctx.font = font;
        ctx.textBaseline = "top";
        predictions.forEach(prediction => {
            const x = prediction.bbox[0] * scaleFactor;
            const y = prediction.bbox[1] * scaleFactor;
            const width = prediction.bbox[2] * scaleFactor;
            const height = prediction.bbox[3] * scaleFactor;

            // Draw the bounding box.
            ctx.strokeStyle = "#00FFFF";
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, width, height);

            // Draw the label background.
            ctx.fillStyle = "#00FFFF";
            const textWidth = ctx.measureText(prediction.class).width;
            const textHeight = parseInt(font, 10); // base 10
            ctx.fillRect(x, y, textWidth + 4, textHeight + 4);
        });
    
        // Write text classifications, drawn last to ensure text on top.
        predictions.forEach(prediction => {
            const x = prediction.bbox[0] * scaleFactor;
            const y = prediction.bbox[1] * scaleFactor;

            // Write text
            ctx.fillStyle = "#000000";
            ctx.fillText(prediction.class, x, y);
        });
    }
}

async function main() {
    /* Main entry point with setup of sizes, loading model, and starting prediction loop. */
    if (video.readyState < 3){
        console.error("Camera error: ", video.readyState);
        return;
    }

    const cHeight = canvas.height;
    const cWidth = canvas.width;
    console.log("cHeight=" + cHeight + ", cWidth=" + cWidth);
    const maxHeight = 480;
    const maxWidth = 640;
    let height = maxHeight;
    let width = maxWidth;
    let scaleFactor = 0;
    if (cHeight > maxHeight || cWidth > maxWidth) {
        if (cHeight / maxHeight > cWidth / maxWidth) {
            scaleFactor = cWidth / maxWidth;
            height = Math.round(cHeight / scaleFactor);
        } else {
            scaleFactor = cHeight / maxHeight;
            width = Math.round(cWidth / scaleFactor);
        }
    } else {
        height = cHeight;
        width = cWidth;
    }
    console.log("Height=" + height + ", Width=" + width + ", Scale=" + scaleFactor);

    console.log("Loading model...")
    const model = await cocoSsd.load('lite_mobilenet_v2');
    console.log("Model loaded!")

    tf.setBackend('webgl');
    console.log("Backend: ", tf.getBackend());

    console.log("Starting main prediction loop")
    await loop(model, height, width, scaleFactor);
}

(async () => {
    /* Startup of the application. */
    setupCanvas();
    setupVideo();
    setupKeybinds();
    video.addEventListener('loadeddata', main);
})();
