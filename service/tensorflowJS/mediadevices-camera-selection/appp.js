
const button = document.getElementById('button');
const select = document.getElementById('select');


let currentStream;

function stopMediaTracks(stream) {
  stream.getTracks().forEach(track => {
    track.stop();
  });
}

function gotDevices(mediaDevices) {
  select.innerHTML = '';
  select.appendChild(document.createElement('option'));
  let count = 1;
  mediaDevices.forEach(mediaDevice => {
    if (mediaDevice.kind === 'videoinput') {
      const option = document.createElement('option');
      option.value = mediaDevice.deviceId;
      const label = mediaDevice.label || `Camera ${count++}`;
      const textNode = document.createTextNode(label);
      option.appendChild(textNode);
      select.appendChild(option);
    }
  });
}


 async function setupCamera(){
const video = document.getElementById('video');
  if (typeof currentStream !== 'undefined') {
    stopMediaTracks(currentStream);
  }
  const videoConstraints = {};
  if (select.value === '') {
    videoConstraints.facingMode = 'environment';
  } else {
    videoConstraints.deviceId = { exact: select.value };
  }
  const constraints = {
    video: videoConstraints,
    audio: false
  };
  /*
  navigator.mediaDevices.getUserMedia(constraints).then(     stream => {
      currentStream = stream;
      video.srcObject = stream;

      //return navigator.mediaDevices.enumerateDevices();
    }).then(gotDevices)
    .catch(error => {
      console.error(error);
    });*/
    try{
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            video.srcObject = stream;
           }catch(err){alert(err)}
        return new Promise((resolve) => {
            video.onloadedmetadata = () => {
                resolve(video);    };    }    );    }


navigator.mediaDevices.enumerateDevices().then(gotDevices);//加载网页之后就直接运行了

async function loadVideo() {

       const video = await setupCamera();
	   video.play();
	    const net = await posenet.load(0.50);
	    detectPoseInRealTime(video, net);    }
	function detectPoseInRealTime(video, net) {
	    const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        // since images are being fed from a webcam
        const flipHorizontal = true;
        canvas.width = 130;
        canvas.height = 130;
	    //document.getElementById("output").style.display = "inline";
        //L = videoWidth / 5;
        //currX= videoWidth/2;
        //currY= videoHeight/2;
        async function poseDetectionFrame() {
            // Scale an image down to a certain factor. Too large of an image will slow
            // down the GPU
            const imageScaleFactor = 0.3;
            const outputStride = 16;
            //let poses = [];
            //let minPoseConfidence = 0.1;
            //let minPartConfidence = 0.5;
	        const pose = await net.estimateSinglePose(video, imageScaleFactor, flipHorizontal, outputStride);
	        document.getElementById('singlePose').innerHTML= JSON.stringify(pose);
	        //poses.push(pose);
            ctx.clearRect(0, 0, 130, 130);
            ctx.save();
            ctx.scale(-1, 1);
            ctx.translate(-130, 0);
            ctx.drawImage(video, 0, 0, 130, 130);
            ctx.restore();
            // For each pose (i.e. person) detected in an image, loop through the poses
            // and draw the resulting skeleton and keypoints if over certain confidence
            // scores
            //这一部很重要，浏览器不提示栈溢出
            requestAnimationFrame(poseDetectionFrame);    }
        poseDetectionFrame();    }

button.addEventListener('click', event => loadVideo())