//全局变量
const button = document.getElementById('button');
const select = document.getElementById('select');
const audio = document.getElementById("audio0");
const status = document.getElementById('status');


//测试自动循环
function loopPlay(){
    //const audio = document.getElementById("audio0");
    document.getElementById('singlePose').innerHTML =!audio.paused;
    var x = audio.src;
    //audio.addEventListener("playing", function(){});
    audio.addEventListener("pause", audio.play());
    requestAnimationFrame(loopPlay);//这个不仅能实现自调用，还能防止栈溢出
                  }
//loopPlay();


//control
function check(){
    //document.getElementById('singlePose').innerHTML=status.innerHTML;
    if (status.innerHTML=="paused"){
        status.innerHTML="waiting";    }
    else{status.innerHTML="paused";    }     }

status.addEventListener('click', event => check());
document.getElementById('showtest').innerHTML=5<"null";//空值也参与运算;5>null为true,5和"null"比都是false

//获取摄像头设备
let currentStream;

function stopMediaTracks(stream) {
    stream.getTracks().forEach(track => {
    track.stop();    }    );    }

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
            select.appendChild(option);    }    }    );
}

navigator.mediaDevices.enumerateDevices().then(gotDevices);//加载网页之后就直接运行了


//获取视频流
async function setupCamera(){
    const video = document.getElementById('video');
    if (typeof currentStream !== 'undefined') {
        stopMediaTracks(currentStream);    }
    const videoConstraints = {};
    if (select.value === '') {
        videoConstraints.facingMode = 'environment';    }
    else {
        videoConstraints.deviceId = { exact: select.value };    }
    const constraints = {
        video: videoConstraints,
        audio: false    };
    /*
    navigator.mediaDevices.getUserMedia(constraints).then(stream => {
        currentStream = stream;
        video.srcObject = stream;
        return navigator.mediaDevices.enumerateDevices();    }).then(gotDevices).catch(error => {
            console.error(error);    }    );
    */
    try{
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;    }catch(err){alert(err)}
    return new Promise((resolve) => {video.onloadedmetadata = () => {
        resolve(video);    };    }    );    }

async function loadVideo() {
    const video = await setupCamera();
	video.play();
	//document.getElementById('showtest').innerHTML=video.width+","+video.height;
	const net = await posenet.load(1.00);
	detectPoseInRealTime(video, net);
	//requestAnimationFrame(loadVideo);
	//play(video, net);
	                       }

