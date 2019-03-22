// @tensorflow/tfjs-models Copyright 2019 Google
!function(e,t){"object"==typeof exports&&"undefined"!=typeof module?t(exports,require("@tensorflow/tfjs")):"function"==typeof define&&define.amd?define(["exports","@tensorflow/tfjs"],t):t(e.posenet={},e.tf)}(this,function(e,t){"use strict";var n=function(){function e(e){this.urlPath=e,"/"!==this.urlPath.charAt(this.urlPath.length-1)&&(this.urlPath+="/")}return e.prototype.loadManifest=function(){var e=this;return new Promise(function(t,n){var r=new XMLHttpRequest;r.open("GET",e.urlPath+"manifest.json"),r.onload=function(){e.checkpointManifest=JSON.parse(r.responseText),t()},r.onerror=function(t){throw new Error("manifest.json not found at "+e.urlPath+". "+t)},r.send()})},e.prototype.getCheckpointManifest=function(){var e=this;return null==this.checkpointManifest?new Promise(function(t,n){e.loadManifest().then(function(){t(e.checkpointManifest)})}):new Promise(function(t,n){t(e.checkpointManifest)})},e.prototype.getAllVariables=function(){var e=this;return null!=this.variables?new Promise(function(t,n){t(e.variables)}):new Promise(function(t,n){e.getCheckpointManifest().then(function(n){for(var r=Object.keys(e.checkpointManifest),i=[],o=0;o<r.length;o++)i.push(e.getVariable(r[o]));Promise.all(i).then(function(n){e.variables={};for(var i=0;i<n.length;i++)e.variables[r[i]]=n[i];t(e.variables)})})})},e.prototype.getVariable=function(e){var n=this;if(!(e in this.checkpointManifest))throw new Error("Cannot load non-existant variable "+e);var r=function(r,i){var o=new XMLHttpRequest;o.responseType="arraybuffer";var a=n.checkpointManifest[e].filename;o.open("GET",n.urlPath+a),o.onload=function(){if(404===o.status)throw new Error("Not found variable "+e);var i=new Float32Array(o.response),a=t.Tensor.make(n.checkpointManifest[e].shape,{values:i});r(a)},o.onerror=function(t){throw new Error("Could not fetch variable "+e+": "+t)},o.send()};return null==this.checkpointManifest?new Promise(function(e,t){n.loadManifest().then(function(){new Promise(r).then(e)})}):new Promise(r)},e}(),r=[["conv2d",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1]],i=[8,16,32];function o(e){t.util.assert("number"==typeof e,function(){return"outputStride is not a number"}),t.util.assert(i.indexOf(e)>=0,function(){return"outputStride of "+e+" is invalid. It must be either 8, 16, or 32"})}function a(e){t.util.assert("number"==typeof e,function(){return"imageScaleFactor is not a number"}),t.util.assert(e>=.2&&e<=1,function(){return"imageScaleFactor must be between 0.2 and 1.0"})}var s={100:[["conv2d",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",2],["separableConv",1]],75:[["conv2d",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",2],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1],["separableConv",1]],50:r,25:r};var u=function(){function e(e,n){this.PREPROCESS_DIVISOR=t.scalar(127.5),this.ONE=t.scalar(1),this.modelWeights=e,this.convolutionDefinitions=n}return e.prototype.predict=function(e,n){var r=this,i=t.div(e.toFloat(),this.PREPROCESS_DIVISOR),o=t.sub(i,this.ONE);return function(e,t){var n=1,r=1;return e.map(function(e,i){var o,a,s=e[0],u=e[1];return n===t?(o=1,a=r,r*=u):(o=u,a=1,n*=u),{blockId:i,convType:s,stride:o,rate:a,outputStride:n}})}(this.convolutionDefinitions,n).reduce(function(e,t){var n=t.blockId,i=t.stride,o=t.convType,a=t.rate;if("conv2d"===o)return r.conv(e,i,n);if("separableConv"===o)return r.separableConv(e,i,n,a);throw Error("Unknown conv type of "+o)},o)},e.prototype.convToOutput=function(e,t){return e.conv2d(this.weights(t),1,"same").add(this.convBias(t))},e.prototype.conv=function(e,t,n){var r=this.weights("Conv2d_"+String(n));return e.conv2d(r,t,"same").add(this.convBias("Conv2d_"+String(n))).clipByValue(0,6)},e.prototype.separableConv=function(e,t,n,r){void 0===r&&(r=1);var i="Conv2d_"+String(n)+"_depthwise",o="Conv2d_"+String(n)+"_pointwise";return e.depthwiseConv2D(this.depthwiseWeights(i),t,"same","NHWC",r).add(this.depthwiseBias(i)).clipByValue(0,6).conv2d(this.weights(o),[1,1],"same").add(this.convBias(o)).clipByValue(0,6)},e.prototype.weights=function(e){return this.modelWeights.weights(e)},e.prototype.convBias=function(e){return this.modelWeights.convBias(e)},e.prototype.depthwiseBias=function(e){return this.modelWeights.depthwiseBias(e)},e.prototype.depthwiseWeights=function(e){return this.modelWeights.depthwiseWeights(e)},e.prototype.dispose=function(){this.modelWeights.dispose()},e}();function l(e,t,n,r){return new(n||(n=Promise))(function(i,o){function a(e){try{u(r.next(e))}catch(e){o(e)}}function s(e){try{u(r.throw(e))}catch(e){o(e)}}function u(e){e.done?i(e.value):new n(function(t){t(e.value)}).then(a,s)}u((r=r.apply(e,t||[])).next())})}function c(e,t){var n,r,i,o,a={label:0,sent:function(){if(1&i[0])throw i[1];return i[1]},trys:[],ops:[]};return o={next:s(0),throw:s(1),return:s(2)},"function"==typeof Symbol&&(o[Symbol.iterator]=function(){return this}),o;function s(o){return function(s){return function(o){if(n)throw new TypeError("Generator is already executing.");for(;a;)try{if(n=1,r&&(i=2&o[0]?r.return:o[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,o[1])).done)return i;switch(r=0,i&&(o=[2&o[0],i.value]),o[0]){case 0:case 1:i=o;break;case 4:return a.label++,{value:o[1],done:!1};case 5:a.label++,r=o[1],o=[0];continue;case 7:o=a.ops.pop(),a.trys.pop();continue;default:if(!(i=(i=a.trys).length>0&&i[i.length-1])&&(6===o[0]||2===o[0])){a=0;continue}if(3===o[0]&&(!i||o[1]>i[0]&&o[1]<i[3])){a.label=o[1];break}if(6===o[0]&&a.label<i[1]){a.label=i[1],i=o;break}if(i&&a.label<i[2]){a.label=i[2],a.ops.push(o);break}i[2]&&a.ops.pop(),a.trys.pop();continue}o=t.call(e,a)}catch(e){o=[6,e],r=0}finally{n=i=0}if(5&o[0])throw o[1];return{value:o[0]?o[1]:void 0,done:!0}}([o,s])}}}var f=["nose","leftEye","rightEye","leftEar","rightEar","leftShoulder","rightShoulder","leftElbow","rightElbow","leftWrist","rightWrist","leftHip","rightHip","leftKnee","rightKnee","leftAnkle","rightAnkle"],p=f.length,h=f.reduce(function(e,t,n){return e[t]=n,e},{}),v=[["nose","leftEye"],["leftEye","leftEar"],["nose","rightEye"],["rightEye","rightEar"],["nose","leftShoulder"],["leftShoulder","leftElbow"],["leftElbow","leftWrist"],["leftShoulder","leftHip"],["leftHip","leftKnee"],["leftKnee","leftAnkle"],["nose","rightShoulder"],["rightShoulder","rightElbow"],["rightElbow","rightWrist"],["rightShoulder","rightHip"],["rightHip","rightKnee"],["rightKnee","rightAnkle"]],d=[["leftHip","leftShoulder"],["leftElbow","leftShoulder"],["leftElbow","leftWrist"],["leftHip","leftKnee"],["leftKnee","leftAnkle"],["rightHip","rightShoulder"],["rightElbow","rightShoulder"],["rightElbow","rightWrist"],["rightHip","rightKnee"],["rightKnee","rightAnkle"],["leftShoulder","rightShoulder"],["leftHip","rightHip"]].map(function(e){var t=e[0],n=e[1];return[h[t],h[n]]});var m=Number.NEGATIVE_INFINITY,b=Number.POSITIVE_INFINITY;function g(e){return e.reduce(function(e,t){var n=e.maxX,r=e.maxY,i=e.minX,o=e.minY,a=t.position,s=a.x,u=a.y;return{maxX:Math.max(n,s),maxY:Math.max(r,u),minX:Math.min(i,s),minY:Math.min(o,u)}},{maxX:m,maxY:m,minX:b,minY:b})}function y(e,n){return void 0===n&&(n="float32"),l(this,void 0,void 0,function(){var r;return c(this,function(i){switch(i.label){case 0:return[4,e.data()];case 1:return r=i.sent(),[2,t.buffer(e.shape,n,r)]}})})}function w(e,t,n){return{score:e.score,keypoints:e.keypoints.map(function(e){var r=e.score,i=e.part,o=e.position;return{score:r,part:i,position:{x:o.x*n,y:o.y*t}}})}}function _(e,t,n){var r=t*e-1;return r-r%n+1}function x(e){return e instanceof t.Tensor?[e.shape[0],e.shape[1]]:[e.height,e.width]}function C(e,n,r,i){return t.tidy(function(){var o=function(e){return e instanceof t.Tensor?e:t.browser.fromPixels(e)}(e);return i?o.reverse(1).resizeBilinear([n,r]):o.resizeBilinear([n,r])})}function E(e){return Math.floor(e/2)}var k=function(){function e(e,t){this.priorityQueue=new Array(e),this.numberOfElements=-1,this.getElementValue=t}return e.prototype.enqueue=function(e){this.priorityQueue[++this.numberOfElements]=e,this.swim(this.numberOfElements)},e.prototype.dequeue=function(){var e=this.priorityQueue[0];return this.exchange(0,this.numberOfElements--),this.sink(0),this.priorityQueue[this.numberOfElements+1]=null,e},e.prototype.empty=function(){return-1===this.numberOfElements},e.prototype.size=function(){return this.numberOfElements+1},e.prototype.all=function(){return this.priorityQueue.slice(0,this.numberOfElements+1)},e.prototype.max=function(){return this.priorityQueue[0]},e.prototype.swim=function(e){for(;e>0&&this.less(E(e),e);)this.exchange(e,E(e)),e=E(e)},e.prototype.sink=function(e){for(;2*e<=this.numberOfElements;){var t=2*e;if(t<this.numberOfElements&&this.less(t,t+1)&&t++,!this.less(e,t))break;this.exchange(e,t),e=t}},e.prototype.getValueAt=function(e){return this.getElementValue(this.priorityQueue[e])},e.prototype.less=function(e,t){return this.getValueAt(e)<this.getValueAt(t)},e.prototype.exchange=function(e,t){var n=this.priorityQueue[e];this.priorityQueue[e]=this.priorityQueue[t],this.priorityQueue[t]=n},e}();function S(e,t,n,r,i,o){for(var a=o.shape,s=a[0],u=a[1],l=!0,c=Math.max(n-i,0),f=Math.min(n+i+1,s),p=c;p<f;++p){for(var h=Math.max(r-i,0),v=Math.min(r+i+1,u),d=h;d<v;++d)if(o.get(p,d,e)>t){l=!1;break}if(!l)break}return l}function M(e,t,n,r){return{y:r.get(e,t,n),x:r.get(e,t,n+p)}}function P(e,t,n){var r=M(e.heatmapY,e.heatmapX,e.id,n),i=r.y,o=r.x;return{x:e.heatmapX*t+o,y:e.heatmapY*t+i}}function O(e,t,n){return e<t?t:e>n?n:e}function N(e,t){return{x:e.x+t.x,y:e.y+t.y}}var T=v.map(function(e){var t=e[0],n=e[1];return[h[t],h[n]]}),B=T.map(function(e){return e[1]}),A=T.map(function(e){return e[0]});function V(e,t,n,r){return{y:O(Math.round(e.y/t),0,n-1),x:O(Math.round(e.x/t),0,r-1)}}function I(e,t,n,r,i,o,a){var s=r.shape,u=s[0],l=s[1],c=function(e,t,n){var r=n.shape[2]/2;return{y:n.get(t.y,t.x,e),x:n.get(t.y,t.x,r+e)}}(e,V(t.position,o,u,l),a),p=V(N(t.position,c),o,u,l),h=M(p.y,p.x,n,i),v=r.get(p.y,p.x,n);return{position:N({x:p.x*o,y:p.y*o},{x:h.x,y:h.y}),part:f[n],score:v}}function W(e,t,n,r,i,o){var a=t.shape[2],s=B.length,u=new Array(a),l=e.part,c=e.score,p=P(l,r,n);u[l.id]={score:c,part:f[l.id],position:p};for(var h=s-1;h>=0;--h){var v=B[h],d=A[h];u[v]&&!u[d]&&(u[d]=I(h,u[v],d,t,n,r,o))}for(h=0;h<s;++h){v=A[h],d=B[h];u[v]&&!u[d]&&(u[d]=I(h,u[v],d,t,n,r,i))}return u}function F(e,t,n,r){var i=n.x,o=n.y;return e.some(function(e){var n,a,s,u,l,c,f=e.keypoints[r].position;return n=o,a=i,s=f.y,u=f.x,(l=s-n)*l+(c=u-a)*c<=t})}function H(e,t,n){return n.reduce(function(n,r,i){var o=r.position,a=r.score;return F(e,t,o,i)||(n+=a),n},0)/n.length}var j=1;function X(e,t,n,r,i,o,a,s){return void 0===a&&(a=.5),void 0===s&&(s=20),l(this,void 0,void 0,function(){var u,f,p,h,v,d,m,b,g,w,_,x;return c(this,function(C){switch(C.label){case 0:return u=[],[4,function(e){return l(this,void 0,void 0,function(){return c(this,function(t){return[2,Promise.all(e.map(function(e){return y(e,"float32")}))]})})}([e,t,n,r])];case 1:for(f=C.sent(),p=f[0],h=f[1],v=f[2],d=f[3],m=function(e,t,n){for(var r=n.shape,i=r[0],o=r[1],a=r[2],s=new k(i*o*a,function(e){return e.score}),u=0;u<i;++u)for(var l=0;l<o;++l)for(var c=0;c<a;++c){var f=n.get(u,l,c);f<e||S(c,f,u,l,t,n)&&s.enqueue({score:f,part:{heatmapY:u,heatmapX:l,id:c}})}return s}(a,j,p),b=s*s;u.length<o&&!m.empty();)g=m.dequeue(),w=P(g.part,i,h),F(u,b,w,g.part.id)||(_=W(g,p,h,i,v,d),x=H(u,b,_),u.push({keypoints:_,score:x}));return[2,u]}})})}function Y(e){var n=e.shape,r=n[0],i=n[1],o=n[2];return t.tidy(function(){var n,a,s=e.reshape([r*i,o]).argMax(0),u=s.div(t.scalar(i,"int32")).expandDims(1),l=(n=s,a=i,t.tidy(function(){var e=n.div(t.scalar(a,"int32"));return n.sub(e.mul(t.scalar(a,"int32")))})).expandDims(1);return t.concat([u,l],1)})}function K(e,t,n,r){return{y:r.get(e,t,n),x:r.get(e,t,n+p)}}function Q(e,n,r){return t.tidy(function(){var i=function(e,n){for(var r=[],i=0;i<p;i++){var o=K(e.get(i,0).valueOf(),e.get(i,1).valueOf(),i,n),a=o.x,s=o.y;r.push(s),r.push(a)}return t.tensor2d(r,[p,2])}(e,r);return e.toTensor().mul(t.scalar(n,"int32")).toFloat().add(i)})}function R(e,t,n){return l(this,void 0,void 0,function(){var r,i,o,a,s,u,l,p,h,v;return c(this,function(c){switch(c.label){case 0:return r=0,i=Y(e),[4,Promise.all([y(e),y(t),y(i,"int32")])];case 1:return o=c.sent(),a=o[0],s=o[1],u=o[2],[4,y(l=Q(u,n,s))];case 2:return p=c.sent(),h=Array.from(function(e,t){for(var n=t.shape[0],r=new Float32Array(n),i=0;i<n;i++){var o=t.get(i,0),a=t.get(i,1);r[i]=e.get(o,a,i)}return r}(a,u)),v=h.map(function(e,t){return r+=e,{position:{y:p.get(t,0),x:p.get(t,1)},part:f[t],score:e}}),i.dispose(),l.dispose(),[2,{keypoints:v,score:r/v.length}]}})})}
var q="https://wangkaibiao.github.io/SettlersFinancialData3/service/posenet/"
,D={1.01:{url:q+"mobilenet_v1_101/",architecture:s[100]},1:{url:q+"mobilenet_v1_100/",architecture:s[100]},.75:{url:q+"mobilenet_v1_075/",architecture:s[75]},.5:{url:q+"mobilenet_v1_050/",architecture:s[50]}},G=function(){function e(e){this.variables=e}return e.prototype.weights=function(e){return this.variables["MobilenetV1/"+e+"/weights"]},e.prototype.depthwiseBias=function(e){return this.variables["MobilenetV1/"+e+"/biases"]},e.prototype.convBias=function(e){return this.depthwiseBias(e)},e.prototype.depthwiseWeights=function(e){return this.variables["MobilenetV1/"+e+"/depthwise_weights"]},e.prototype.dispose=function(){for(var e in this.variables)this.variables[e].dispose()},e}(),z=function(){function e(e){this.mobileNet=e}return e.prototype.predictForSinglePose=function(e,n){var r=this;return void 0===n&&(n=16),o(n),t.tidy(function(){var t=r.mobileNet.predict(e,n),i=r.mobileNet.convToOutput(t,"heatmap_2"),o=r.mobileNet.convToOutput(t,"offset_2");return{heatmapScores:i.sigmoid(),offsets:o}})},e.prototype.predictForMultiPose=function(e,n){var r=this;return void 0===n&&(n=16),t.tidy(function(){var t=r.mobileNet.predict(e,n),i=r.mobileNet.convToOutput(t,"heatmap_2"),o=r.mobileNet.convToOutput(t,"offset_2"),a=r.mobileNet.convToOutput(t,"displacement_fwd_2"),s=r.mobileNet.convToOutput(t,"displacement_bwd_2");return{heatmapScores:i.sigmoid(),offsets:o,displacementFwd:a,displacementBwd:s}})},e.prototype.estimateSinglePose=function(e,n,r,i){return void 0===n&&(n=.5),void 0===r&&(r=!1),void 0===i&&(i=16),l(this,void 0,void 0,function(){var s,u,l,f,p,h,v,d,m,b,g,y=this;return c(this,function(c){switch(c.label){case 0:return o(i),a(n),s=x(e),u=s[0],l=s[1],f=_(n,u,i),p=_(n,l,i),h=t.tidy(function(){var t=C(e,f,p,r);return y.predictForSinglePose(t,i)}),v=h.heatmapScores,d=h.offsets,[4,R(v,d,i)];case 1:return m=c.sent(),b=u/f,g=l/p,v.dispose(),d.dispose(),[2,w(m,b,g)]}})})},e.prototype.estimateMultiplePoses=function(e,n,r,i,s,u,f){return void 0===n&&(n=.5),void 0===r&&(r=!1),void 0===i&&(i=16),void 0===s&&(s=5),void 0===u&&(u=.5),void 0===f&&(f=20),l(this,void 0,void 0,function(){var l,p,h,v,d,m,b,g,y,E,k,S=this;return c(this,function(c){switch(c.label){case 0:return o(i),a(n),l=x(e),p=l[0],h=l[1],v=_(n,p,i),d=_(n,h,i),m=t.tidy(function(){var t=C(e,v,d,r);return S.predictForMultiPose(t,i)}),b=m.heatmapScores,g=m.offsets,y=m.displacementFwd,E=m.displacementBwd,[4,X(b,g,y,E,i,s,u,f)];case 1:return k=c.sent(),b.dispose(),g.dispose(),y.dispose(),E.dispose(),[2,function(e,t,n){return 1===n&&1===t?e:e.map(function(e){return w(e,t,n)})}(k,p/v,h/d)]}})})},e.prototype.dispose=function(){this.mobileNet.dispose()},e}();var L={load:function(e){return l(void 0,void 0,void 0,function(){var t,r,i;return c(this,function(o){switch(o.label){case 0:return t=D[e],[4,new n(t.url).getAllVariables()];case 1:return r=o.sent(),i=new G(r),[2,new u(i,t.architecture)]}})})}};e.decodeMultiplePoses=X,e.decodeSinglePose=R,e.MobileNet=u,e.mobileNetArchitectures=s,e.CheckpointLoader=n,e.checkpoints=D,e.partChannels=["left_face","right_face","right_upper_leg_front","right_lower_leg_back","right_upper_leg_back","left_lower_leg_front","left_upper_leg_front","left_upper_leg_back","left_lower_leg_back","right_feet","right_lower_leg_front","left_feet","torso_front","torso_back","right_upper_arm_front","right_upper_arm_back","right_lower_arm_back","left_lower_arm_front","left_upper_arm_front","left_upper_arm_back","left_lower_arm_back","right_hand","right_lower_arm_front","left_hand"],e.partIds=h,e.partNames=f,e.poseChain=v,e.load=function(e){return void 0===e&&(e=1.01),l(this,void 0,void 0,function(){var n,r;return c(this,function(i){switch(i.label){case 0:if(null==t)throw new Error("Cannot find TensorFlow.js. If you are using a <script> tag, please also include @tensorflow/tfjs on the page before using this model.");return n=Object.keys(D),t.util.assert("number"==typeof e,function(){return"got multiplier type of "+typeof e+" when it should be a number."}),t.util.assert(n.indexOf(e.toString())>=0,function(){return"invalid multiplier value of "+e+".  No checkpoint exists for that multiplier. Must be one of "+n.join(",")+"."}),[4,L.load(e)];case 1:return r=i.sent(),[2,new z(r)]}})})},e.PoseNet=z,e.getAdjacentKeyPoints=function(e,t){return d.reduce(function(n,r){var i=r[0],o=r[1];return function(e,t,n){return e<n||t<n}(e[i].score,e[o].score,t)?n:(n.push([e[i],e[o]]),n)},[])},e.getBoundingBox=g,e.getBoundingBoxPoints=function(e){var t=g(e),n=t.minX,r=t.minY,i=t.maxX,o=t.maxY;return[{x:n,y:r},{x:i,y:r},{x:i,y:o},{x:n,y:o}]},e.scalePose=w,Object.defineProperty(e,"__esModule",{value:!0})});
