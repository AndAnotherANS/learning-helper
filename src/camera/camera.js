'use strict';

console.log('camera script');




var mediaSource = new MediaSource();
mediaSource.addEventListener('sourceopen', handleSourceOpen, false);
var mediaRecorder;
var sourceBuffer;
var intervalTimer;
var startTime;
var finishTime;


var gumVideo = document.querySelector('video#gum');
var canvas = document.querySelector('canvas');
canvas.width = 266;
canvas.height = 200;
gumVideo.addEventListener('click', function(){
    let ctx = canvas.getContext('2d');
    ctx.drawImage( gumVideo, 0, 0, canvas.width, canvas.height );

    let image = canvas.toDataURL('image/jpeg');
    console.log(image)
});


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