function detectPoseInRealTime(video, net) {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    // since images are being fed from a webcam
    const flipHorizontal = false;//true;的效果差
    //canvas.width = video.width;
    //canvas.height = video.height;
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
        let minPoseConfidence = 0.1;
        let minPartConfidence = 0.5;
        if (audio.paused & status.innerHTML=="paused"){
            status.innerHTML="waiting";
            const pose = await net.estimateSinglePose(video, imageScaleFactor, flipHorizontal, outputStride);
	        //document.getElementById('singlePose').innerHTML= JSON.stringify(pose);
	        //poses.push(pose);
	        //document.getElementById('singlePose').innerHTML= pose.score;
	        //document.getElementById('singlePose').innerHTML=JSON.stringify( pose.keypoints[1]);

/* {"score":0.18446882074589238,"keypoints":[
{"score":0.6417005658149719,"part":"nose","position":{"x":56.495598301743016,"y":113.11837514241536}},
{"score":0.4671669602394104,"part":"leftEye","position":{"x":66.714881550182,"y":101.28246076179273}},
{"score":0.5327326655387878,"part":"rightEye","position":{"x":55.739575010357484,"y":101.64757121693005}},
{"score":0.15938811004161835,"part":"leftEar","position":{"x":91.44621588967064,"y":113.03567077174331}},
{"score":0.12185829877853394,"part":"rightEar","position":{"x":49.02600808577104,"y":111.64298086455375}},
{"score":0.27013903856277466,"part":"leftShoulder","position":{"x":102.08201899673,"y":129.3080844301166}},
{"score":0.2553987503051758,"part":"rightShoulder","position":{"x":28.06698900280577,"y":142.37862095688328}},
{"score":0.19427983462810516,"part":"leftElbow","position":{"x":97.59928732207327,"y":157.63011238791725}},
{"score":0.13131378591060638,"part":"rightElbow","position":{"x":32.047804630163945,"y":154.92721904407847}},
{"score":0.16482456028461456,"part":"leftWrist","position":{"x":67.66207839503433,"y":161.3046900431315}},
{"score":0.07185297459363937,"part":"rightWrist","position":{"x":53.37408874974106,"y":163.22847770922112}},
{"score":0.03781336545944214,"part":"leftHip","position":{"x":72.87345308246034,"y":195.2580989490856}},
{"score":0.031015999615192413,"part":"rightHip","position":{"x":49.072826558893375,"y":192.62467817826706}},
{"score":0.01984754391014576,"part":"leftKnee","position":{"x":68.14571149421461,"y":178.53997432824337}},
{"score":0.010319637134671211,"part":"rightKnee","position":{"x":52.1284513762503,"y":177.15177015824753}},
{"score":0.01603000797331333,"part":"leftAnkle","position":{"x":6.333806912104289,"y":76.75166216763583}},
{"score":0.010287853889167309,"part":"rightAnkle","position":{"x":12.04725778464115,"y":74.28635510531339}}
]}*/

       if(pose.score > minPoseConfidence){
           let list_17name=[];
           let list_17x=[];
           let list_17y=[];
	       pose.keypoints.forEach(({score, part,position}) => {
	           if (score >= minPartConfidence) {
	               //document.getElementById('singlePose').innerHTML= part;
	               list_17name.push(part);
                   list_17x.push(position.x.toFixed(1));
                   list_17y.push(position.y.toFixed(1));    }
               else{
                   list_17x.push("null");//null是能够参与比较的
                   list_17y.push("null");    }    }    );
           document.getElementById('posename').innerHTML= list_17name;
           document.getElementById('posex').innerHTML= list_17x;
           document.getElementById('posey').innerHTML= list_17y;
           var x ;
           //"身体呈正 人 字站立，双臂向外稍微张开; 图片的左上角是原点（0,0）、图片和现实相反"
           nosex=list_17x[0]
           nosey=list_17y[0]//#以鼻子为参照点
           //#以手腕作为活动点
           try{
           if (list_17x[10]< nosex & list_17y[10] < nosey){
               x='./Piano/res/sound/C3.mp3';
               document.getElementById('singlePose').innerHTML="右手 垂直向上指"+x;    }
           else if (list_17x[10]> nosex & list_17y[10] < nosex){
               x='./Piano/res/sound/D3.mp3';
               document.getElementById('singlePose').innerHTML="右手朝左上方指、高于鼻子"+x;    }
           else if (list_17x[10]> nosex & list_17y[10] > nosey){
               x='./Piano/res/sound/E3.mp3';
               document.getElementById('singlePose').innerHTML="右手朝左指、不高于 鼻子"+x;    }
           else if (list_17x[9]> nosex & list_17y[9] < nosey){
               x='./Piano/res/sound/F3.mp3';
               document.getElementById('singlePose').innerHTML="左手 垂直向上指"+x;    }
           else if (list_17x[9]< nosex & list_17y[9] < nosex){
               x='./Piano/res/sound/G3.mp3';
               document.getElementById('singlePose').innerHTML="左手朝右上方指、高于鼻子"+x;    }
           else if (list_17x[9]< nosex & list_17y[9] > nosey){
               x='./Piano/res/sound/A3.mp3';
               document.getElementById('singlePose').innerHTML="左手朝右指、不高于 鼻子"+x;    }
           else if ((list_17x[9]< nosex & list_17y[9] > nosey) & (list_17x[10]< nosex & list_17y[10] < nosey)){
               x='./Piano/res/sound/B3.mp3';
               document.getElementById('singlePose').innerHTML="左手朝右指、不高于 鼻子;右手 垂直向上指"+x;    }
           }catch(err){document.getElementById('singlePose').innerHTML=err}


           if(typeof x !== 'undefined') {
               audio.src=x;
               audio.play();
               // For each pose (i.e. person) detected in an image, loop through the poses
               // and draw the resulting skeleton and keypoints if over certain confidence
               // scores
               //audio.addEventListener("playing", function(){});
                                       }
           else{document.getElementById('singlePose').innerHTML="姿势未编码";

               }

           ctx.clearRect(0, 0, canvas.width, canvas.height);
           //ctx.save();
           //ctx.scale(-1, 1);
           //ctx.translate(-canvas.width, 0);//画反方向图，和其他配套使用、否则canvas不显示
           //ctx.translate(canvas.width, 0);//这一步不起作用
           ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
           ctx.fillText("起点",10,10);
           ctx.fillText("终点",canvas.width-20, canvas.height-20);
           //ctx.restore();
           for(i=0;i<17;i++){
               ctx.fillText(list_17x[i]+list_17name[i]+list_17y[i],list_17x[i],list_17y[i]);
                            }

           }    }

        requestAnimationFrame(poseDetectionFrame);//这一步很重要，浏览器不提示栈溢出
                                       }
    poseDetectionFrame();    }

button.addEventListener('click', event => loadVideo());